from typing import Dict
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def save_to_db(superbase_connection, table_name: str, payload: dict):
    logger.info(f"Attempting insert into {table_name}: {payload}")
    response = superbase_connection.table(table_name).insert(payload).execute()
    return response