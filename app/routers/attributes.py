import inspect
from typing import List

import pandas as pd
from fastapi import Query, Depends, APIRouter

from app.queries.get_data import exec_sql
from app.queries.sql import get_sql_statement
from entities.attributes import AttributeResponseList, Attributes

router = APIRouter(tags=["attributes"])


@router.get("/read_data", response_model=AttributeResponseList)
async def read_data(
    names: List[str] | None = Query(None, description="list of names"),  # noqa: B008
    ids: List[str] | None = Query(None, description="list of ids"),  # noqa: B008
    descriptions: List[str] | None = Query(None, description="list of descriptions"),  # noqa: B008
    sources: List[str] | None = Query(None, description="list of sources"),  # noqa: B008
    request_params: Attributes = Depends(),  # noqa: B008
) -> pd.DataFrame:
    """

    Args:
        ids: list of ids or fragments of ids to filter output. Should be usable in the manner of a search function.
            Defaults to no filter.
        names: List of attribute names or fragments of names to filter output. Defaults to no filter.
        descriptions: List of descriptions or fragments of descriptions to filter output. Defaults to no filter.
        sources: List of sources to filter output. Defaults to no filter.
        request_params: see AssetRequestParams model

    Returns:
        List of AttributeMasterData
    """
    try:
        sql_qry = get_sql_statement("sql/read_data.sql")
        name = inspect.currentframe().f_code.co_name
        params = ids
        df = await exec_sql(sql_qry, params, name)
        data = df.to_dict(orient="records")
        return data
    except Exception as e:
        raise e


@router.post("/insert_data", response_model=Attributes)
async def insert_data(
    new_data: List[Attributes],
) -> str:
    try:
        sql_query = get_sql_statement("sql/insert_data.sql")
        params = [(data.name, data.description, data.default, data.source, data.type) for data in new_data]
        name = inspect.currentframe().f_code.co_name
        await exec_sql(sql_query, params, name)

        return "done"
    except Exception as e:
        raise e
