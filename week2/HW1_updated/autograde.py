import os
from os import listdir
import re
input_format = re.compile(r'test\d+\.txt')
file_list = listdir('./testcases2')
input_list = []

for f_name in file_list:
    if input_format.match(f_name):
        input_list.append(f_name)

total_pass = len(input_list)
for input_file_name in input_list:
    os.system('python hw1cs561s17.py -i ' + 'testcases2/' + input_file_name)
    with open('output.txt', 'r') as f:
        output = f.readline()
    with open('testcases2/' + 'solution' + input_file_name[4:input_file_name.find('.')] + '.txt','r') as f:
        right_output = f.readline()
    if output != right_output:
        print '--------------------------'
        total_pass -= 1
    	print input_file_name
    	print 'My output: ' + output
    	print 'Right output: ' + right_output
    	print output == right_output
    	print '--------------------------'
    else:
	print input_file_name + ' pass'

print 'pass/total: ' + str(total_pass) + '/' + str(len(input_list))
