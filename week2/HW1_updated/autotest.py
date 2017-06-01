import os
from os import listdir
import re
input_format = re.compile(r't\d+\.txt')
file_list = listdir('./testcases')
input_list = []

for f_name in file_list:
    if input_format.match(f_name):
        input_list.append(f_name)

total_pass = len(input_list)
for input_file_name in input_list:
    print input_file_name
    os.system('python hw1cs561s17.py -i ' + 'testcases/' + input_file_name)
    with open('output.txt', 'r') as f:
        output = f.readline()
    with open('testcases/' + input_file_name[:input_file_name.find('.')] + '_output.txt', 'r') as f:
        right_output = f.readline()
    print output
    print right_output
    if output != right_output:
        total_pass -= 1
        print '!!!!!!!!!!!!!!!!!!!!!'
    print output == right_output
    print '--------------------------'

print 'pass/total: ' + str(total_pass) + '/' + str(len(input_list))
