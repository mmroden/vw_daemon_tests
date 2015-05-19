import gzip
import os
from environment import start_vw
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
        unzipped = input.read().split('\n')
        for line in unzipped:
            context.sock.send(line)


@then(u'the model is identical to the previously saved non-regularized model')
def step_impl(context):
    assert filecmp.cmp("/vagrant/model_test.vw", "models/offline-without-regularization.vw")
