from pathlib import Path


def get_sql_statement(file_name: str, query_folder: str | None = None):
    """
    Depending on the prefix of an endpoint the method checks if there is a corresponding sql file available relative to
    the current file location (../../queries/<prefix>.sql)
    Args:
        file_name: The file_name of an endpoint
        query_folder (str): A string representation of a folder where the files shall be located

    Returns:
        A sql statement taken from a sql file
    """
    query_folder = "" if query_folder is None else query_folder
    sql_file = Path(__file__).parent.parent / query_folder / file_name
    if not sql_file.is_file():
        raise FileNotFoundError("No sql file found (" + sql_file + ")")
    with sql_file.open() as my_sql_file:
        sql_statement = my_sql_file.read()
    return sql_statement
