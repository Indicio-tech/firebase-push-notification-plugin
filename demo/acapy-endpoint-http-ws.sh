#!/bin/bash

TUNNEL_ENDPOINT_HTTP=${TUNNEL_ENDPOINT_HTTP}
TUNNEL_ENDPOINT_WS=${TUNNEL_ENDPOINT_WS}
#TODO: assert env's

while [[ "$(curl -s -o /dev/null -w '%{http_code}' "${TUNNEL_ENDPOINT_HTTP}/status")" != "200" ]]; do
    echo "Waiting for tunnel..."
    sleep 1
done
while [[ "$(curl -s -o /dev/null -w '%{http_code}' "${TUNNEL_ENDPOINT_WS}/status")" != "200" ]]; do
    echo "Waiting for tunnel..."
    sleep 1
done
ACAPY_ENDPOINT_HTTP=$(curl --silent "${TUNNEL_ENDPOINT_HTTP}/start" | python -c "import sys, json; print(json.load(sys.stdin)['url'])")
echo "fetched end point [$TUNNEL_ENDPOINT_HTTP]"
ACAPY_ENDPOINT_WS=$(curl --silent "${TUNNEL_ENDPOINT_WS}/start" | python -c "import sys, json; print(json.load(sys.stdin)['url'])")
echo "fetched end point [$TUNNEL_ENDPOINT_WS]"

export ACAPY_ENDPOINT="[$ACAPY_ENDPOINT_HTTP, $ACAPY_ENDPOINT_WS, ${ACAPY_ENDPOINT/http/ws}/ws]"
#export ACAPY_ENDPOINT="$ACAPY_ENDPOINT"
exec "$@"
