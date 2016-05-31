from psycopg2.extras import DictConnection
import typing
import inject
from sample.repository.base import Repository, Transaction


class TransactionManager:
    def __init__(self, connection: DictConnection):
        self.connection = connection
        self.autocommit = None
        self.tx_counter = 0

    def begin_transaction(self, tx):
        self.autocommit = self.connection.autocommit
        if self.connection.autocommit:
            self.connection.autocommit = False
        tx.subscribe(self.__create_callback())
        self.tx_counter += 1

    def __create_callback(self):
        def callback(success):
            self.tx_counter -= 1
            if self.tx_counter == 0:
                try:
                    if success:
                        self.connection.commit()
                    else:
                        self.connection.rollback()
                except:
                    self.connection.autocommit = self.autocommit
                    raise

        return callback


class PgRepository(Repository):

    @inject.params(connection=DictConnection)
    def __init__(self, connection):
        self.__tx_manager = TransactionManager(connection)
        self.connection = connection

    def set_transaction(self, tx: typing.Union[Transaction, None]):
        if tx:
            self.__tx_manager.begin_transaction(tx)


