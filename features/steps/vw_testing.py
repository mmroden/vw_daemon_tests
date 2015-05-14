import socket
from time import sleep

@given(u'a connection to a remote vw cluster')
def step_impl(context):
    # parse the .ssh.config file to get the hostname
    with open('.ssh.config', 'r') as ssh_config:
        ssh_read = ssh_config.read()
        ip_address = ssh_read.split('\n')[1].split(' ')[3]
        context.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context.sock.connect((ip_address, 26542))
        print ('Vagrant ip address: ', ip_address)


@when(u'training data is provided')
def step_impl(context):
    # following the example on https://github.com/JohnLangford/vowpal_wabbit/wiki/daemon-example
    for i in xrange(20):
        context.sock.sendall('0 example0| a b c\n1 example1| x y z\n')
        sleep(0.01)
        context.sock.recv(2048)  # flushing


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
