from multiprocessing import Process

class CommEdison(Process):

  def __init__(self):
    from mraa import I2c
    i2c = I2c(1)
    i2c.address(0x77)


  def run(self):
    print('Edison run')