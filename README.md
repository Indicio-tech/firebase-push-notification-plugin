Firebase Push Notification Plugin
=======================================

[Add description]

## Installation and Usage

First, install this plugin into your environment.

```sh
$ pip install git+https://github.com/Indicio-tech/firebase-push-notification-plugin.git
```

When starting up ACA-Py, load the plugin along with any other startup
parameters.

```sh
$ aca-py start --arg-file my_config.yml --plugin firebase_push_notification
```
## Running Tests for development

```sh
pytest --cov-report term-missing --cov
```