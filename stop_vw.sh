#!/bin/bash

if [ -e "/tmp/vw.pid" ]; then
    cat /tmp/vw.pid | xargs kill
fi