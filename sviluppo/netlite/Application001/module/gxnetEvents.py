from threading import Event, Thread
import time

class MyEvent():
	NONE = "0"
	CLICK = "1"
	KEY_DOWN = "2"
	KEY_UP = "3"
	DESTROY = "4"

	def __init__(self):
		self.event = Event()
		self.event_type = MyEvent.NONE
	def is_set(self):
		return self.event.is_set()
	def set(self, event_type):
		self.event_type = event_type
		return self.event.set()
	def wait(self, timeout = 0):
		self.event.wait(timeout)
		return self.event_type
	def clear(self):
		self.event_type = MyEvent.NONE
		return self.event.clear()

class MyThread(Thread):
	def __init__(self, event_handler):
		Thread.__init__(self)
		self.event_handler = event_handler
	def run(self):
		while 1:
			event_type = self.event_handler.wait()
			self.event_handler.clear()
			if (event_type != "0"):
				print("received :" + event_type +'\n')
				

#e = MyEvent()
#t = MyThread(e)
#t.start()

#while 1:
#	print("\n")
	#print("1. Click")
	#print("2. Key Down")
	#print("3. Key Up")
	#print("4. Destroy")
	#print("\n>> "),
	#event_type = input()
	#event_type = event_type

#	e.set(event_type)	

	#if(event_type == MyEvent.DESTROY):
#		break

#t.join()