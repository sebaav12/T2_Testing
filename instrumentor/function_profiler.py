from abstract_profiler import Profiler
from function_instrumentor import *
from function_record import FunctionRecord

# Clase que rastrea y reporta las funciones que se ejecutan
class FunctionProfiler(Profiler):
    # Pila para rastrear llamadas de funciones
    call_stack = []  

    # Metodo que se llama cada vez que se ejecuta una funcion
    @classmethod
    def record_start(cls, functionName, args):
        instance = cls.getInstance()
        record = instance.get_record(functionName)
        record.increase_frequency()

        # Registrar la función desde la que se hizo la llamada
        if cls.call_stack:
            print(f"La función {cls.call_stack[-1]} llama a {functionName}")
            record.add_caller(cls.call_stack[-1])   

        print(f"Entrando a {functionName}")

        # Agrega al call_stack
        cls.call_stack.append(functionName)

        # Guarda los argumentos para usarlos en record_end (cache)
        cls.current_args = args   

    #   def record_end(cls, functionName, returnValue):
    #     cls.getInstance().fun_call_end(functionName, returnValue)
    #     return returnValue
    
    @classmethod
    def record_end(cls, functionName, returnValue):
        print(f"Saliendo de {functionName}")
        if cls.call_stack and cls.call_stack[-1] == functionName:

            # Guardar el resultado de la función para el cache
            record = cls.getInstance().get_record(functionName)

            print(" El resultdo de " +str(functionName) +" es "+ str(returnValue))
            record.add_result(cls.current_args, returnValue)

            # Eliminar la función actual de la pila para el caller
            cls.call_stack.pop()
        else:
            print(f"Error: Desbalance en la pila al salir de {functionName}")

    @classmethod
    def add_internal_call(cls, functionName):
        """Añadir una llamada interna a la función en la parte superior de la pila."""
        if cls.call_stack:
            record = cls.getInstance().get_record(cls.call_stack[-1])
            record.add_internal_call(functionName)

    # Este metodo inyecta codigo en el programa segun el visitor del profiler
    @classmethod
    def instrument(cls, ast):
        visitor = FunctionInstrumentor()
        return fix_missing_locations(visitor.visit(ast))
    
    # Metodos de instancia
    def __init__(self):
        self.records = {}

    def get_record(self, functionName):
        if functionName not in self.records:
            self.records[functionName] = FunctionRecord(functionName)
        return self.records[functionName]

    def fun_call_start(self, functionName, args):  
        record = self.get_record(functionName)

    def fun_call_end(self, functionName, returnValue):
        pass

    def evaluate_all_cacheable(self):
        print("\n evaluate_all_cacheable")
        """Evaluar si todas las funciones son cacheables."""
        print(self.records.values())

        for record in self.records.values():
            print(record.functionName)
            record.evaluate_cacheable(self.records)

    def print_fun_report(self):
        print("\n\nFunction Report")
        #self.evaluate_all_cacheable()
        print("{:<30} {:<10} {:<10} {:<10}".format('fun', 'freq', 'cache', 'callers'))
        for record in self.records.values():
            record.print_report()
        
    def report_executed_functions(self):
        print("estoy en report_executed_functions")
         
        self.print_fun_report()
        return self.records
