# pylint: skip-file
import multiprocessing

workers = multiprocessing.cpu_count() + 1
loglevel = 'info'
capture_output = True
