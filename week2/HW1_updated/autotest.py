import os
from os import listdir

file_list = listdir('./testcases')
input_list = []
for f_name in file_list:
    if f_name == 'output.txt':
        os.system('rm testcases/output.txt')
    if f_name.find('txt') and f_name.find('_') < 0:
        input_list.append(f_name)

for input_file_name in input_list:
    print input_file_name
    os.system('python hw1cs561s17.py -i ' + 'testcases/' + input_file_name)
    with open('output.txt', 'r') as f:
        output = f.readline()
    with open('testcases/' + input_file_name[:input_file_name.find('.')] + '_output.txt', 'r') as f:
        right_output = f.readline()
    print output
    print right_output
    print output == right_output
    print '--------------------------'
