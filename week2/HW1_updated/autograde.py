from os import listdir
import re
input_format = re.compile(r'test\d+\.txt')
file_list = listdir('./testcases2')
input_list = []
TIME_OUT = 1
timeusedsum = 0


def timeout_command(command, timeout):
    """call shell-command and either return its output or kill it
    if it doesn't normally exit within timeout seconds and return None"""
    import subprocess, datetime, os, time, signal
    start = datetime.datetime.now()
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while process.poll() is None:
      time.sleep(0.001)
      now = datetime.datetime.now()
      if (now - start).seconds > timeout:
        os.kill(process.pid, signal.SIGKILL)
        os.waitpid(-1, os.WNOHANG)
        return None
    return (now - start).microseconds / 1000

for f_name in file_list:
    if input_format.match(f_name):
        input_list.append(f_name)

total_pass = len(input_list)
for input_file_name in input_list:
    time_used = timeout_command(['python', 'hw1cs561s17.py', '-i', 'testcases2/' + input_file_name], TIME_OUT)
    with open('testcases2/' + input_file_name, 'r') as f:
        search_type = f.readline().replace('\n', '')
    with open('output.txt', 'r') as f:
        output = f.readline()
    with open('testcases2/' + 'solution' + input_file_name[4:input_file_name.find('.')] + '.txt','r') as f:
        right_output = f.readline()
    if output != right_output:
        print '--------------------------'
        print search_type
        total_pass -= 1
        print input_file_name
        print 'My output: ' + output
        print 'Right output: ' + right_output
        if time_used:
            print output == right_output
            print str(time_used) + 'ms'
        else:
            print 'timeout'
        print '--------------------------'
    else:
        timeusedsum += time_used
        print input_file_name + ' pass in ' + str(time_used) + 'ms'

print 'pass/total: ' + str(total_pass) + '/' + str(len(input_list)) + ', avg time: ' + str(float(timeusedsum)/total_pass) + 'ms'
