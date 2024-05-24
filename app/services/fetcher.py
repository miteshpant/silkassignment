import logging

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
