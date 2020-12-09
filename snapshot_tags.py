# This script copies tag value of specified tag key of ec2 volume
# to snapshots made from the volume.

import boto3

tagKey = input("Input tag key: ")
account_id = input("Input account ID: ")
region = input("Input a region (e.g. us-east-1): ")

def for_region():
    '''
    Copies tag value of tag key for specified region in the account.
    :return:
    '''

    request_get = boto3.client('ec2', region_name=region)

    def get_snapshot():
        '''
        Returns snapshots for the account in the region specified in get_region() function.
        :return: List of snapshots
        '''
        request_snapshot = request_get.describe_snapshots(Filters=[{'Name':'owner-id','Values':[account_id]}])
        return request_snapshot
    get_snapshot()

    def get_volume():
        '''
        Returns volumes in the region with specified tag key.
        :return: List of volumes
        '''
        request_volumes = request_get.describe_volumes(Filters=[{'Name':'tag-key','Values':[tagKey]}])
        return request_volumes
    get_volume()

    def tagging_snapshots():
        '''
        Tagging snapshots by volume ID with tag value of the volume.
        :return: None
        '''

        for response_snapshot in get_snapshot():
            for snapshots in get_snapshot()['Snapshots']:
                volume_to_tag = snapshots['VolumeId']
                snapshot_id = snapshots['SnapshotId']
                for response_volumes in get_volume():
                    for volumes in get_volume()['Volumes']:
                        volume_id_resp = volumes['VolumeId']
                        volume_tags = volumes['Tags']
                        for volume_keys in volume_tags:
                            if volume_keys['Key'] == tagKey:
                                tag = volume_keys['Value']
                                volume_id = volume_id_resp
                                if volume_id == volume_to_tag:
                                    print(tagKey)
                                    set_snap_tag = boto3.resource('ec2', region_name=region).Snapshot(snapshot_id).create_tags(Tags=[
                                        {
                                            'Key': tagKey,
                                            'Value': tag
                                        }
                                    ])

    tagging_snapshots()
for_region()