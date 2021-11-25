from instance_fetcher import get_instances, get_regions

if __name__ == "__main__":
    instances = get_instances(regions=get_regions())
    regions = instances.keys()
    for region in regions:
        print(region)
        for instance in instances[region]:
            print(instance)
