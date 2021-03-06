# This script copies tag value of specified tag key of ec2 volume
# to snapshots made from the volume.

import boto3
from botocore.exceptions import ClientError

tagKey = input("Input tag key: ")
account_id = input("Input account ID: ")
region = input("Input a region (e.g. us-east-1): ")
request_get = boto3.client('ec2', region_name=region)


def get_snapshots():
    '''
    Returns snapshots for the account in the region.
    :return: List of snapshots
    '''
    print("Getting snapshots....")
    request_snapshots = request_get.describe_snapshots(Filters=[{'Name':'owner-id','Values':[account_id]}])
    return request_snapshots


def get_volumes():
    '''
    Returns volumes in the region with specified tag key.
    :return: List of volumes
    '''
    print("Getting volumes.....")
    request_volumes = request_get.describe_volumes(Filters=[{'Name':'tag-key','Values':[tagKey]}])
    return request_volumes


def tagging_snapshots():
    '''
    Copying tag value of the volume with specified tag key to snapshots.
    :return: None
    '''
    all_snapshots = get_snapshots()
    all_volumes = get_volumes()
    available_zones = [region + 'a', region + 'b', region + 'c', region + 'd']
    for snapshots in all_snapshots['Snapshots']:
        volume_id_in_snap = snapshots['VolumeId']
        snapshot_id = snapshots['SnapshotId']
        if 'Tags' in snapshots:
            snapshot_tags = snapshots['Tags']
            for a in snapshot_tags:
                if tagKey not in a['Key']:
                    continue

            for volumes in all_volumes['Volumes']:
                volume_id_resp = volumes['VolumeId']
                volume_tags = volumes['Tags']
                for volume_keys in volume_tags:
                    if volume_keys['Key'] == tagKey and volumes['AvailabilityZone'] in available_zones:
                        tag = volume_keys['Value']
                        volume_id = volume_id_resp
                        if volume_id == volume_id_in_snap:
                            try:
                                print(f"Tagging snapshot: {snapshot_id}")
                                set_snap_tag = boto3.resource('ec2', region_name=region).Snapshot(snapshot_id).create_tags(Tags=[
                                    {
                                        'Key': tagKey,
                                        'Value': tag
                                    }
                                ])
                            except ClientError:
                                pass

tagging_snapshots()
print("Done!")
