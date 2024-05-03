from typing import List, AnyStr

import pandas as pd

from app.config import log, CONFIG
from app.db_module.connect import SimplePostgresConnector


async def exec_sql(
    sql_qry: AnyStr,
    params: List,
    name: AnyStr,
) -> pd.DataFrame:
    """
    Returns data based on a sql query
    Args:
        sql_qry: SQL Query string
        params: SQL params list
        name: Name of the query, used for logging
    Returns:
        pyarrow Table
    """
    try:
        log.debug(f"starting query for: {name}")

        connector = SimplePostgresConnector(
            host=CONFIG.DATABASE.HOST, dbname=CONFIG.DATABASE.DBNAME, user=CONFIG.DATABASE.USER
        )
        results = connector.execute_query(sql_qry, params)
        return results

    except Exception as e:
        raise e
