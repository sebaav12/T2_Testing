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
        print(f"Iniciando ejecución de {functionName} con argumentos {args}")
        instance = cls.getInstance()
        record = instance.get_record(functionName)
        record.increase_frequency()

        # Registrar la función desde la que se hizo la llamada
        if cls.call_stack:
            print(f"{cls.call_stack[-1]} llama a {functionName}")
            print(f"La función {cls.call_stack[-1]} llama a {functionName}")
            record.add_caller(cls.call_stack[-1])   

        print(f"Entrando a {functionName}")

        # Agrega al call_stack
        cls.call_stack.append(functionName)

        # Guarda los argumentos para usarlos en record_end (cache)

        print("args en recod stat: " + str(args))
        print("tipo " + str(type(args)))
        cls.current_args = args   

    #   def record_end(cls, functionName, returnValue):
    #     cls.getInstance().fun_call_end(functionName, returnValue)
    #     return returnValue
    
    @classmethod
    def record_end(cls, functionName, returnValue):
        print(f"Finalizando ejecución de {functionName}, retorno: {returnValue}")
        if cls.call_stack and cls.call_stack[-1] == functionName:

            # Guardar el resultado de la función para el cache
            record = cls.getInstance().get_record(functionName)

            print(" El resultdo de " +str(functionName) +" es "+ str(returnValue))
            record.add_result(cls.current_args, returnValue)

            print(" resultado agregado coectamente")

            # Eliminar la función actual de la pila para el caller

            print("call stck")
            print(cls.call_stack)
            cls.call_stack.pop()

            print("call stck nuevo")
            print(cls.call_stack)

            print("se elimino")
        else:
            print(f"Error: Desbalance en la pila al salir de {functionName}")

        return returnValue
        

    @classmethod
    def add_internal_call(cls, functionName):
        """Añadir una llamada interna a la función en la parte superior de la pila."""
        print("add_internal_call")
        if cls.call_stack:
            record = cls.getInstance().get_record(cls.call_stack[-1])
            record.add_internal_call(functionName)

    # Este metodo inyecta codigo en el programa segun el visitor del profiler
    @classmethod
    def instrument(cls, ast):
        print("instrumentor")
        visitor = FunctionInstrumentor()
        return fix_missing_locations(visitor.visit(ast))
    
    # Metodos de instancia
    def __init__(self):
        self.records = {}

    def get_record(self, functionName):
        print("get_record para " + str(functionName))
        print(" self records: " + str(self.records))
        if functionName not in self.records:
            self.records[functionName] = FunctionRecord(functionName)
            print("no estaba aca")
        return self.records[functionName]

    def fun_call_start(self, functionName, args):  
        record = self.get_record(functionName)

    def fun_call_end(self, functionName, returnValue):
        pass

    def print_fun_report(self):
        print("\nFunction Report")
        print("{:<30} {:<10} {:<10} {:<10}".format('fun', 'freq', 'cache', 'callers'))
        for record in self.records.values():
            record.print_report()
        
    def report_executed_functions(self):
        print
        self.print_fun_report()
        return self.records



# def factorial(n):
#     FunctionProfiler.record_start('factorial', [n])
#     if n == 0:
#         result = 1
#     else:
#         print(type(factorial(n - 1)))
#         result = n * factorial(n - 1)
#     return FunctionProfiler.record_end('factorial', result)

# Probar con `factorial(1)`
#print(factorial(2))