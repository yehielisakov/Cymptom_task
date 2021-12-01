from instance_dc import Instance
from log import get_logger
from dacite import from_dict
from typing import List, Dict, Optional
import boto3

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_DEFAULT_REGION = "us-east-2"

AWS_DESCRIBE_REGIONS_RESPONSE_REGION_NAME_KEY_STR = 'RegionName'
AWS_DESCRIBE_REGIONS_RESPONSE_REGIONS_KEY_STR = 'Regions'
AWS_DESCRIBE_REGIONS_RESPONSE_INSTANCES_KEY_STR = 'Instances'
AWS_DESCRIBE_REGIONS_RESPONSE_RESERVATIONS_KEY_STR = 'Reservations'

AWS_EC2_STR = 'ec2'

logger_instance = get_logger("AwsInstanceFetcherService")


def get_regions(region_name: str = AWS_DEFAULT_REGION, aws_access_key_id: str = AWS_ACCESS_KEY_ID,
                aws_secret_access_key: str = AWS_SECRET_ACCESS_KEY) -> List[str]:
    regions = []
    try:
        ec2 = boto3.client(AWS_EC2_STR, region_name=region_name,
                           aws_access_key_id=aws_access_key_id,
                           aws_secret_access_key=aws_secret_access_key)
        describe_regions_responce = ec2.describe_regions()
        regions = [region[AWS_DESCRIBE_REGIONS_RESPONSE_REGION_NAME_KEY_STR]
                   for region in describe_regions_responce[AWS_DESCRIBE_REGIONS_RESPONSE_REGIONS_KEY_STR]]
        return regions
    except Exception as ex:
        logger_instance.error(ex)
        return regions


def get_instances(regions: List[str] = None, aws_access_key_id: str = AWS_ACCESS_KEY_ID,
                  aws_secret_access_key: str = AWS_SECRET_ACCESS_KEY) -> Dict[str, List[Instance]]:
    result: Dict[str, List[Instance]] = dict()
    if regions is None:
        return result
    for region in regions:
        try:
            ec2 = boto3.client(AWS_EC2_STR, region_name=region,
                               aws_access_key_id=aws_access_key_id,
                               aws_secret_access_key=aws_secret_access_key)
            instances = ec2.describe_instances()
            result[region] = []
            reservations = instances[AWS_DESCRIBE_REGIONS_RESPONSE_RESERVATIONS_KEY_STR]
            insts = reservations[0][AWS_DESCRIBE_REGIONS_RESPONSE_INSTANCES_KEY_STR]
            for instance in insts:
                instance_info = from_dict(data_class=Instance, data=instance)
                result[region].append(instance_info)

        except Exception as ex:
            print("Can't get instances on region %s: see log file for more details." % region)
            logger_instance.error("Error while getting instances on region %s" % region)
            logger_instance.exception(ex)
            continue

    return result
