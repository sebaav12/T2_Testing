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
        print("add_caller")
        if caller_name and caller_name not in self.callers:
            self.callers.append(caller_name)

    def increase_frequency(self):
        print("increase_frequency")
        self.frequency += 1

    def add_result(self, args, result):
        print("add_result")
 
        args_tuple = tuple(args)

        print("Registrando resultado de " + str(self.functionName) + 
      " con args " + str(args_tuple[0]) + ": " + str(result))
        
        print("resultssssss")
        print(self.results)

        if args_tuple in self.results:
            if self.results[args_tuple] != result:
                self.cacheable = False  
            print("a")
        else:
            self.results[args_tuple] = result
            print("b")

        print("c")

        # Si hay más de una combinación de argumentos, no es cacheable
        if len(self.results) > 1:
            print(f"{self.functionName} es llamada con múltiples combinaciones de argumentos")
            self.cacheable = False

        print("temino de add results")

    def add_internal_call(self, func_name):
        """Identificamos si la función hace llamadas internas a otras funciones.    """
        print("add_internal_call")
        print("agrammos " + str(func_name) + " a internal_calls que realizo")
        self.internal_calls.add(func_name)
 
    def is_cacheable(self):
        print("is_cacheable")
        return self.cacheable
        
    def print_report(self):
        #print("print_report")
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