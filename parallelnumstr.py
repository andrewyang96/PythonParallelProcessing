import multiprocessing as mp
import logging, sys
import random
import string
import timeit
from functools import partial

import platform
def print_sysinfo():
    print '\nPython version  :', platform.python_version()
    print 'compiler        :', platform.python_compiler()

    print '\nsystem     :', platform.system()
    print 'release    :', platform.release()
    print 'machine    :', platform.machine()
    print 'processor  :', platform.processor()
    print 'CPU count  :', mp.cpu_count()
    print 'interpreter:', platform.architecture()[0]
    print

def gen_rand_string(length):
    return ''.join(random.choice(
                    string.ascii_lowercase
                    + string.ascii_uppercase
                    + string.digits)
                   for i in xrange(length))

def rand_str_worker(q, length, num):
    for n in xrange(num):
        q.put(gen_rand_string(length))

def rand_num_worker(q, num):
    for n in xrange(num):
        q.put(random.random())

# Uses processes for parallel processing.
def randnumstr_parallel(num=1000000):
    qnums = mp.Queue()
    pnums = mp.Process(target=rand_str_worker, args=(qnums,5,num))
    pnums.start()
    
    qstrs = mp.Queue()
    pstrs = mp.Process(target=rand_num_worker, args=(qstrs,num))
    pstrs.start()
    
    pnums.join()
    pstrs.join()

    nums = []
    while not qnums.empty():
        nums.append(qnums.get())
    qnums.close()
    
    strs = []
    while not qstrs.empty():
        strs.append(qstrs.get())
    qstrs.close()
    
    ret = zip(nums, strs)
    ret.sort()
    return ret

def randnumstr_reg(num=1000000):
    # Generate random numbers
    nums = []
    for n in xrange(num):
        nums.append(random.random())
    # Generate random strings
    strs = []
    for n in xrange(num):
        strs.append(gen_rand_string(5))
    ret = zip(nums, strs)
    ret.sort()
    return

if __name__ == "__main__":
    mp.log_to_stderr(logging.DEBUG)
    ret = randnumstr_parallel(600) # times out after 600
    # Hypothesis: queue probably gets too full.
