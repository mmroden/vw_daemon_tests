from environment import start_vw, VAGRANT_TEST_MODEL, check_remote_file
import os


@given(u'a simple running vw daemon that can save models')
def step_impl(context):
    saving_vw = "vw -f {} --save_resume --daemon".format(VAGRANT_TEST_MODEL)
    start_vw(saving_vw)


@when(u'a save command is sent')
def step_impl(context):
    context.sock.send("save\n")


@then(u'a model is saved')
def step_impl(context):
    from time import sleep
    sleep(2)
    remote_check = check_remote_file(VAGRANT_TEST_MODEL)
    print (remote_check)
    assert remote_check == VAGRANT_TEST_MODEL
    

@when(u'two save commands are sent in rapid succession')
def step_impl(context):
    context.sock.send("save\n")
    context.sock.send("save\n")

