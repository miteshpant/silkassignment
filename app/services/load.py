from flask import current_app
from pymongo import UpdateOne
import logging

logger = logging.getLogger(__name__)


def load_data_to_mongo(transformed_data, batch_size=1000):
    db = current_app.mongo.db
    operations = []
    for i, item in enumerate(transformed_data):
        operations.append(
            UpdateOne({'_id': item['_id']}, {'$set': item}, upsert=True)
        )

        if len(operations) >= batch_size:
            db.common_model.bulk_write(operations)
            logger.info(f"Loaded {len(operations)} records into MongoDB")
            operations = []

    if operations:
        db.common_model.bulk_write(operations)
        logger.info(f"Loaded {len(operations)} records into MongoDB")
