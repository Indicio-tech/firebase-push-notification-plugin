import sys

from aries_cloudagent.messaging.agent_message import AgentMessage, AgentMessageSchema


def generate_model_schema(  # pylint: disable=protected-access
    name: str, handler: str, msg_type: str, schema: dict, *, init: callable = None
):
    """Generate a Message model class and schema class programmatically.

    The following would result in a class named XYZ inheriting from
    AgentMessage and XYZSchema inheriting from AgentMessageSchema.

    XYZ, XYZSchema = generate_model_schema(
        name='XYZ',
        handler='aries_cloudagent.admin.handlers.XYZHandler',
        msg_type='{}/xyz'.format(PROTOCOL),
        schema={}
    )

    The attributes of XYZ are determined by schema's keys. The actual
    schema of XYZSchema is defined by the field-value combinations of
    schema_dict, similar to marshmallow's Schema.from_dict() (can't actually
    use that here as the model_class must be set in the Meta inner-class of
    AgentMessageSchemas).
    """
    if isinstance(schema, dict):
        slots = list(schema.keys())
        schema_dict = schema
    elif hasattr(schema, "_declared_fields"):
        slots = list(schema._declared_fields.keys())
        schema_dict = schema._declared_fields
    else:
        raise TypeError("Schema must be dict or class defining _declared_fields")

    class Model(AgentMessage):
        """Generated Model."""

        __slots__ = slots
        __qualname__ = name
        __name__ = name
        __module__ = sys._getframe(2).f_globals["__name__"]
        __init__ = init if init else generic_init

        @property
        def _type(self):
            """
            Override default _type method to ensure incorrect DIDComm Prefix
            is not prepended to all our message types.
            """
            return self.Meta.message_type

        class Meta:
            """Generated Meta."""

            __qualname__ = name + ".Meta"
            handler_class = handler
            message_type = msg_type
            schema_class = name + "Schema"

    class Schema(AgentMessageSchema):
        """Generated Schema."""

        __qualname__ = name + "Schema"
        __name__ = name + "Schema"
        __module__ = sys._getframe(2).f_globals["__name__"]

        class Meta:
            """Generated Schema Meta."""

            __qualname__ = name + "Schema.Meta"
            model_class = Model

    Schema._declared_fields.update(schema_dict)

    return Model, Schema


def generic_init(instance, **kwargs):
    """Initialize from kwargs into slots."""
    for slot in instance.__slots__:
        setattr(instance, slot, kwargs.get(slot))
        if slot in kwargs:
            del kwargs[slot]
    super(type(instance), instance).__init__(**kwargs)