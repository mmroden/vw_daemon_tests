import gzip
import os
from environment import start_vw, VAGRANT_TEST_MODEL
import filecmp
from time import sleep


@given(u'a vw daemon running without regularization')
def step_impl(context):
    start_vw("/vagrant/scripts/start_vw_daemon_non_regularized.sh")


@given(u'a vw daemon running with regularization')
def step_impl(context):
    start_vw("/vagrant/scripts/start_vw_daemon_regularized.sh")


@given(u'a saved regularized model made in offline mode')
def step_impl(context):
    assert os.path.exists("models/offline-with-regularization.vw")


@given(u'a saved non-regularized model made in offline mode')
def step_impl(context):
    assert os.path.exists("models/offline-without-regularization.vw")


@when(u'the regularization data set is provided')
def step_impl(context):
    with open('data/train-examples.txt') as input:
        count = 0
        for line in input.readlines():
            context.sock.send(line + '\n')  # have to end in \n to be processed
            count = count + 1
            if count % 10000 == 0:
                results = context.sock.recv(1024000)
    results = context.sock.recv(1024000)
    while not results.endswith('\n'):
        results = context.sock.recv(1024000)


def compare_test_results(context, test_results):
    with open('output-data.txt', 'w') as output:
        with open('data/additional-examples.txt') as input:
            for line in input.readlines():
                context.sock.sendall(line + '\n')
                results = ''
                with os.fdopen(context.sock.fileno(), 'r') as file_obj:
                    for read_line in file_obj.readline():
                        results = results + read_line
                print ("results: ", results)
    try:
        assert filecmp.cmp('output-data.txt', test_results)
    finally:
        # os.remove('output-data.txt')
        pass


@then(u'the model is identical to the previously saved non-regularized model')
def step_impl(context):
    compare_test_results(context, 'data/additional-examples-no-regularization.txt')


@then(u'the model is identical to the previously saved regularized model')
def step_impl(context):
    compare_test_results(context, 'data/additional-examples-regularization.txt')
