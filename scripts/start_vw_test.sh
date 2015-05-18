#!/bin/bash

vagrant ssh -- nohup vw --daemon --port 26542 --pid_file /tmp/vw.pid &