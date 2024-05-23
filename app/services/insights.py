import time

from flask import current_app


def generate_insights(deduplicated_data):
    insights = []
    for host in deduplicated_data:
        insight = {
            'host_id': host['_id'],
            'hostname': host['hostname'],
            'os': host.get('operating_system', 'Unknown'),
            'provider': host.get('provider', 'Unknown'),
            'data': time.time()
        }
        insights.append(insight)
    return insights


def save_insights_to_mongo(insights):
    db = current_app.mongo.db
    db.insights.insert_many(insights)
