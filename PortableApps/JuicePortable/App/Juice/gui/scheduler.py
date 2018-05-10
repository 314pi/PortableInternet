import time
import random
import os
import shutil
import logging

DEFAULT_MINUTE = random.randrange(1, 59)
DEFAULT_RUN_TIMES = [x + ":" + "%02d" % DEFAULT_MINUTE for x in ["4","10","16"]]
DEFAULT_RUN_TIMES_ENABLE = ["0","0","0"]
DEFAULT_ENABLE_AUTO = "off"
DEFAULT_RUN_MODE = "specific"
DEFAULT_INTERVAL_HOURS = 12.0
DEFAULT_STARTING_AT = "00:" + "%02d" % DEFAULT_MINUTE

CONFIG_OPTS = ['sched_runTimes', \
               'sched_runTimesEnable', \
               'sched_defaultMinute', \
               'sched_runMode', \
               'sched_enableAuto', \
               'sched_intervalHours', \
               'sched_startingAt']

log = logging.getLogger('Juice')

def have_config(config):
    for opt in CONFIG_OPTS:
        #If any of the config opts are None, we're uninitialized.
        if not hasattr(config,opt) or getattr(config,opt) == None:
            return False
    return True

def copy_config(source, target):
    """Assigns attributes to a target object from a source dictionary."""
    for opt in CONFIG_OPTS:
        setattr(target,opt,source[opt])

def fresh_config(scheduleFile):
    """Returns a dictionary with a fresh set of scheduler options,
    potentially setting them from a deprecated schedule.txt file."""
    
    #defaults
    config = {
        "sched_runTimes" : DEFAULT_RUN_TIMES,
        "sched_runTimesEnable" : [int(x) for x in DEFAULT_RUN_TIMES_ENABLE],
        "sched_defaultMinute" : DEFAULT_MINUTE,
        "sched_runMode" : DEFAULT_RUN_MODE,
        "sched_enableAuto" : DEFAULT_ENABLE_AUTO,
        "sched_intervalHours" : DEFAULT_INTERVAL_HOURS,
        "sched_startingAt" : DEFAULT_STARTING_AT
    }
    
    if scheduleFile and os.path.exists(scheduleFile):
        log.info("fresh_config: Found schedule file at %s.  Attempting to load schedule settings from it." % scheduleFile)
        try:
            pf = open(scheduleFile,"r")
            for l in pf:
                #print (l.strip()).split("=")
                (key,val) = (l.strip()).split("=")
                (valid,typed_val) = opt_from_string("sched_%s" % key,val)
                if valid:
                    config["sched_%s" % key] = typed_val
        finally:
            pf.close()

        #Ensure runTimesEnable mask is big enough
        while len(config["sched_runTimesEnable"]) < len(config["sched_runTimes"]):
            config["sched_runTimesEnable"].append(0)

    return config

def ensure_config(config,scheduleFile=None):
    """Ensure that the config object has all the needed scheduler options,
    generating a fresh set if config does not have everything it needs,
    possibly drawing options from scheduleFile if it exists.  Returns
    True if we set a fresh config, False otherwise."""
    if not have_config(config):
        log.info("ensure_config: Don't have a complete scheduler config, getting a fresh one.")
        copy_config(fresh_config(scheduleFile),config)
        return True

    return False

def opt_from_string(key, val):
    """Returns a two-tuple containing (valid,value)."""
    if key == "sched_runTimes":
        return (True,(val.strip('"')).split(","))
    elif key == "sched_defaultMinute":
        return (True,int(val))
    elif key == "sched_runMode" and (val in ["specific","regular"]):
        return (True,val)
    elif key == "sched_enableAuto" and (val in ["on","off"]):
        return (True,val)
    elif key == "sched_intervalHours":
        return (True,float(val))
    elif key == "sched_runTimesEnable":
        return (True,[int(x) for x in (val.strip('"')).split(",")])
    elif key == "sched_startingAt":
        return (True,val)
    return (False,None)

