# 
# iPodder engine
#

import threads
import threading
import Queue
import bisect
import time
import logging

from ipodder import hooks

log = logging.getLogger('Juice')

class PriorityQueue(Queue.Queue): 
    """Prioritised Queue, as per bisect module documentation."""
    def _put(self, item): 
        bisect.insort(self.queue, item)

    # 2 remaining methods are temporary for Python 2.4
    # compatability, just a temporary fix. Newer versions
    # of the Queue module use a collections.deque instead of
    # a list object. 
    def _init(self, maxsize):
        self.maxsize = maxsize
        self.queue = []

    def _get(self):
        return self.queue.pop(0)

class Job(threads.SelfLogger): 
    """Runnable job."""

    def __init__(self, engine, name=None): 
        """Initialise the job."""
        #assert isinstance(engine, Engine)
        threads.SelfLogger.__init__(self, tag=name)
        self.abort = False
        self.doneflag = threading.Event() # set by us when we're done
        self.engine = engine
    
    def __call__(self): 
        """Make us callable."""
        try: 
            self.run()
        except Exception, ex: 
            self.exception("Job failed with uncaught exception.")
        self.doneflag.set() # just in case someone is waiting

    def run(self): 
        """Run us. Over-ride this method!
        
        To have the engine run another job, call self.engine.addjob(job)."""
        pass

    def _stop(self): 
        """Perform any internal stopping work. Over-ride this."""
        pass

    def stop(self, wait=True): 
        """Stop the job. Don't over-ride this; use _stop instead."""
        self.info("Asked to stop. Setting flag...")
        self.abort = True
        self._stop()
        if wait: 
            self.debug("asked to shut down; waiting...")
            self.doneflag.wait()
            self.debug("shut down.")
        else: 
            self.debug("asked to shut down, but not waiting.")
    
class CurryJob(Job): 
    """Curried function job."""

    def __init__(self, engine, callable, *args, **kwargs): 
        Job.__init__(self, engine)
        self.callable = callable
        self.args = args
        self.kwargs = kwargs

    def run(self): 
        self.callable(*self.args, **self.kwargs)
            
class Engine(threads.OurThread): 
    """The Engine maintains a queue of jobs to do, and runs them."""

    def __init__(self, maxworkers=1, keepgoing=False, **kwargs):
        """Initialise the Engine. 

        maxworkers -- maximum number of concurrent worker threads.
                      If maxworkers is callable, we'll call it to 
                      get the integer every time we check to see 
                      whether we should start a new worker (max 
                      one call every tenth of a second).
        """

        threads.OurThread.__init__(self, **kwargs)
        self.queue = PriorityQueue()
        self.workers = {}
        self.__maxworkers = maxworkers
        self.hooks = hooks.HookCollection()
        self.donejobs = 0
        self.keepgoing = keepgoing # wait for new jobs if no jobs
        self.keeplaunching = True # launch new jobs
        self.stopped = threading.Event()

    def get_maxworkers(self): 
        maxworkers = self.__maxworkers
        if callable(maxworkers): 
            maxworkers = maxworkers()
        return int(maxworkers)

    maxworkers = property(fget=get_maxworkers)

    def _tick(self): 
        """Called by our_run() in the middle of the loop."""
        pass

    def our_run(self): 
        """Called by run(), in turn started in another thread by start()."""
        self.debug("Started with maxworkers=%d.", self.maxworkers)

        ticks = 0
        last_loud = time.time()
        while 1: 
            ticks += 1
            self._tick()
            isloud = (time.time() - last_loud) >= 10
            #self.debug("Crank: %d", ticks)

            self.checkworkers() # sweep out any dead workers
            
            # If we're running as many workers as we can, loop around. 
            nworkers = int(len(self.workers))
            maxworkers = self.maxworkers
            if nworkers >= maxworkers: 
                if isloud: 
                    self.debug("We have as many workers as we can support.")
                    last_loud = time.time()
                time.sleep(0.1)
                continue
            
            # Get a job and fire up a worker. 
            try: 
                priority, job = self.queue.get(True, 1)
            except Queue.Empty: 
                if isloud: 
                    self.spam("No jobs waiting; %d worker(s) live.", nworkers)
                    last_loud = time.time()
                if nworkers: 
                    continue
                else: 
                    if not self.keepgoing: 
                        break
                    else: 
                        time.sleep(0.1)
                        continue

            if not self.keeplaunching: 
                continue

            self.debug("Next job is %s", repr(job))
            worker = threads.OurThread(target = job)
            worker.setDaemon(True)
            self.workers[worker] = job
            self.hooks('doing', job)
            worker.start()

        self.debug("All jobs done. Stopped.")
        self.hooks('stopped')

    def checkworkers(self): 
        # self.debug("Checking for dead workers...")
        nworkers = len(self.workers)
        for worker in self.workers.keys(): 
            if not worker.isAlive(): 
                self.debug("Worker %s is an ex parrot.", repr(worker))
                self.donejobs += 1
                nworkers -= 1
                del self.workers[worker]
                self.hooks('done', worker.target)
                alljobs = self.donejobs + nworkers + self.queue.qsize()
                self.hooks('counter', self.donejobs, alljobs)

    def addjob(self, job, priority=1): 
        """Add a job."""
        self.spam("Adding job %s to the queue.", repr(job))
        self.queue.put((priority, job))

    def stopgoing(self): 
        """Turn off keepgoing."""
        self.keepgoing = False

    def stop(self, wait=True, timeout=0): 
        """Stop all active jobs, and halt the engine."""
        self.info("Asked to stop with %d job(s) running.",len(self.workers))
        self.keepgoing = False
        self.keeplaunching = False
        for worker, job in self.workers.items(): 
            job.stop(wait=False)
        if not wait: 
            self.warn("Not bothering to wait...")
            return
        self.info("Waiting...")
        begin = time.time()
        last = begin
        while len(self.workers): 
            # First, complain about how long it has been
            now = time.time()
            gap = now - last
            if gap > 1.0: 
                delay = now - begin
                last = now
                if timeout and delay > timeout: 
                    self.info("Giving up on %d workers after "\
                              "%.1f seconds.", 
                              len(self.workers), delay)
                    return
                else: 
                    self.info("Still waiting for %d workers "\
                               "after %.1f seconds.", 
                               len(self.workers), delay)
            # Then, sleep a little and check for dead workers
            time.sleep(0.1)
            self.checkworkers()

