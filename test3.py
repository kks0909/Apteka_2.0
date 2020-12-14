from threading import Thread
from time import sleep

a = True

def fun1c():
	while a:
		print("*")

def func2():
	while a:
		sleep(10)


def off():
	global a
	a = False

def on():
	global a
	a = True


if __name__ == "__main__":
	p2 = Thread(target=fun1c)
	p1 = Thread(target=func2)
	p1.start()
	p2.start()
	p1.join()
	p2.join()
