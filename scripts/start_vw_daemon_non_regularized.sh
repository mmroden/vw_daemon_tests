#!/bin/bash

vw --daemon --port 26542 --holdout_off --loss_function logistic --learning_rate 5.0 --decay_learning_rate 0.95 --power_t 0 --initial_t 0 -f /vagrant/model_test.vw --save_resume --pid_file /tmp/vw.pid --num_children 1