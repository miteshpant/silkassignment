from app.transform.qualys_transform import transform_qualys
from app.transform.crowdstrike_transform import transform_crowdstrike


def transform_data(new_data):
    all_transformed_data = []
    for model in new_data:
        if model == 'qualys':
            # deduplicate data from qualys
            deduplicated_merged_data = deduplicate_hosts_within_model(new_data[model], 'fqdn', 'address')
            all_transformed_data.extend(transform_qualys(deduplicated_merged_data, model))
        elif model == 'crowdstrike':
            # deduplicate data from crowdstrike
            deduplicated_merged_data = deduplicate_hosts_within_model(new_data[model], 'hostname', 'local_ip')
            all_transformed_data.extend(transform_crowdstrike(deduplicated_merged_data, model))
    #         deduplicate final data from all sources
    return deduplicate_hosts_within_model(all_transformed_data,'hostname','ip_address')


def deduplicate_hosts_within_model(hosts, key1, key2):
    unique_hosts = {}
    # we can also merge data if that is different
    # in multiple entries of same host
    for host in hosts:
        key = (host[key1], host[key2])
        if key not in unique_hosts:
            unique_hosts[key] = host
    return list(unique_hosts.values())


def combine_data(transformed_data, existing_data):
    retrieved_data = {item['ip_address']: item for item in transformed_data}
    combined_data = {item['ip_address']: item for item in existing_data}

    for ip_address in retrieved_data:
        if ip_address in combined_data:
            combined_data[ip_address].update(retrieved_data[ip_address])
        else:
            combined_data[ip_address] = retrieved_data[ip_address]
            combined_data[ip_address]['first_seen'] = retrieved_data[ip_address]['observation_date']
        combined_data[ip_address]['last_seen'] = retrieved_data[ip_address]['observation_date']

    return list(combined_data.values())
