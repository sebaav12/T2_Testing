class FunctionRecord:
    def __init__(self, funName):
        self.functionName = funName
        self.frequency = 0
        self.cacheable = True
        self.callers =  []
        self.results = {} 
        self.internal_calls = set()

    # Almacena el nombre de la función que llama a esta función
    def add_caller(self, caller_name):
        if caller_name and caller_name not in self.callers:
            self.callers.append(caller_name)

    def increase_frequency(self):
        self.frequency += 1

    def add_result(self, args, result): 
        args_tuple = tuple(args)

        if args_tuple in self.results:
            if self.results[args_tuple] != result:
                self.cacheable = False        
        else:
            self.results[args_tuple] = result
 
        # Si hay más de una combinación de argumentos, no es cacheable
        if len(self.results) > 1:
            self.cacheable = False

    def add_internal_call(self, func_name):
        print("agrammos " + str(func_name) + " a internal_calls que realizo")
        self.internal_calls.add(func_name)
 
    def is_cacheable(self):
        print("is_cacheable")
        return self.cacheable
        
    def print_report(self):
        cacheable_str = '1' if self.cacheable else '0'
        print("{:<30} {:<10} {:<10} {}".format(self.functionName, self.frequency, cacheable_str, self.callers))

    def __eq__(self, other):
        if isinstance(other, FunctionRecord):
            print("__eq__")
            return self.functionName == other.functionName and self.frequency == other.frequency and self.isCacheable() == other.isCacheable() and self.callers == other.callers
        return False

    @classmethod
    def new_instance_with(cls, funName, frequency, cacheable, callers):
        instance = cls(funName)
        instance.frequency = frequency
        instance.cacheable = cacheable
        instance.callers = callers
        return instance