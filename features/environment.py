import subprocess
from time import sleep
import os


VAGRANT_TEST_MODEL="/vagrant/model_test.vw"


def start_vw(call_string):
    args = ['vagrant', 'ssh', '--', call_string]
    p =subprocess.Popen(args)
    sleep(5)  # will get connection reset errors if vw isn't allowed to start up fully


def stop_vw():
    args = ['vagrant', 'ssh', '--', '"/vagrant/stop_vw.sh"']
    p = subprocess.Popen(args)
    p.wait()


def check_remote_file(filename):
    return manipulate_remote_file("ls", filename)


def remove_remote_file(filename):
    return manipulate_remote_file("rm", filename)


def manipulate_remote_file(remote_command, remote_file):
    args = ['vagrant', 'ssh', '--', remote_command, remote_file]
    try:
        results = subprocess.check_output(args).strip()
        print ("arguments: ", args, " results: ", results)
        return results
    except:
        return None  # something broke on the other side, so rather than die, just return None


def clean_up():
    stop_vw()
    if check_remote_file(VAGRANT_TEST_MODEL):
        remove_remote_file(VAGRANT_TEST_MODEL)


def before_scenario(context, scenario):
    clean_up()


def after_scenario(context, scenario):
    clean_up()


def after_all(context):
    start_vw("/vagrant/start_vw.sh")  # so that vw is running when tests are done
