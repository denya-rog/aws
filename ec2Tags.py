# This script copies tag value of specified tag key of ec2 instance
# to volumes and network interfaces attached to the instance.

import boto3

# Edit parameters:
tagKey = 'End User' #Tag key of an instance you need to copy to its volumes and network interfaces
region = 'us-east-1'

# Do not edit below
ec2 = boto3.resource('ec2', region_name=region).instances.all()
request_get = boto3.client('ec2',region_name=region)
filters = [{'Name':'tag-key','Values':[tagKey]}]
response = request_get.describe_instances(Filters=filters)["Reservations"]
instance_id = ''

for group in response:
    instances = group['Instances']
    for id in instances:
        instance_id = id['InstanceId']
        #print(instance_id)

        # finding value of the tag key
        tags = id['Tags']
        for t in tags:
            q = t['Key']
            j = t['Value']
            if q == tagKey:
                tag = j
        #print(tag)

        # copying tag key and value to volumes
        volumes = id['BlockDeviceMappings']
        for values in volumes:
            ebs = values['Ebs']
            volume_id = ebs['VolumeId']
            kek = boto3.resource('ec2', region_name=region).Volume(volume_id).create_tags(Tags=[
                {
                    'Key': tagKey,
                    'Value': tag
                },
            ])
            #print(volume_id)

        # copying tag key and value to network interfaces
        networks = id['NetworkInterfaces']
        for interfaces in networks:
            eni_id = interfaces['NetworkInterfaceId']
            kek = boto3.resource('ec2', region_name=region).Volume(eni_id).create_tags(Tags=[
                {
                    'Key': tagKey,
                    'Value': tag
                },
            ])
            #print(eni_id)
print("Done!")