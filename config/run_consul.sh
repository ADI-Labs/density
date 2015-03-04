#!/bin/sh
# http://www.consul.io/docs/commands/index.html

consul agent \
    -server \
    -bootstrap \
    -client 0.0.0.0 \
    -data-dir ~/consul \
    -ui-dir /usr/share/consul/ui

