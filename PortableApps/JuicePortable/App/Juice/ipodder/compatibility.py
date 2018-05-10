# Various helper code for compatibility with versions of iPodder.

import logging
import os, sys

log = logging.getLogger('Juice')

def migrate_2x_tmp_downloads(basepath,state):

    result = []

    try:
        encinfolist = []
        try:
            encinfolist = state['tmp_downloads']
            log.info("Detected post-2.1 developer tmp_downloads")
        except ImportError:
            #This path should not be part of a zip file.
            path = os.path.join(basepath,"compat","2x")
            sys.path.append(path)
            encinfolist = state['tmp_downloads']
            sys.path.remove(path)
            log.info("Detected release 2.1 tmp_downloads")

        from ipodder.core import Enclosure
        for i in range(len(encinfolist)):
            encinfo = encinfolist[i]
            try:
                (is_present,filename) = encinfo.feed.get_target_status(encinfo)
                compatible_enclosure = Enclosure(
                    None, \
                    encinfo.url, \
                    encinfo.feed, \
                    encinfo.length, \
                    encinfo.marked, \
                    encinfo.item_title, \
                    encinfo.description, \
                    encinfo.item_link, \
                    filename = filename)
                compatible_enclosure.status = encinfo.status
                compatible_enclosure.creation_time = encinfo.creation_time
                compatible_enclosure.download_started = encinfo.download_started
                compatible_enclosure.download_completed = encinfo.download_completed
                result.append(compatible_enclosure)
            except:
                log.exception("Error migrating 2x-style tmp_downloads entry %d." % i)
                pass
        #Now save the fruits of our labor.
        state['latest_downloads'] = result
        state.sync()
    except:
        log.exception("Error migrating 2x-style tmp_downloads.")
        pass

    return result
