from multiprocessing import Process
from Queue import Queue

class CommReceiver(Process):
  web_queue = Queue()
  comm_queue = Queue()

  def __init__(self):
    pass

  def run(self):
    print('Receiver run')
    print(self.web_queue, self.comm_queue)