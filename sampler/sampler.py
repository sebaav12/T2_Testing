from __future__ import print_function
import threading
from time import sleep
import traceback
from sys import _current_frames

class Sampler:
    def __init__(self, tid) -> None:
        self.tid = tid
        self.t = threading.Thread(target=self.sample, args=())
        self.active = True
        self.counts_dict = {}
        self.num_seconds = 0

    def start(self):
        self.active = True
        self.t.start()

    def stop(self):
        self.active = False
        
    def checkTrace(self):
        for thread_id, frames in _current_frames().items():
            if thread_id == self.tid:
                frames = traceback.walk_stack(frames)
                stack = []
                for frame, _ in frames: 
                    code = frame.f_code.co_name
                    stack.append(code)
                stack.reverse()
                #print(stack)  # Esta linea imprime el stack despues de invertirlo la pueden comentar o descomentar si quieren
                return stack 
    
    def sample(self):
        while self.active:
            stack = self.checkTrace()
            if stack:
                self.update_counts_dict(stack)
                self.num_seconds += 1
            sleep(1)



    def update_counts_dict(self, stack):
        node = self.counts_dict #obtiene el diccionario actual.
        for func in stack:  #le suma uno al elemento correspondiente del diccionario cada vez que aparece en
        #el stack y lo agrega al diccionario en caso de que no esté (es decir, es la primera vez que se llama)        
            if func not in node:
                node[func] = {"count": 1}  
            else:
                node[func]["count"] += 1 
            node = node[func] #genera que los diccionarios se guarden uno dentro de otro, para luego
            #al imprimir generar la estructura del árbol.


    def print_report(self):
        print(f"total ({self.num_seconds} seconds)") #imprime la cantidad total de segundos.
        self.print_tree(self.counts_dict)

    #función recursiva que imprime el diccionario counts_dict en forma de árbol  
    def print_tree(self, counts_dict, indent=1):   
        for func, child_node in counts_dict.items(): #revisa la función y el nodo hijo (función que se ejecuta después de ella)
            if isinstance(child_node, dict):  #revisa si el nodo hijo es un diccionario.
                count = child_node.get("count", 0) #obtiene el número de veces que esa función en esa profundidad es llamada.
                print("    " * indent + f"{func} ({count} seconds)")
                self.print_tree(child_node, indent + 1)  #llamanda recursiva aumentando la indentación.