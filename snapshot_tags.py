# This script copies tag value of specified tag key of ec2 volume
# to snapshots made from this volume.

import boto3


# Edit parameters:
tagKey = ''            # Tag key of an instance you need to copy to its volumes and network interfaces
account_id = ''        # Check it on AWS Support page
region = ''            # Specify a region


# Do not edit below
request_get = boto3.client('ec2',region_name=region)
filters = [{'Name':'tag-key','Values':[tagKey]}]
request_snapshot = request_get.describe_snapshots(Filters=[{'Name':'owner-id','Values':[account_id]}])
request_volumes = request_get.describe_volumes(Filters=[{'Name':'tag-key','Values':[tagKey]}])



for response_snapshot in request_snapshot:
    for snapshots in request_snapshot['Snapshots']:
        volume_to_tag = snapshots['VolumeId']
        snapshot_id = snapshots['SnapshotId']
        for response_volumes in request_volumes:
            for volumes in request_volumes['Volumes']:
                volume_id_resp = volumes['VolumeId']
                volume_tags = volumes['Tags']
                for volume_keys in volume_tags:
                    if volume_keys['Key'] == tagKey:
                        tag = volume_keys['Value']
                        volume_id = volume_id_resp
                        if volume_id == volume_to_tag:
                            set_snap_tag = boto3.resource('ec2', region_name=region).Snapshot(snapshot_id).create_tags(Tags=[
                                {
                                    'Key': tagKey,
                                    'Value': tag
                                }
                            ])

print("Done!")

