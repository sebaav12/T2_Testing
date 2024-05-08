import sys
import ast
import inspect
from types import *
import traceback
from stack_inspector import StackInspector
from line_record import LineRecord  

""" Clase para la Tarea 2. Para su uso, considere:
with CoverageTracer() as covTracer:
    function_to_be_traced()

covTracer.report_executed_lines()
"""

class CoverageTracer(StackInspector):

    def __init__(self):
        super().__init__(None, self.traceit)
        self.executed_lines = [] #lista que almacena las líneas ejecutadas.
        self.freq = {} #diccionario que almacena la cantidad de veces que cada línea fue ejecutada.


    # esta función la copié de la función traceit del archivo function_tracer.py del código base
    def traceit(self, frame, event: str, arg):
        if event == 'line':
            function_name = frame.f_code.co_name
            line = frame.f_lineno
            if not self.our_frame(frame) and not self.problematic_frame(frame):
                self.executed_lines.append((function_name, line))
    
        return self.traceit

    def print_lines_report(self):
        print("{:<30} {:<10} {:<10}".format('fun', 'line', 'freq'))
        #revisa si la función ya fue ejecutada por primera vez, en caso de no haber sido ejecutada se agrega al diccionario
        #En caso contrario, se suma uno a la frecuencia de la función
        for function_name, line in self.executed_lines:
            if (function_name, line) in self.freq:
                self.freq[(function_name, line)] += 1
            else:
                self.freq[(function_name, line)] = 1
        #Ordena la lista según el número de línea.
        sorted_list = sorted(self.freq.items(), key=lambda a: a[0][1]) # esta función la copié de la función report_executed_functions del archivo function_tracer.py del código base
        #imprime lo pedido 
        for (function_name, line), freq in sorted_list:
            print("{:<30} {:<10} {:<10}".format(function_name, line, freq))

    def report_executed_lines(self):
        self.print_lines_report() #imprime el output 
        line_records_instances = [] #lista de instancias de la clase Line Record
        sorted_list = sorted(self.freq.items(), key=lambda a: a[0][1]) #ordena la lista según el número de línea
        for (function_name, line_number), freq in sorted_list:
            line_records_instances.append(LineRecord.new_instance_with(function_name, line_number, freq)) #genera una instancia de 
            #Line Record y la agrega a la lista.
        return line_records_instances #devuelve la lista de instancias de la clase Line Record