class Scheduler:

    def __init__(self,sc):
        self.config = sc
        self.scheduledRuns = []
        self.lastRun = -1
        self.lastCheck = 0

    def secondsSinceMidnight(self,timeStruct):
        return (timeStruct.tm_hour*3600) + (timeStruct.tm_min*60) + timeStruct.tm_sec


    def stringTimeToSeconds(self,stringTime):
        timeParts = stringTime.split(":")
        hour = int(timeParts[0])
        min = int(timeParts[1])

        return (hour*3600) + (min*60)

    def initScheduledRuns(self):
        self.scheduledRuns = []
        if self.config.sched_runMode == "specific":
            for i in range(len(self.config.sched_runTimes)):
                if self.config.sched_runTimesEnable[i] == 1:
                    self.scheduledRuns.append(self.stringTimeToSeconds(self.config.sched_runTimes[i]))
        elif self.config.sched_runMode == "regular":
            for x in range(self.stringTimeToSeconds(self.config.sched_startingAt),86400,int(self.config.sched_intervalHours*3600)):
                self.scheduledRuns.append(x)
        self.scheduledRuns.sort()
        #print self.scheduledRuns
        #print time.asctime(self.getNextRun())

    #Return True if we should run, false otherwise
    def checkTimeToRun(self):
        if len(self.scheduledRuns) == 0:
            self.initScheduledRuns()
        if len(self.scheduledRuns) == 0:
            #Nothing to do.
            return False

        result = False

        now = self.secondsSinceMidnight(time.localtime())

        if self.lastRun == -1:
            #First sweep after startup; don't run
            self.lastRun = now
            result = False
        else:
            if self.lastRun > now:
                #The last run was yesterday.
                if self.scheduledRuns[-1] > self.lastRun:
                    result = True
            else:
                #The last run was today.
                for testTime in self.scheduledRuns:
                    if testTime > self.lastRun and testTime <= now:
                        result = True

        if self.lastCheck > now:
            #Last check was yesterday.  We must reset lastRun for our own
            #internal accounting, regardless of the result.
            self.lastRun = 0

        self.lastCheck = now

        return result

    def logLastRun(self):
        self.lastRun = self.secondsSinceMidnight(time.localtime())

    def getNextRun(self):

        if len(self.scheduledRuns) == 0:
            return None
        
        now = self.secondsSinceMidnight(time.localtime())

        if now < self.scheduledRuns[-1]:
            #next run is today
            x = time.localtime()
            midnight = time.mktime((x[0],x[1],x[2],0,0,0,0,0,x[8]))
            for secondsSinceMidnight in self.scheduledRuns:
                if secondsSinceMidnight > now:
                    return time.localtime(midnight+secondsSinceMidnight)
        else:
            #next run is tomorrow
            x = time.localtime(time.time()+86400)
            midnight = time.mktime((x[0],x[1],x[2],0,0,0,0,0,x[8]))
            return time.localtime(midnight+self.scheduledRuns[0])

if __name__ == '__main__':
    class bag:
        def __str__(self):
            return ",".join(["%s = %s" % (attr,getattr(self,attr)) for attr in CONFIG_OPTS])
    logging.basicConfig()
    log.setLevel(logging.DEBUG)
    log.info("Test 1, empty config, no schedule File.")
    config = bag()
    result = ensure_config(config)
    log.info("ensure returns %s" % str(result))
    log.info("config object is now: %s" % str(config))
    log.info("Test 2, empty config, scheduler file.")
    config = bag()
    # TODO: make this a little less Andrew-specific. :) 
    result = ensure_config(config,r'C:\Documents and Settings\aegrumet\Application Data\iPodder\schedule.txt')
    log.info("ensure returns %s" % str(result))
    log.info("config object is now: %s" % str(config))
    log.info("Test 3, full config, no scheduler file.")
    config = bag()
    config.sched_startingAt = '00:41'
    config.sched_runTimes = ['04:05','16:37', '10:11']
    config.sched_runMode = 'specific'
    config.sched_runTimesEnable = [1, 1, 1]
    config.sched_defaultMinute = 49
    config.sched_intervalHours = 2.0
    config.sched_enableAuto =  'on'    
    result = ensure_config(config)
    log.info("ensure returns %s" % str(result))
    log.info("config object is now: %s" % str(config))    
    log.info("Test 4, partial config, no scheduler file.")
    config.sched_startingAt = None
    result = ensure_config(config)
    log.info("ensure returns %s" % str(result))
    log.info("config object is now: %s" % str(config))
