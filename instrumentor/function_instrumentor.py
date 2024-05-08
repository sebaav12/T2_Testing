from ast import *
import astor

class FunctionInstrumentor(NodeTransformer):

    def visit_Module(self, node: Module):
        transformedNode = NodeTransformer.generic_visit(self, node)
        import_profile_inyected = parse("from function_profiler import FunctionProfiler")
        transformedNode.body.insert(0, import_profile_inyected.body[0])
        fix_missing_locations(transformedNode)
        return transformedNode

    def visit_FunctionDef(self, node: FunctionDef):
        transformedNode = NodeTransformer.generic_visit(self, node)

        # Preparar el llamado a record_start
        argList = [arg.arg for arg in transformedNode.args.args]
        argNames = [Name(id=n, ctx=Load()) for n in argList]
        argNames = [Constant(value=transformedNode.name), List(elts=argNames, ctx=Load())]

        before = Expr(value=Call(
            func=Attribute(value=Name(id='FunctionProfiler', ctx=Load()), attr='record_start', ctx=Load()),
            args=argNames,
            keywords=[]
        ))

        # Insertar record_start al principio de la función
        if isinstance(transformedNode.body, list):
            transformedNode.body.insert(0, before)
        else:
            transformedNode.body = [before, node.body]

        # Inyectar `add_internal_call` para cada llamada interna
        new_body = []
        for stmt in transformedNode.body:
            if isinstance(stmt, Expr) and isinstance(stmt.value, Call) and isinstance(stmt.value.func, Name):
                # Registrar la llamada interna en el perfilador
                internal_call = Expr(value=Call(
                    func=Attribute(value=Name(id='FunctionProfiler', ctx=Load()), attr='add_internal_call', ctx=Load()),
                    args=[Constant(value=stmt.value.func.id)],
                    keywords=[]
                ))
                new_body.append(internal_call)
                new_body.append(stmt)
            else:
                new_body.append(stmt)

        transformedNode.body = new_body

        # Evaluar si hay un return explícito
        has_return = any(isinstance(stmt, Return) for stmt in transformedNode.body)
        if has_return:
            for i, stmt in enumerate(transformedNode.body):
                if isinstance(stmt, Return):
                    new_return = Call(
                        func=Attribute(value=Name(id='FunctionProfiler', ctx=Load()), attr='record_end', ctx=Load()),
                        args=[Constant(value=transformedNode.name), stmt.value],
                        keywords=[]
                    )
                    transformedNode.body[i] = Return(value=new_return)
        else:
            # Añadir record_end con `None` al final si no hay return explícito
            end_call = Expr(value=Call(
                func=Attribute(value=Name(id='FunctionProfiler', ctx=Load()), attr='record_end', ctx=Load()),
                args=[Constant(value=transformedNode.name), Constant(value=None)],
                keywords=[]
            ))
            transformedNode.body.append(end_call)

        # Imprimir la función transformada
        print(astor.to_source(transformedNode))

        return transformedNode
