import multiprocessing as mp
import random
import string
import timeit

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

def randnumstr_parallel(num=1000000):
    pool = mp.Pool(processes=mp.cpu_count()+2)
    nums = pool.map(random.random, ())
    strs = pool.map(gen_rand_string, (5,)*num)
    ret = zip(nums, strs)
    ret.sort()
    return

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

def f(x):
    return x*x

if __name__ == '__main__':
    print "Regular:", timeit.timeit(randnumstr_reg, number=1)
    print "Parallel:", timeit.timeit(randnumstr_parallel, number=1)
