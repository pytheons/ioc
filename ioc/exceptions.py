# vim: set fileencoding=utf-8 :

# import exceptions

class UnknownService(Exception):
    pass

class CyclicReference(Exception):
    pass
    