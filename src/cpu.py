import multiprocessing
import inspect
from multiprocessing.managers import BaseManager, NamespaceProxy, AutoProxy

from player import User, Computer
from cards import Deck

# ======= Workaround for py36 bug ========

# https://stackoverflow.com/questions/46779860/multiprocessing-managers-and-custom-classes

# Backup original AutoProxy function
backup_autoproxy = multiprocessing.managers.AutoProxy

# Defining a new AutoProxy that handles unwanted key argument 'manager_owned'


def redefined_autoproxy(token, serializer, manager=None, authkey=None,
                        exposed=None, incref=True, manager_owned=True):
    # Calling original AutoProxy without the unwanted key argument
    return backup_autoproxy(token, serializer, manager, authkey,
                            exposed, incref)


# Updating AutoProxy definition in multiprocessing.managers package
AutoProxy = redefined_autoproxy

# ========================================


class GameManager(BaseManager):
    pass

# A proxy that exposes all class methods AND attributes


class NamedProxy(NamespaceProxy):
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__')


def register_proxy(name, cls, proxy):
    for attr in dir(cls):
        if inspect.ismethod(getattr(cls, attr)) and not attr.startswith("__"):
            proxy._exposed_ += (attr,)
            setattr(proxy, attr,
                    lambda s: object.__getattribute__(s, '_callmethod')(attr))
    GameManager.register(name, cls, proxy)


register_proxy('Deck', Deck, NamedProxy)
register_proxy('User', User, NamedProxy)
register_proxy('Computer', Computer, NamedProxy)
