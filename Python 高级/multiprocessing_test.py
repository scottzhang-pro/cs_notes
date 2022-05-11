from multiprocessing import Manager

def producer(pipe):
    pipe.send('scott')

def consumer(pipe):
    data = pipe.recv()
    print(data)

if __name__ == '__main__':
    share_var = Manager().dict
    share_var = Manager().Array
    share_var = Manager().list
    # and more