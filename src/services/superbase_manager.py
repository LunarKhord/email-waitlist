from typing import Dict
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def save_to_db(superbase_connection, table_name:str, payload: Dict) -> bool:
    logger.info("Attempt to save email to superbase...")
    try:
        response =  (
            superbase_connection.table(table_name)
            .insert(payload)
            .execute()
            )
        logger.info("Email was saved to subperbase.")
        return True
    except Exception as e:
        logger.error(f"Unable to save email to superbase {e}")
        raise e