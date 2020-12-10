# This script copies tag value of specified tag key of ec2 instance
# to volumes and network interfaces attached to the instance.

import boto3

tagKey = input('Input tag key: ') #Tag key of an instance you need to copy to its volumes and network interfaces
region = input('Input region name (example: us-east-1): ')


# Do not edit below
ec2 = boto3.resource('ec2', region_name=region).instances.all()
request_get = boto3.client('ec2',region_name=region)
filters = [{'Name':'tag-key','Values':[tagKey]}]
response = request_get.describe_instances(Filters=filters)["Reservations"]
instance_id = ''

for group in response:
    instances = group['Instances']
    for id_list in instances:
        instance_id = id_list['InstanceId']

        # finding value of the tag key
        tags = id_list['Tags']
        for tag_values in tags:
            key_value = tag_values['Key']
            value_value = tag_values['Value']
            if key_value == tagKey:
                tag = value_value

        # copying tag key and value to volumes
        volumes = id_list['BlockDeviceMappings']
        for v_values in volumes:
            ebs = v_values['Ebs']
            volume_id = ebs['VolumeId']
            set_tags = boto3.resource('ec2', region_name=region).Volume(volume_id).create_tags(Tags=[
                {
                    'Key': tagKey,
                    'Value': tag
                },
            ])

        # copying tag key and value to network interfaces
        networks = id_list['NetworkInterfaces']
        for interfaces in networks:
            eni_id = interfaces['NetworkInterfaceId']
            set_tags = boto3.resource('ec2', region_name=region).Volume(eni_id).create_tags(Tags=[
                {
                    'Key': tagKey,
                    'Value': tag
                },
            ])
print("Done!")