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
                read_everything(context.sock)
    read_everything(context.sock)


def read_everything(socket):
    old_timeout = socket.gettimeout()
    socket.settimeout(0.1)
    buffering = True
    while buffering:
        try:
            more = socket.recv(8192)
            if not more:
                buffering = False
        except:
            buffering = False
    socket.settimeout(old_timeout)


def write_output_lines(socket, open_file):
    buffering = True
    while buffering:
        try:
            results = socket.recv(1024)
            if not results:
                buffering = False
            while not results.endswith('\n'):
                results = results + socket.recv(1024)
            for line_split in results.split('\n'):
                if len(line_split.split(' ')) > 1:
                    open_file.write(line_split + '\n')
        except:
            buffering = False


def compare_test_results(context, test_results):
    with open('output-data.txt', 'w') as output:
        with open('data/additional-examples.txt') as input:
            count = 0
            for line in input.readlines():
                context.sock.send(line + '\n')
                count = count + 1
                if count % 1000 == 0:
                    write_output_lines(context.sock, output)
        write_output_lines(context.sock, output)
    
    try:
        with open('output-data.txt', 'r') as output:
            with open(test_results, 'r') as canonical:
                for output_line in output.readlines():
                    canonical_line = canonical.readline()
                    output_split = output_line.split(' ')
                    canonical_split = canonical_line.split(' ')
                    # print ("output: ", output_split[0], " canonical: ", canonical_split[0])
                    assert abs(float(output_split[0]) - float(canonical_split[0])) < 0.2
                    assert output_split[1] == canonical_split[1]
    finally:
        # os.remove('output-data.txt')
        pass


@then(u'the model is identical to the previously saved non-regularized model')
def step_impl(context):
    compare_test_results(context, 'data/additional-examples-no-regularization.txt')


@then(u'the model is identical to the previously saved regularized model')
def step_impl(context):
    compare_test_results(context, 'data/additional-examples-regularization.txt')
