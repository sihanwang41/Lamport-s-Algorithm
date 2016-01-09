import sys
import threading
import Queue
import socket
from collections import defaultdict

tid = None
port = None
timer = 1
task_queue = Queue.Queue(maxsize = 10)

multicast_list = None
message_ack = {}
class Message:
	def __init__(self, tid, mtype, content):
		self.id = None
		self.content = ''
		self.time_issued = None
		self.tid = tid
		self.type = mtype

	def time_generate(self):
		global timer
		self.time_issued = str(timer+1)+'.'+str(tid)


def encrypt(message):
	return '#'.join([message.time_issued, message.type, message.content])

def decrypt():
	pass

def need_to_send():
	pass

def broadcast(message):
	message.time_generate()
	str_message = encrypt(message)
	message_ack[message.time_issued] = 0
	sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	for port in multicast_list:
		sendSocket.sendto(str_message,('127.0.0.1', int(port)))

def handleInput(input_message):
	message = Message(tid, 'M', input_message)
	broadcast(message)
def do_listening():
	listenSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	listenSocket.bind(('', int(port)))
	message, clientAddress = listenSocket.recvfrom(2048)	

def main():
	global tid
	global port
	global multicast_list
	tid = sys.argv[1]
	port = sys.argv[2]
	print 'Tid: %s Port: %s\n' %(tid, port)
	
	multicast_list = sys.argv[3].split(':')
	print sys.argv[3]
	print ' '.join(multicast_list)

	listenThread = threading.Thread(target = do_listening);
	listenThread.daemon = True
	listenThread.start()

	while True:
		clientInput = raw_input("\r>")
		worker = threading.Thread(target=handleInput, args=(clientInput,))
		worker.daemon = True
		worker.start()

if __name__ == '__main__':
	main()