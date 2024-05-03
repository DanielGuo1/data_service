import psycopg2
from contextlib import contextmanager
from app.config import log


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

    def parse_query(self, sql) -> str:
        """Decide which query best to execute by looking at the SQL statement.

        This function focuses on basic SQL statements and selects the appropriate execution method accordingly.

        Args:
            sql: SQL query
            force_read_only: Ensure that stored procedures are directed to read-only mode if True.

        Returns:
            Callable: Method to execute the query.

        """
        if not isinstance(sql, str):
            raise ValueError("SQL statements must be a string")
        raw = [x for x in sql.casefold().strip().split() if x]
        if not raw:
            raise ValueError("SQL statement seems to be empty")

        return raw

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
                    return cursor.fetchall()
                return None
        except psycopg2.Error as e:
            log.error(f"Error executing the query: {e}")
            raise


# Example usage of the class
connector = SimplePostgresConnector(host="localhost", dbname="data_service", user="platau")
sql_query = "SELECT * FROM attributes"

try:
    parsed_query = connector.parse_query(sql_query)
    results = connector.execute_query(sql_query)
    for row in results:
        print(row)

except Exception as e:
    log.error(f"Error executing SQL query: {e}")
