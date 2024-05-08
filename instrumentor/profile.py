from function_profiler import *
import sys

if __name__ == '__main__':
    print("1.1")
    profiler = FunctionProfiler.profile("input_code/" + sys.argv[1] + ".py")
    print("1.2")
    profiler.print_fun_report()
