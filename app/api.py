from app.services.fetcher import fetch_data_from_api, fetch_existing_hosts
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
    param_list = []
    start = 0
    while total_hosts_left > 0:
        param_list.append(
            {
                "skip": start,
                "limit": min(limit, total_hosts_left)
            }
        )
        start = start + limit
        total_hosts_left -= limit

    new_data_chunks = {}
    for source in sources:
        new_data_chunks[source] = []
        api_url = current_app.config['API_URL'][source]
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_params = {executor.submit(fetch_data_from_api, api_url, params): params for params in param_list}
            for future in as_completed(future_to_params):
                try:
                    new_data_chunks[source].extend(future.result())
                except Exception as e:
                    logger.error(f"Error fetching data: {e}")

    transformed_data = transform_data(new_data_chunks)
    existing_data = fetch_existing_hosts()
    combined_data = combine_data(transformed_data, existing_data)
    load_data_to_mongo(combined_data)

    # there can be a separate async service to generate
    # insights for the data that we are capturing
    # insights = generate_insights(combined_data)
    # save_insights_to_mongo(insights)

    logger.info(f"data fetched, transformed, deduplicated, and loaded successfully")
    return "data processed successfully", 200
