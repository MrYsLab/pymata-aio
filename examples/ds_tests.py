from pymata_aio.pymata3 import PyMata3
import time

def the_call_back(data):
    print(data)
    # pass

board = PyMata3()

while True:
    board.sleep(.2)
    # start = time.time()
    board.get_ds_temperature(10, the_call_back)

    # elapsed = time.time()-start
    # print(elapsed)


