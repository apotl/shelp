from os import listdir
from re import match
from importlib import import_module
SHELPERS = [shelper[:-3] for shelper in listdir('shelpers') if match(r'^.*\.py$', shelper)
            and shelper != '__init__.py']
for shelper in SHELPERS:
    import_module('shelpers.'+shelper)
    del(shelper)
del(SHELPERS)
del(listdir)
del(match)
del(import_module)
