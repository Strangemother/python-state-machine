import sys
import demos

def cherry(cmds):
	from http import  cherry
	print 'Run cherry'

def http(cmds):
	cmd = cmds[0] if len(cmds) > 0 else None
	if cmd == 'cherry':
		cherry(cmds[1:])
	elif cmd == 'demo':
		print 'demo'
	else:
		print '---'
		print 'Running HTTP server'
		print '---'
		cherry(cmds[1:])

def demo(cmds):
	cmd = cmds[0] if len(cmds) > 0 else None
	if cmd == 'run' or cmd is None:
		print 'run demo'
		demos.run()

def machine(cmds):
	cmd = cmds[0] if len(cmds) > 0 else None
	if cmd == 'http':
		http(cmds[1:])
	elif cmd == 'demo':
		demo(cmds[1:])
	else:
		print ['http', 'demo']



if __name__ == '__main__':
	ar = sys.argv
	if ar[0] == 'machine':
		machine(ar[1:])
	#main()
