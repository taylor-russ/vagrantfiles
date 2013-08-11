#!/usr/bin/env python26
#
#
# Depot Cleaning Utilities
#
#
#
#
 
import os
import random
import threading
import time
import Queue
import pprint
from optparse import OptionParser
 
################################################################################
# OPTIONS
################################################################################
 
 
def create_cli_parser():
    parser = OptionParser()
    parser.add_option("-p", "--path", type="string", dest="depot_path", help="""path to depot you wish to audit""")
    parser.add_option("-d", "--depth", type="int", dest="depth", help="""how far tree depth should be""")
    parser.add_option("-c", "--count", type="int", dest="count", help="""count if using random""")
    parser.add_option("-r", "--random", action="store_true", default=False, dest="random", help="""random dirs for auditing, or everything?""")
    (options, args) = parser.parse_args()
    return (options, args)
 
   
################################################################################
# MAIN
################################################################################
 
class Threader(threading.Thread):
    def __init__(self, work_queue, function, results_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue # arguments for target functions
        self.function = function # the target
        self.results_queue = results_queue # the results from target(work)
   
    def run(self):
        while True:
            item = self.work_queue.get()
            data = self.function(item)
            if data is not None:
                self.results_queue.put(data)
            self.work_queue.task_done()
 
class Depot(object):
    def __init__(self, path, ):
        self.path = path
       
    def __start_audit_threads__(self, target):
        for i in range(self.worker_threads):
            t = Threader(self.work_queue, target, self.results_queue)
            t.setDaemon(True)
            t.start()
 
    def __choose_random__(self, count=1, max_range=255, depth=1):
        """ random subdirs under path """
        results = []
        for i in xrange(count):
            cur_path = self.path
            for i in xrange(depth):
               r_hex = "%0.2X" % random.randint(0, max_range)
                cur_path = os.path.join(cur_path, r_hex)
            results.append(cur_path)
        return results
     
    def __choose_all__(self):
        """ all subdirs under path """
       return [os.path.join(self.path, x) for x in os.listdir(self.path)]
       
    def __sizeof_fmt__(self, num):
        """ borrowed from http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
       
            used to generate human readable output
       
        """
        for x in ['bytes','KB','MB','GB']:
            if num < 1024.0 and num > -1024.0:
                return "%3.1f%s" % (num, x)
            num /= 1024.0
        return "%3.1f%s" % (num, 'TB')
     
    def __audit_worker__(self, _dir):
        """ worker function to perform the audit and return the data
       
            (dict, list of lists)
       
        """
        __sizes_ = {}
       
        
        # format
        # list of strings and tuple
        # [ date, size, (extension, path, filename) ]
        __files_ = []
 
        # start walking the target
        for root, subdirs, files in os.walk(_dir):
            # loop over each file and get the size
            for file in files:
               
                # get the data about the files
            
                full_path = os.path.join(root, file)
                #http://userprimary.net/posts/2007/11/18/ctime-in-unix-means-last-change-time-not-create-time/
 
                # filename and extension info
                file_size = os.path.getsize(full_path)
                file_extension = file.split(".")[1]
               
                # timestamp data
                file_epoch = os.path.getctime(full_path)
                created_date = time.ctime(file_epoch)
                
                # is file newer than n days ago? then skip
                n_days_ago = time.time() - 60*60*24*self.older_than
                if file_epoch > n_days_ago:
                    continue
                  
                # append/populate results
                try:
                    __sizes_[file_extension] += file_size
                except KeyError:
                    __sizes_[file_extension] = file_size
                   
                __files_.append([created_date, file_size, (file_extension, root, file)])
       
        return (__sizes_, __files_)
       
 
       
    def audit(self, random=True, count=1, max_range=255, worker_threads=2, older_than=-1, depth=1):
        """         generates the output
           
            random: audits all directories under the depot-root if false
                    if true, audits a random directory
                    
            count: determines how many random dirs are audited
           
            depth: how deep you should start looking down from (meant to be used in conjunction with random
           
            worker_threads: how many worker_threads you wish to start to process os.walk on depot subfolders
           
            max_range: can be used to specify a hex range max in int (like 64 becomes 0x40)
           
            older_than: only audits files with a os.path.ctime OLDER THAN this value. Default is off.
           
        """
        # set output variables (number of days, etc)
        self.older_than = older_than
       
        
        # set up some output methods
        self.sizes = {}         # holds k=extension, v=total_size
         
        # set number of threads
        self.worker_threads = worker_threads
       
        # create work queues
        self.work_queue = Queue.Queue()
        self.results_queue = Queue.Queue()
       
        # start the threads, put a worker on each
        self.__start_audit_threads__(target=self.__audit_worker__)
       
        # get our list of subdir targets
        audit_targets = self.__choose_random__(count, max_range, depth)
        
        if random == False:
            audit_targets = self.__choose_all__()
           
         
        print "targeting the following dirs: \n"
        print "\n".join(audit_targets)
 
        
        # put each target into a queue
        for target in audit_targets:
            self.work_queue.put(target)
           
        # wait for all the workers to return
        self.work_queue.join()
       
      
        # get and parse results
        while True:
            try:
                # get one result entry
                entry = self.results_queue.get(block=False)
               
                # only while the queue isn't empty
            except Queue.Empty:
                break
               
                # if it wasn't empty, handle it
            else:
               
                # sizes - add whatever is in the current entry to results
                # take everything already in it self.sizes, union with each entry
                self.sizes = dict( (n, self.sizes.get(n, 0) + entry[0].get(n, 0)) for n in set(self.sizes)|set(entry[0]) )            
 
                pprint.pprint(entry[1])
               
      
      
def main():
    options, args = create_cli_parser()
    # initialize a depot object with a path
    bn_depot = Depot(options.depot_path)
   
    # call audit, random hex directories, options.count of them
    # can set optional worker_threads
    # older_than - optional days threshold
    # max_range - max_range defaults to 255, use to select hex values
    bn_depot.audit(random=options.random, count=options.count, max_range=32, worker_threads=5, older_than=180, depth=options.depth)
 
    # get a dict of extensions, total file_size for that extension
    sizes = bn_depot.sizes
 
   
    for extension, total_size in bn_depot.sizes.iteritems():
        print "%s       %s" % (extension, bn_depot.__sizeof_fmt__(total_size))
         
if __name__ == "__main__":
 
    try:
        main()
    except KeyboardInterrupt:
        print "Exiting...."
    
 