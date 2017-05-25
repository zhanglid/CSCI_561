"""This is the code for goal based agent
course: csci561
author: zhangliang dong, jiajun xu
id: 7086935462, 9467402560
email: zhanglid@usc.edu, jiajunx@usc.edu
"""
import sys

def goal_based(track, status):
    global model
    model[track] = status

    if model['1'] == 'yes' and model['2'] == 'yes':
        return 'keep' # meet the goal, no need to move
    else:
        if model['1'] == 'no':
            return 'move_to_1' # track 1 is avaliable
        elif model['2'] == 'no':
            return 'move_to_2'# track 2 is avaliable
        elif model['1'] == None:
            return 'move_to_1'
        elif model['2'] == None:
            return 'move_to_2'
        else:
            return 'keep' # we have none in the model, need to wait for more info

if __name__ == '__main__':
    action_list = []

    # init the model
    model = {'1':None, '2':None}
    with open(sys.argv[2]) as f:
        for line in f:
            track, status = line.replace('\n', '').split(',')
            action_list.append(goal_based(track, status))

    # print action_list
    with open('output.txt', 'w') as f:
        for action in action_list:
            f.write(action + '\n')
