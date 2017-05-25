"""This is the code for model based agent
course: csci561
author: zhangliang dong, jiajun xu
id: 7086935462, 9467402560
email: zhanglid@usc.edu, jiajunx@usc.edu
"""

import sys

def model_based(track, status):
    """
    We record the status of two tracks to decide which action to take.
    If first track is no, we move to first track.
    Else if second track is no, we move to second track.
    If both tracks are yes, we keep.
    """
    global model

    # update model
    model[track] = status

    # decide the aciton
    if model['1'] == 'no':
        return 'move_to_1'
    elif model['2'] == 'no':
        return 'move_to_2'
    elif model['1'] == None:   # if track 1 is unkown, it is worth to try
        return 'move_to_1'
    elif model['2'] == None:   # if track 2 is unkown, it is worth to try
        return 'move_to_2'
    else:
        return 'keep'


if __name__ == '__main__':
    action_list = []

    # init the model
    model = {'1':None, '2':None}
    with open(sys.argv[2]) as f:
        for line in f:
            track, status = line.replace('\n', '').split(',')
            action_list.append(model_based(track, status))

    # print action_list
    with open('output.txt', 'w') as f:
        for action in action_list:
            f.write(action + '\n')
