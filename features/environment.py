import subprocess
from time import sleep


def start_vw():
    args = ['vagrant', 'ssh', '--', '"/vagrant/start_vw.sh"']
    p = subprocess.Popen(args)
    sleep(4)  # not really completion, but vw starts as a daemon and so p.wait() won't work


def stop_vw():
    args = ['vagrant', 'ssh', '--', '"/vagrant/stop_vw.sh"']
    p = subprocess.Popen(args)
    p.wait()


def before_scenario(context, scenario):
    start_vw()


def after_scenario(context, scenario):
    stop_vw()


def after_all(context):
    start_vw()
