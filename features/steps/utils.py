from environment import TEST_FILES


def read_everything(socket):
    old_timeout = socket.gettimeout()
    socket.settimeout(0.1)
    buffering = True
    while buffering:
        try:
            more = socket.recv(8192)
            if not more:
                buffering = False
        except:
            buffering = False
    socket.settimeout(old_timeout)


def write_output_lines(socket, open_file):
    buffering = True
    while buffering:
        try:
            results = socket.recv(1024)
            if not results:
                buffering = False
            while not results.endswith('\n'):
                results = results + socket.recv(1024)
            for line_split in results.split('\n'):
                if len(line_split.split(' ')) > 1:
                    open_file.write(line_split + '\n')
        except:
            buffering = False


def send_data_ignore_output(context,
                            training_file='data/train-examples.txt'):
    with open(training_file) as input_data:
        count = 0
        for line in input_data.readlines():
            context.sock.send(line + '\n')  # have to end in \n to be processed
            count += 1
            if count % 10000 == 0:
                read_everything(context.sock)
    read_everything(context.sock)


def save_training_output(context,
                         current_test_results=TEST_FILES[0],
                         training_data='data/additional-examples.txt'):
    with open(current_test_results, 'w') as output:
        with open(training_data) as input:
            count = 0
            for line in input.readlines():
                context.sock.send(line + '\n')
                count += 1
                if count % 10000 == 0:
                    write_output_lines(context.sock, output)
        write_output_lines(context.sock, output)


def compare_two_test_results(result1, result2):
    try:
        with open(result2, 'r') as output:
            with open(result1, 'r') as canonical:
                for output_line in output.readlines():
                    canonical_line = canonical.readline()
                    output_split = output_line.split(' ')
                    canonical_split = canonical_line.split(' ')
                    print ("output: ", output_split[0], " canonical: ", canonical_split[0])
                    assert abs(float(output_split[0]) - float(canonical_split[0])) < 0.001
                    assert output_split[1] == canonical_split[1]
    finally:
        # os.remove('output-data.txt')
        pass
