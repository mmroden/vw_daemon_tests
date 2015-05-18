#!/bin/bash

vw -f model.vw --save_resume --daemon --loss_function logistic --learning_rate 5.0 --decay_learning_rate 0.95 --power_t 0.5 --initial_t 0 --l1 1e-8 --l2 1e-8 --port 26542 --pid_file /tmp/vw.pid