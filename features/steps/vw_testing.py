import socket
from time import sleep
from environment import start_vw


@given(u'a simple running vw daemon')
def step_impl(context):
    simple_vw_start = "/vagrant/scripts/start_vw_daemon.sh"  # "vw --daemon --port 26542"
    start_vw(simple_vw_start)


@given(u'a connection to the remote vw daemon')
def step_impl(context):
    # parse the .ssh.config file to get the hostname
    with open('.ssh.config', 'r') as ssh_config:
        ssh_read = ssh_config.read()
        ip_address = ssh_read.split('\n')[1].split(' ')[3]
        context.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context.sock.connect((ip_address, 26542))
        context.sock.settimeout(2)  # 2 seconds is probably pretty long
        print ('Vagrant ip address: ', ip_address)


@when(u'training data is provided')
def step_impl(context):
    # following the example on https://github.com/JohnLangford/vowpal_wabbit/wiki/daemon-example
    for i in xrange(20):
        try:
            context.sock.send('0 example0| a b c\n')
            context.sock.send('1 example1| x y z\n')
            context.sock.recv(2048)  # flushing
        except:
            pass  # don't do anything if we get nothing back, that's not really a problem


@when(u'testing data is sent')
def step_impl(context):
    context.sock.sendall(' abc-example| a b c\n')


@then(u'the remote cluster responds appropriately')
def step_impl(context):
    reply = context.sock.recv(1000)
    print ('Reply: ', reply)
    reply_split = reply.split('\n')
    print (reply_split)
    assert reply_split[len(reply_split)-2] == "0.000000 abc-example"
