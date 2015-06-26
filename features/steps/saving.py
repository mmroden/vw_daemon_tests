from environment import stop_vw
from utils import (save_training_output,
                   compare_test_results,
                   send_data_ignore_output)
import os


@given(u'a vw daemon running that has no decay learning rate')
def step_impl(context):
    start_vw("/vagrant/scripts/start_vw_daemon_save_broken.sh")


@when(u'more training data is provided and results are saved to a file')
def step_impl(context):
    context.output_file_1 = "output-data-1.txt"
    if os.path.exists(context.output_file_1):
        os.remove(context.output_file_1)
    save_training_output(context, context.output_file_1)


@when(u'the vw daemon is killed')
def step_impl(context):
    stop_vw()


@when(u'initial training data is provided')
def step_impl(context):
    send_data_ignore_output(context)


@then(u'there is no difference between the saved outputs')
def step_impl(context):
    compare_test_results(context, context.output_file_1)
