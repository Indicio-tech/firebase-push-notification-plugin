#!/bin/bash

TUNNEL_ENDPOINT_HTTP=${TUNNEL_ENDPOINT_HTTP}
TUNNEL_ENDPOINT_WS=${TUNNEL_ENDPOINT_WS}
#TODO: assert env's
if [ -z ${TUNNEL_ENDPOINT_HTTP+x} ]; then echo "WARNING TUNNEL_ENDPOINT_HTTP is unset"; else echo "TUNNEL_ENDPOINT_HTTP is set to '$TUNNEL_ENDPOINT_HTTP'"; fi
if [ -z ${TUNNEL_ENDPOINT_WS+x} ]; then echo "WARNING TUNNEL_ENDPOINT_WS is unset"; else echo "TUNNEL_ENDPOINT_WS is set to '$TUNNEL_ENDPOINT_WS'"; fi
for ENDPOINT in TUNNEL_ENDPOINT_HTTP, TUNNEL_ENDPOINT_WS
do 
    while [[ "$(curl -s -o /dev/null -w '%{http_code}' "${ENDPOINT}/status")" != "200" ]]; do
        echo "Waiting for $ENDPOINT tunnel..."
        sleep 1
    done
done
ACAPY_ENDPOINT_HTTP=$(curl --silent "${TUNNEL_ENDPOINT_HTTP}/start" | python -c "import sys, json; print(json.load(sys.stdin)['url'])")
echo "fetched end point [$TUNNEL_ENDPOINT_HTTP]"
ACAPY_ENDPOINT_WS=$(curl --silent "${TUNNEL_ENDPOINT_WS}/start" | python -c "import sys, json; print(json.load(sys.stdin)['url'])")
echo "fetched end point [$TUNNEL_ENDPOINT_WS]"

export ACAPY_ENDPOINT="[$ACAPY_ENDPOINT_HTTP, ${ACAPY_ENDPOINT_WS/http/ws}]"
exec "$@"
