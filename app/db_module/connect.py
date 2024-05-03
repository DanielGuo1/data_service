import pandas as pd
import psycopg2
from contextlib import contextmanager
from app.config import log, CONFIG


class SimplePostgresConnector:
    """
    A simplified class for managing PostgreSQL connections with basic functionalities.
    This class simplifies the process of connecting to, executing queries on, and managing PostgreSQL database connections.
    """

    def __init__(self, host, dbname, user, password=None, port=5432):
        """
        Initializes a new instance of the SimplePostgresConnector.

        Args:
            host (str): The hostname or IP address of the database server.
            dbname (str): The name of the database to connect to.
            user (str): The username used to authenticate with the database.
            password (str, optional): The password used to authenticate with the database. Defaults to None.
            port (int, optional): The port number on which the database server is listening. Defaults to 5432.
        """
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        """
        Establishes a connection to the database.
        Sets autocommit to True for the session, as required.
        """
        if not self.connection:
            try:
                self.connection = psycopg2.connect(
                    host=self.host, dbname=self.dbname, user=self.user, password=self.password, port=self.port
                )
                self.connection.autocommit = True
                log.info("Database connection successfully established.")
            except psycopg2.Error as e:
                log.error(f"Error establishing a connection to the database: {e}")
                raise

    def close(self):
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            log.info("Database connection closed.")

    @contextmanager
    def cursor(self):
        """
        A context manager that opens and automatically closes a cursor.
        Ensures that the connection is opened and closed properly.
        """
        self.connect()
        try:
            with self.connection.cursor() as cur:
                yield cur
        finally:
            self.close()

    def execute_query(self, query, params=None):
        """
        Executes an SQL query and returns the results.

        Args:
            query (str): The SQL query to execute.
            params (tuple, list, or dict, optional): Parameters to use with the query. Defaults to None.

        Returns:
            list: The result of the query as a list of tuples. None if there are no results to fetch.
        """
        try:
            with self.cursor() as cursor:
                cursor.execute(query, params)
                if cursor.description:
                    columns = [desc[0] for desc in cursor.description]
                    return pd.DataFrame(cursor.fetchall(), columns=columns)
                return None
        except psycopg2.Error as e:
            log.error(f"Error executing the query: {e}")
            raise


# Example usage of the class
connector = SimplePostgresConnector(host=CONFIG.DATABASE.HOST, dbname=CONFIG.DATABASE.DBNAME, user=CONFIG.DATABASE.USER)
sql_query = "SELECT * FROM attributes"

try:
    results = connector.execute_query(sql_query)

except Exception as e:
    log.error(f"Error executing SQL query: {e}")
