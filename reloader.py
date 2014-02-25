import os
from decorator import decorator
from collections import defaultdict

__all__ = ['reload_from']

module_mts = defaultdict(int)
module_funcs = defaultdict(dict)

def reload_from(module, name=None):
    def dec(f):
        from_name = name
        if from_name is None:
            from_name = f.__name__

        module_funcs[module][from_name] = f # fallback

        def reloader(f, *args, **kwargs):
            check_reload(module)
            f = module_funcs[module][from_name]
            return f(*args, **kwargs)

        return decorator(reloader, f)

    return dec

def check_reload(module):
    # TODO: set a flag in a background thread instead
    try:
        mt = os.path.getmtime(module.__file__)
    except Exception, e:
        print 'Exception checking %s' % module
        return

    if mt == module_mts[module]:
        return

    module_mts[module] = mt
    try:
        reload(module)
    except Exception, e:
        print 'Exception reloading %s' % module
        return

    print 'Reloaded %s' % module
    funcs = module_funcs[module]
    for name in funcs:
        funcs[name] = getattr(module, name)

