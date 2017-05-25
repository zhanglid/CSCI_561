import sys
lines=[]
intline=[]
with open(sys.argv[2]) as f:
    lines.extend(f.read().splitlines())
def reflex(location,status):
	if status == 'Dirty':
		return 'Suck' 
	elif location == 'A':
		return 'Right' 
	elif location == 'B':
		return 'Left'
fo= open("trace_actions_simplereflex.txt", "wb")
for line in lines:
	splits=line.split(',')
	status=splits[1]
	location=splits[0]
	action=reflex(location,status)
	fo.write(action)
	fo.write('\n')