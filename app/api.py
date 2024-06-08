import asyncio

from app.config import Params
from app.services.fetcher import fetch_data_from_api, fetch_existing_hosts, fetch_data_for_limit_params, \
    fetch_data_for_cursor_params, get_limit_params, fetch_data_async
from flask import Blueprint, current_app
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.transform.common_transform import transform_data, combine_data
from app.services.load import load_data_to_mongo
import logging

bp = Blueprint('api', __name__)
logger = logging.getLogger(__name__)


@bp.route('/data', methods=['GET'])
def fetch_data():
    sources = current_app.config['SOURCES']

    limit = current_app.config['API_HOST_LIMIT']
    total_hosts_left = current_app.config['TOTAL_HOSTS_TO_BE_PROCESSED']
    param_list = get_limit_params(total_hosts_left, limit)

    new_data_chunks = asyncio.run(fetch_data_async(sources, param_list))

    transformed_data = transform_data(new_data_chunks)
    existing_data = fetch_existing_hosts()
    combined_data = combine_data(transformed_data, existing_data)
    load_data_to_mongo(combined_data)

    logger.info(f"data fetched, transformed, deduplicated, and loaded successfully")
    return "data processed successfully", 200


