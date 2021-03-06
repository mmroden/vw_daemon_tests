from utils import send_data_ignore_output, compare_two_test_results, save_training_output
import os
from environment import start_vw, VAGRANT_TEST_MODEL, TEST_FILES


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
    send_data_ignore_output(context)


@then(u'the model is identical to the previously saved non-regularized model')
def step_impl(context):
    save_training_output(context, current_test_results=TEST_FILES[0])
    compare_two_test_results(TEST_FILES[0], 'data/additional-examples-no-regularization.txt')


@then(u'the model is identical to the previously saved regularized model')
def step_impl(context):
    save_training_output(context, current_test_results=TEST_FILES[0])
    compare_two_test_results(TEST_FILES[0], 'data/additional-examples-regularization.txt')
