import time


def transform_qualys(data, source):
    transformed = []
    for item in data:
        transformed.append({
                '_id': item['id'],
                'hostname': item['fqdn'],
                'ip_address': item['address'],
                'data_source': source,
                'provider': item.get('cloudProvider', 'UNKNOWN')[:10],
                'operating_system': item.get('os', 'UNKNOWN')[:10],
                'observation_date': time.time()
        })
    return transformed
