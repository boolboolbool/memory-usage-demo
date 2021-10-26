# memory usage tracking demo module

memory_usage is a mini module demo containing a decorator for recording program
memory usage. This was whipped up for python 2.

For python 3 programs, we can use the @profile decorator from `memory_profiler`, see https://pypi.org/project/memory-profiler/#line-by-line-memory-usage


## Installation
No need for any package manager, a simple copy paste of the module file
contents `memory_usage.py` or clone of this git repository will do.


## Usage
Wrap this decorator around your main program entrypoint function definition.

``` python
from memory_usage import track_memory_usage

# record memory usage every 30 seconds
@track_memory_usage(freq_per_min=0.5, './my_memory_usage.csv')
def my_main_entrypoint()
    do_something_time_and_memory_consuming()

# creates csv file containing memory records
```

## Limitations
This module/decorator is not for use of tracking individual function memory usage, it will start recording the memory usage of whole process that the function is called from.

Nor does it handle cases where a program works with multiproessing, i.e. creating separate independent processes. It will not track the memory usage in those processes.

## Implementation Idea
Import the module and use the decorator to wrap the entrypoint function of a
program, providing decoratora rguments `(freq_per_minte, output_csv_path)`, and
it will:
 1. Get the current `process` for recording memory usage
 1. Start a separate independent process with `multiprocessing` right before program
    entrypoint executes
 1. Separate process records memory usage via `psutil` (**rss**, **vrt**,
   **shr** like with unix `top` monitoring tool)
 1. Output to a **csv** file

## Resources for learning/understanding this implementation
 - About `psutil` memory info: [psutil.Process.memory_info](https://psutil.readthedocs.io/en/latest/index.html#psutil.Process.memory_info)
- About `htop` monitoring: [understanding and using htop to monitor system resources](https://www.deonsworld.co.za/2012/12/20/understanding-and-using-htop-monitor-system-resources/)
- [Different ways to get memory consumption in python or lessons learned from memory_profiler](http://fa.bianp.net/blog/2013/different-ways-to-get-memory-consumption-or-lessons-learned-from-memory_profiler/)
- Implement python decorator factory for decorator args: [decorator factory how to pass arguments to decorators](https://dev.to/rohitsanj/decorator-factory-how-to-pass-arguments-to-decorators-3a19)
