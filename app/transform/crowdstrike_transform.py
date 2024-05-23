import time


def transform_crowdstrike(data, source):
    transformed = []
    for item in data:
        transformed.append({
                '_id': item['device_id'],
                'hostname': item['hostname'],
                'ip_address': item['local_ip'],
                'data_source': source,
                'provider': item.get('service_provider', 'UNKNOWN')[:10],
                'operating_system': item.get('os_version', 'UNKNOWN')[:10],
                'observation_date': time.time()
            })
    return transformed
