import compiler
import types

METHOD_SOURCE = 'def {name}({args}): pass'


def generate_method_source(name, argc):
    args = ['arg_{0}'.format(index) for index in range(argc)]
    return METHOD_SOURCE.format(name=name, args=', '.join(args))


def create_pass_method(name='pass_method', argc=0):
    context = {}

    source = generate_method_source(name, argc)
    compiled = compiler.compile(source, '<generated>', 'exec')

    eval(compiled, context)

    return context[name]


def create_bound_pass_method(name='pass_method', argc=0, binding=object()):
    method = create_pass_method(name, argc)
    return types.MethodType(method, binding, binding.__class__)
