from environment import stop_vw, start_vw, TEST_FILES
from utils import (save_training_output,
                   compare_test_results,
                   send_data_ignore_output)


@given(u'a vw daemon running that has no decay learning rate')
def step_impl(context):
    if hasattr(context, 'sock'):
        context.sock.close()  # make sure there aren't any lying around, open
    start_vw("/vagrant/scripts/start_vw_daemon_save_broken.sh")


@when(u'more training data is provided and results are saved to a file')
def step_impl(context):
    save_training_output(context, current_test_results=TEST_FILES[0])  # because TEST_FILES[0] is used in utils


@when(u'the vw daemon is killed')
def step_impl(context):
    stop_vw()


@when(u'initial training data is provided')
def step_impl(context):
    send_data_ignore_output(context)


@then(u'there is no difference between the saved outputs')
def step_impl(context):
    compare_test_results(context,
                         canonical_test_results=TEST_FILES[0],
                         current_test_results=TEST_FILES[1])
