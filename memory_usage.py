import os
from time import sleep
from datetime import datetime
from functools import wraps
import psutil
import multiprocessing
import csv

CSV_HEADER = ['time', 'rss', 'vrt', 'shr']
NUM_SECONDS_IN_MINUTE = 60



class MemoryUsage:
    """
        Stores and updates formatted memory status information
    """
    SINGLE_BYTE_IN_MEGABYTE = 0.000001

    def __init__(self, mem_info=None):
        """
            Create memory usage object with optional memory usage info 
            
            Parameters
            ----------
            mem_info : [float] 
                list of memory usage numbers: [rss, vrt, shr]
        """
        self._status = [-1, -1, -1]
        if mem_info:
            self.update(mem_info)
    @staticmethod
    def bytes_to_megabytes(data_in_bytes):
        """
            Converts bytes to megabytes
            
            Paramteters
            -----------
            data_in_bytes : float
            
            Returns
            -------
             : float
                converted data in megabytes
        """
        return data_in_bytes * MemoryUsage.SINGLE_BYTE_IN_MEGABYTE

    def update(self, mem_info):
        """
            Updates the stored memory status with new memory usage info
            
            Paramters
            ---------
            mem_info : [float]
                list of memory usage numbers: [rss, vrt, shr]
        """
        rss = self.bytes_to_megabytes(mem_info[0])
        vrt = self.bytes_to_megabytes(mem_info[1])
        shr = self.bytes_to_megabytes(mem_info[2])
        self._status = [datetime.now(), rss, vrt, shr]
    
    def status(self):
        """
            Gets the current memory usage information stored
            
            Returns
            -------
            _status : list
                list containing the following, with respect to order:
                    * datetime object of status
                    * rss - resident set size
                    * vrt - virtual memory size
                    * shr - shared memory size
        """
        return self._status

def record_memory_usage(pid, freq_per_min, output_csv_file):
    """
        Records memory usage to csv file

        
        Parameters
        ----------
        pid : int
            process id to record memory usage on
        freq_per_min : float
            Refer to :func:`track_memory_usage`
        output_csv_file : str
            Refer to :func:`track_memory_usage`
    """
    proc = psutil.Process()
    mem_data = MemoryUsage(proc.memory_info())
    frequency = NUM_SECONDS_IN_MINUTE / freq_per_min

    with open(output_csv_file, 'w', 0) as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(CSV_HEADER)

        mem_use = MemoryUsage()
        while True:
            mem_use.update(proc.memory_info())
            csv_writer.writerow(mem_use.status())
            sleep(frequency)

def track_memory_usage(freq_per_min, output_csv_file):
    """
        Decorator factory for tracking memory usage

        Starts a separate process to record the memory usage of the wrapped
        function's process.

        Parameters
        ----------
        freq_per_min : float
            the frequency of which to record memory usage at (per minute)
        output_csv_file : str
            the filepath to write memory usage information to

        Example
        -------
        >>> @track_memory_usage('./my_memory_usage.csv')
        ... def my_main_func():
        ...     do_something_for_some_time()
    """
    def wrapper(func):
        def wrapped(*args, **kwargs):
            pid = os.getpid()
            record_memory_process = multiprocessing.Process(
                    target=record_memory_usage,
                    args=(pid, freq_per_min, output_csv_file,))

            record_memory_process.daemon = True
            record_memory_process.start()
            
            result = func(*args, **kwargs)

            record_memory_process.terminate()

            return result
        return wrapped
    return wrapper
