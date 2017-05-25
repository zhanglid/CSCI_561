import sys
lines=[]
intline=[]
model={'A':None,'B':None}
with open(sys.argv[2]) as f:
    lines.extend(f.read().splitlines())
def modelbased(location,status):
	model[location]=status
	if model['A']==model['B']=='Clean':
		return 'NoOp'
	elif status == 'Dirty':
		return 'Suck' 
	elif location == 'A':
		return 'Right' 
	elif location == 'B':
		return 'Left'
fo= open("trace_actions_modelbased.txt", "wb")
for line in lines:
	splits=line.split(',')
	status=splits[1]
	location=splits[0]
	action=modelbased(location,status)
	fo.write(action)
	fo.write('\n')