if __name__ == '__main__': 
    import unittest
    logging.basicConfig()
    log = logging.getLogger('Juice')
    log.setLevel(logging.DEBUG)

    class QuickJobTests(unittest.TestCase): 
        def test_create(self): 
            job = Job(None)

        def test_run(self): 
            job = Job(None)
            job()

    class SimpleTestJob(Job): 
        def __init__(self, engine, times=5): 
            Job.__init__(self, engine)
            self.times = times
        def run(self): 
            for idx in range(self.times): 
                self.debug("%d", idx)
                time.sleep(0.12)

    class JobMakingTestJob(Job):
        def __init__(self, engine, times=5): 
            Job.__init__(self, engine)
            self.times = times
        def run(self): 
            self.debug("Boo.")
            if self.times: 
                self.engine.addjob(JobMakingTestJob(self.engine, self.times - 1))

    class PeckingOrderJob(Job): 
        def __init__(self, engine, priority, state): 
            Job.__init__(self, engine, name='Snob %d'%priority)
            self.priority = priority
            self.state = state
        def run(self): 
            nextpri = self.state['nextpriority']
            assert nextpri == self.priority, nextpri
            self.state['nextpriority'] = nextpri + 1
        def __repr__(self): 
            return "Snob %d" % self.priority
                
    class EngineTests(unittest.TestCase): 
        def test_create(self): 
            engine = Engine()

        def test_run_empty(self): 
            engine = Engine()
            engine.run()

        def test_run(self): 
            job = lambda: log.info("Whee!")
            engine = Engine(maxworkers = 1)
            engine.addjob(job)
            engine.run()

        def test_run_multiple(self): 
            engine = Engine(maxworkers = 1)
            for idx in range(5): 
                engine.addjob(SimpleTestJob(engine, times=2))
            engine.run()
                
        def test_run_multithreaded(self): 
            engine = Engine(maxworkers = 3)
            for idx in range(10): 
                engine.addjob(SimpleTestJob(engine, times=idx))
            engine.run()

        def test_run_jobmaker(self): 
            engine = Engine(maxworkers = 3)
            engine.addjob(JobMakingTestJob(engine, times=10))
            engine.run()

        def test_run_priorities(self): 
            # Adds jobs to the engine in reverse order of priority. 
            # The jobs themselves are fussier than that. 
            # Remember that lower priority numbers are higher priority. 
            state = {'nextpriority': 1}
            engine = Engine(maxworkers = 1)
            for priority in range(10, 0, -1): 
                engine.addjob(PeckingOrderJob(engine, priority, state), priority=priority)
            engine.run()

    unittest.main()
