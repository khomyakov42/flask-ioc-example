import abc
import typing
import threading
import contextlib


class Transaction:
    def __init__(self):
        self.__callbacks = []
        self.__finished = False
        self.__lock = threading.RLock()

    def subscribe(self, callback: typing.Callable[[bool], None]):
        self.__callbacks.append(callback)

    def commit(self):
        self.__finish(True)

    def rollback(self):
        self.__finish(False)

    def __finish(self, success):
        with self.__lock:
            if self.__finished:
                raise Exception('Transaction finished')

        for callback in self.__callbacks:
            callback(success)


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def set_transaction(self, tx: typing.Union[Transaction, None]):
        raise NotImplementedError()


@contextlib.contextmanager
def transaction(*repositories: typing.List[Repository]):
    tx = Transaction()
    for repository in repositories:
        repository.set_transaction(tx)

    try:
        yield tx
    except:
        tx.rollback()
        raise
    else:
        tx.commit()
    finally:
        for repository in repositories:
            repository.set_transaction(None)