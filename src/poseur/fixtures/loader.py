import inspect 

from django.utils.importlib import import_module
from poseur.fixtures import FakeModel


def _get_unmet_dependency(faker, faked):
    for req in faker.requires:
        if req not in faked:
            return req
    raise NotImplementedError 
    

def _dependencies_met(faker, faked):
    return all(req in faked for req in faker.requires)

def _generate(fakers, faked):
    if not len(fakers):
        return 
    if _dependencies_met(fakers[0], faked):
        fakers[0].generate()
        faked.append(fakers[0])
        _generate(fakers[1:], faked)
    else:
        dep = _get_unmet_dependency(fakers[0], faked)
        fakers.insert(0, fakers.pop(fakers.index(dep)))
        _generate(fakers, faked)
        

def load_fixtures(import_path):
    mod = import_module(import_path)
    fakers = [
        getattr(mod, attr)
        for attr in dir(mod)
        if inspect.isclass(getattr(mod, attr)) and \
            getattr(mod, attr) != FakeModel and \
            issubclass(getattr(mod, attr), FakeModel)
    ]
    _generate(fakers, [])
