import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
import app.config
from flask import current_app
import requests

logger = logging.getLogger(__name__)


def fetch_data_from_api(url, params):
    response_data = {}
    try:
        headers = {
            'accept': 'application/json',
            'token': app.config.Config.TOKEN
        }
        response = requests.post(url, params=params, headers=headers)
        response.raise_for_status()
        response_data = response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Failed to get data for {params} , {e}")
    except Exception as e:
        logger.error(f"Failed to get data for {params} , {e}")
    return response_data


def fetch_existing_hosts():
    db = current_app.mongo.db
    return list(db.common_model.find())


async def fetch_data_for_limit_params(api_url, source, param_list, new_data_chunks):
    loop = asyncio.get_event_loop()
    new_data_chunks[source["name"]] = []
    with ThreadPoolExecutor() as executor:
        tasks = [loop.run_in_executor(executor, fetch_data_from_api, api_url, params) for params in param_list]

        for result in await asyncio.gather(*tasks):
            try:
                if result:  # Ensure result is not None or empty
                    new_data_chunks[source["name"]].extend(result)
            except Exception as e:
                logger.error(f"Error fetching data: {e}")


async def fetch_data_for_cursor_params(api_url, source, new_data_chunks):
    cursor = None
    new_data_chunks[source["name"]] = []
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        while True:
            p_list = [{"cursor": cursor}]
            tasks = [loop.run_in_executor(executor, fetch_data_from_api, api_url, params) for params in p_list]

            for result in await asyncio.gather(*tasks):
                try:
                    hosts = result.get("hosts", [])
                    if hosts:
                        new_data_chunks[source["name"]].extend(hosts)
                        cursor = result.get("cursor")
                    else:
                        cursor = None
                        break
                except Exception as e:
                    logger.error(f"Error fetching data: {e}")
                    cursor = None
                    break

            if cursor is None:
                break


async def fetch_data_async(sources, param_list):
    new_data_chunks = {}
    tasks = []
    for source in sources:
        api_url = source["api_url"]
        if source["param_type"] == app.config.Params.SKIP_LIMIT:
            tasks.append(fetch_data_for_limit_params(api_url, source, param_list, new_data_chunks))
        elif source["param_type"] == app.config.Params.CURSOR:
            tasks.append(fetch_data_for_cursor_params(api_url, source, new_data_chunks))
    await asyncio.gather(*tasks)
    return new_data_chunks


def get_limit_params(total_hosts_left, limit):
    start = 0
    param_list = []
    while total_hosts_left > 0:
        param_list.append(
            {
                "skip": start,
                "limit": min(limit, total_hosts_left)
            }
        )
        start = start + limit
        total_hosts_left -= limit
    return param_list