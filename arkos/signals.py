"""
Classes and functions to manage internal signal hooks and listeners.

arkOS Core
(c) 2016 CitizenWeb
Written by Jacob Cook
Licensed under GPLv3, see LICENSE.md
"""

from arkos import storage, logger


class Listener:
    """
    Class representing a signal listener.

    A signal listener is set up to track the emittance of certain signals
    and to execute a function based on the result of said emittance. These
    are good to use for cleanup after an item is removed from the system,
    or for making sure certain elements are established after loading a
    necessary component.
    """

    def __init__(self, by, id, sig, func):
        """
        Initialize the signal listener.

        :param str by: the name of the module that registered this listener
        :param str id: identifier for this listener
        :param str sig: signal ID to listen for
        :param func func: hook function to execute
        """
        self.id = id
        self.by = by
        self.sig = sig
        self.func = func

    def trigger(self, data, crit=True):
        """
        Trigger the hook function for this listener.

        :param data: parameter to provide to the hook function
        :param bool crit: Raise hook function exceptions?
        """
        try:
            if data:
                self.func(data)
            else:
                self.func()
        except:
            if crit:
                raise


def add(by, id, sig, func):
    """
    Register a new listener with the system.

    :param str by: the name of the module that registered this listener
    :param str id: identifier for this listener
    :param str sig: signal ID to listen for
    :param func func: hook function to execute
    """
    if not storage.signals.get(id):
        storage.signals[id] = []
    storage.signals[id].append(Listener(by, id, sig, func))
    logger.debug("Sign", "Registered {0} to {1} for {2}".format(
        sig, id, by
    ))


def emit(id, sig, data=None, crit=True):
    """
    Emit a signal.

    :param str id: name of the module emitting this signal
    :param str sig: signal ID
    :param data: parameter to pass to hook function (if necessary)
    :param bool crit: Raise hook function exceptions?
    """
    if not storage.signals.get(id):
        return
    sigs = filter(
        lambda x: x.sig == sig, storage.signals.get(id)
    )
    for x in sigs:
        x.trigger(data, crit)


def remove(by):
    """
    Deregister all listeners for this module.

    :param str by: name of the module to dereigster listeners for
    """
    for x in storage.signals:
        for y in filter(lambda z: z.by == by, storage.signals[x]):
            storage.signals.remove(y)
