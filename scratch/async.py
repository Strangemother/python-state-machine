import sys
import subprocess
import random
import time
import threading
import Queue


class AsynchronousFileReader(threading.Thread):
    '''
    Helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    '''

    def __init__(self, fd, queue):
        assert isinstance(queue, Queue.Queue)
        assert callable(fd.readline)

        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queue

    def daemonize(self):

        if hasattr(os, 'fork'):
            try:
                pid = os.fork()
                if pid > 0:
                    # already exists
                    sys.exit(0)
            except OSError, e:
                sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
                sys.exit(1)
            # decouple from parent environment
            os.chdir("/")
            os.setsid()
            os.umask(0)

            # do second fork
            try:
                    pid = os.fork()
                    if pid > 0:
                            # exit from second parent
                            sys.exit(0)
            except OSError, e:
                    sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
                    sys.exit(1)

            # redirect standard file descriptors
            sys.stdout.flush()
            sys.stderr.flush()
            si = file(self.stdin, 'r')
            so = file(self.stdout, 'a+')
            se = file(self.stderr, 'a+', 0)
            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())

            # write pidfile
            atexit.register(self.delpid)
            pid = str(os.getpid())
            file(self.pidfile,'w+').write("%s\n" % pid)

    def run(self):
        '''The body of the tread: read lines and put them on the queue.'''
        for line in iter(self._fd.readline, ''):
            self._queue.put(line)

    def eof(self):
        '''Check whether there is no more content to expect.'''
        return not self.is_alive() and self._queue.empty()


class AsyncClock(threading.Thread):

    def __init__(self, queue, interval=1):
        super(AsyncClock, self).__init__()
        self.ticks = 0
        self._queue = queue
        self.running = False
        self.interval = interval

    def start(self):
        self.running = True
        super(AsyncClock, self).start()

    def run(self):
        while self.running:
            self.ticks += 1 * self.interval
            self.set_ticks()
            time.sleep(self.interval)

    def set_ticks(self):
        with self._queue.mutex:
            self._queue.queue.clear()
        self._queue.put_nowait(self.ticks)


class Clock(object):

    def __init__(self, interval=1):
        self.q = Queue.Queue()
        self.interval = interval
        self.thr = AsyncClock(self.q, self.interval)
        self._last = 0

    def start(self):
        self.thr.start()

    def stop(self):
        self.thr.running = False
        self.thr.join()

    def reset(self):
        self._last = 0

    def get_q(self):
        res = self._last
        while not self.q.empty():
            line = self.q.get()
            res = line
        self._last = res
        return res

    def get_count(self):
        self.get_q()
        return self._last

    count = property(get_count)

def consume(command):
    '''
    Example of how to consume standard output and standard error of
    a subprocess asynchronously without risk on deadlocking.
    '''

    # Launch the command as subprocess.
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Launch the asynchronous readers of the process' stdout and stderr.
    stdout_queue = Queue.Queue()
    stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
    stdout_reader.start()
    stderr_queue = Queue.Queue()
    stderr_reader = AsynchronousFileReader(process.stderr, stderr_queue)
    stderr_reader.start()

    # Check the queues if we received some output (until there is nothing more to get).
    while not stdout_reader.eof() or not stderr_reader.eof():
        # Show what we received from standard output.
        while not stdout_queue.empty():
            line = stdout_queue.get()
            print 'Received line on standard output: ' + repr(line)

        # Show what we received from standard error.
        while not stderr_queue.empty():
            line = stderr_queue.get()
            print 'Received line on standard error: ' + repr(line)

        # Sleep a bit before asking the readers again.
        time.sleep(.1)

    # Let's be tidy and join the threads we've started.
    stdout_reader.join()
    stderr_reader.join()

    # Close subprocess' file descriptors.
    process.stdout.close()
    process.stderr.close()

def produce(items=10):
    '''
    Dummy function to randomly render a couple of lines
    on standard output and standard error.
    '''
    for i in range(items):
        output = random.choice([sys.stdout, sys.stderr])
        output.write('Line %d on %s\n' % (i, output))
        output.flush()
        time.sleep(random.uniform(.1, 1))

if __name__ == '__main__':
    # The main flow:
    # if there is an command line argument 'produce', act as a producer
    # otherwise be a consumer (which launches a producer as subprocess).
    if len(sys.argv) == 2 and sys.argv[1] == 'produce':
        produce(10)
    else:
        consume(['python', sys.argv[0], 'produce'])
