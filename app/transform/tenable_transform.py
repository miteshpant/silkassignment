import time


def transform_tenable(data, source):
    transformed = []
    for item in data:
        transformed.append({
                '_id': item['_id'],
                'hostname': item['host_name'],
                'ip_address': item['display_ipv4_address'],
                'data_source': source,
                'provider': item.get("system_type", 'UNKNOWN')[:20],
                'operating_system': item.get('display_operating_system', 'UNKNOWN')[:20],
                'observation_date': time.time()
            })
    return transformed
