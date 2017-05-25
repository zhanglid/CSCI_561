"""This is the code for simple reflex agent
course: csci561
author: zhangliang dong, jiajun xu
id: 7086935462, 9467402560
email: zhanglid@usc.edu, jiajunx@usc.edu
"""

import sys

def simple_relfex(track, status):
    """
    simple reflex agent
    rule:
        if status == no then move to this track
        else move to other track
    """
    if status == 'no':
        if track == '1':
            return 'move_to_1'
        else:
            return 'move_to_2'
    else:
        if track == '1':
            return 'move_to_2'
        else:
            return 'move_to_1'

if __name__ == '__main__':
    action_list = []
    with open(sys.argv[2]) as f:
        for line in f:
            track, status = line.replace('\n', '').split(',')
            action_list.append(simple_relfex(track, status))

    with open('output.txt', 'w') as f:
        for action in action_list:
            f.write(action + '\n')
