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
        self.frequency += 1

    def add_result(self, args, result):

        print("add_result")
        """Añadir el resultado de una llamada con los argumentos dados"""

        print("self results "+ str(self.results))
        args_tuple = tuple(args)
        if args_tuple in self.results:
            if self.results[args_tuple] != result:
                self.cacheable = False  
        else:
            self.results[args_tuple] = result

                # Si hay más de una combinación de argumentos, marca la función como no cacheable
        if len(self.results) > 1:
            print(f"{self.functionName} es llamada con múltiples combinaciones de argumentos")
            self.cacheable = False

        # Si todos los resultados son `None`, no es cacheable
        # if all(val is None for val in self.results.values()):
        #     self.cacheable = False

    def add_internal_call(self, func_name):
        """Identificamos si la función hace llamadas internas a otras funciones.    """
        print("add_internal_call")
        print("agrammos " + str(func_name) + " a internal_calls que realizo")
        self.internal_calls.add(func_name)

    # def evaluate_cacheable(self, all_records):
    #     """Evaluar si esta función es cacheable dependiendo de las funciones que llama internamente"""


    #     print("\n evaluate_cacheable")
    #     print("evaluate_cacheable " + str(self.functionName))
    #     print("internal_calls" + str(self.internal_calls))
    #     if not self.internal_calls:
    #         print("No hay llamadas internas")
    #         return None

    #     # Verificar si alguna llamada interna es cacheable
    #     #self.cacheable = False
    #     for func_name in self.internal_calls:
    #         print("llamdas intenas a " + str(func_name))
    #         if func_name in all_records:
    #             print("func_name in all_records")
    #         if all_records[func_name].cacheable:
    #             print("all_records[func_name].cacheable")
    #         if all_records[func_name].results:
    #             print("all_records[func_name].results")
    #         if func_name in all_records and all_records[func_name].cacheable and all_records[func_name].results:
    #             print(str(func_name) + " es cacheable entonces " + str(self.functionName) + " tambien lo es")
    #             self.cacheable = True
    #             break


    def is_cacheable(self):
        return self.cacheable
        
    def print_report(self):
        cacheable_str = '1' if self.cacheable else '0'
        print("{:<30} {:<10} {:<10} {}".format(self.functionName, self.frequency, cacheable_str, self.callers))

    def __eq__(self, other):
        if isinstance(other, FunctionRecord):
            return self.functionName == other.functionName and self.frequency == other.frequency and self.isCacheable() == other.isCacheable() and self.callers == other.callers
        return False

    @classmethod
    def new_instance_with(cls, funName, frequency, cacheable, callers):
        instance = cls(funName)
        instance.frequency = frequency
        instance.cacheable = cacheable
        instance.callers = callers
        return instance