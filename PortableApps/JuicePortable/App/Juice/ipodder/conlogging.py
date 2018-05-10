# 
# iPodder console logging module
#
# ConsoleFormatter and ConsoleLogRecordProxy work together to alter the 
# default output format of the logging module. Current functionality 
# includes wrapping output and not bothering with a log level indicator 
# if the record has INFO level. 
#

import logging
import textwrap

class ConsoleLogRecordProxy(logging.LogRecord):
    "A LogRecord that wraps lines for console output, etc."
    
    def __init__(self, record, wrap):
        "Initialise the `WrappingLogRecordProxy`."
        self.__record = record
        self.__wrap = wrap
        
    def getMessage(self):
        "Return an adjusted version of the original record's message."
        r = self.__record
        msg = r.getMessage()
        if r.levelno != logging.INFO:
            msg = "%s: %s" % (r.levelname, msg)
        if self.__wrap: 
            msg = '\n'.join(textwrap.wrap(msg, width=78))
        return msg
    
    def __str__(self):
        "Convert this record to a string."
        return self.__record.__str__()
    
    def __getattr__(self, key):
        "Shadow attributes on the original record."
        return getattr(self.__record, key)

class ConsoleFormatter(logging.Formatter):
    """Console log formatter. 
    
    Converts records to WrappingLogRecordProxy records."""
    
    def __init__(self, *a, **kw): 
        "Initialise the `ConsoleFormatter`."
        if kw.has_key('wrap'):     # if there's a wrap= argument
            self.wrap = kw['wrap'] # steal it
            del kw['wrap']         # and delete it
        else: 
            self.wrap = False
        logging.Formatter.__init__(self, *a, **kw)
        
    def format(self, record):
        "Format a record by wrapping it."
        record = ConsoleLogRecordProxy(record, self.wrap)
        return logging.Formatter.format(self, record)
