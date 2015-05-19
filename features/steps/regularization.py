import gzip
import os
from environment import start_vw, VAGRANT_TEST_MODEL
import filecmp


@given(u'a vw daemon running without regularization')
def step_impl(context):
    start_vw("/vagrant/scripts/start_vw_daemon_non_regularized.sh")


@given(u'a saved non-regularized model made in offline mode')
def step_impl(context):
    assert os.path.exists("models/offline-without-regularization.vw")


@when(u'the regularization data set is provided')
def step_impl(context):
    with gzip.open('data/train-examples.txt.gz', 'rb') as input:
        # context.sock.sendall(input.read())
        unzipped = input.read().split('\n')
        count = 0
        for line in unzipped:
            count = count + 1
            if count % 100 == 0:  # have to consume the returned messages and throw them away
                for i in xrange(0, 10):
                    returned = context.sock.recv(1024)
            context.sock.send(line + '\n')  # have to end in \n to be processed


@then(u'the model is identical to the previously saved non-regularized model')
def step_impl(context):
    print ("cwd:", os.getcwd())
    assert os.path.exists("model_test.vw")
    assert filecmp.cmp("model_test.vw", "models/offline-without-regularization.vw")
