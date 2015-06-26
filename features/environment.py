import subprocess
from time import sleep
import os


VAGRANT_TEST_MODEL="/vagrant/model_test.vw"
PID_FILE="/tmp/vw.pid"
TEST_FILES = "output-data.txt", "output-data-1.txt"


def start_vw(call_string):
    # call_string = "{} --pid_file {}".format(call_string, PID_FILE)
    # print ("VW start string: ", call_string)
    args = ['vagrant', 'ssh', '--command', call_string]
    print ("args: ", args)
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sleep(1)
    out = p.stdout.read(1024)
    print ("out: ", out)
    err = p.stderr.read(1024)
    print ("err: ", err)


def stop_vw():
    killing_vw = "sudo killall vw"
    if check_remote_file(PID_FILE):
        pid = cat_remote_file(PID_FILE)
        killing_vw = "sudo kill {}".format(pid)
        remove_remote_file(PID_FILE)
    # print ("VW kill string: ", killing_vw)
    args = ['vagrant', 'ssh', '--', killing_vw]
    p = subprocess.Popen(args)
    p.wait()


def cat_remote_file(filename):
    return manipulate_remote_file("cat", filename)


def check_remote_file(filename):
    return manipulate_remote_file("ls", filename)


def remove_remote_file(filename):
    return manipulate_remote_file("sudo rm", filename)


def manipulate_remote_file(remote_command, remote_file):
    args = ['vagrant', 'ssh', '--', remote_command, remote_file]
    try:
        results = subprocess.check_output(args).strip()
        # print ("arguments: ", args, " results: ", results)
        return results
    except:
        return None  # something broke on the other side, so rather than die, just return None


def clean_up():
    stop_vw()
    if check_remote_file(VAGRANT_TEST_MODEL):
        remove_remote_file(VAGRANT_TEST_MODEL)
    for file in TEST_FILES:
        if os.path.exists(file):
            os.remove(file)


def before_scenario(context, scenario):
    clean_up()


def after_scenario(context, scenario):
    if hasattr(context, 'sock'):
        context.sock.close()



def after_all(context):
    clean_up()
    start_vw("/vagrant/scripts/start_vw.sh")  # so that vw is running when tests are done
