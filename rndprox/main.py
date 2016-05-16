import boto3


def main():
    # terminate_instance()
    create_instance()
    # list_instances()


def create_instance():
    client = boto3.client('ec2', region_name='us-east-1')
    reservation = client.run_instances(
            ImageId='ami-fce3c696',
            MinCount=1,
            MaxCount=1,
            KeyName='proxy-manager',
            InstanceType='t2.nano',
            Placement={
                'AvailabilityZone': 'us-east-1a'
            }
    )
    instance_id = reservation['Instances'][0]['InstanceId']
    while True:
        states = client.describe_instance_status(InstanceIds=[instance_id])['InstanceStatuses']
        if len(states) < 1:
            print("No instances returned")
            return
        state = states[0]['InstanceState']
        if state == 'running':
            break
    client.create_tags(
            Resources=[instance_id],
            Tags=[{
                'Key': 'Name',
                'Value': 'proxy-manager'
            }]
    )


def terminate_instance():
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    client = boto3.client('ec2', region_name='us-east-1')
    for i in ec2.instances.all():
        if i.tags is None:
            continue
        for t in i.tags:
            if t['Key'] == 'Name' and t['Value'] == 'proxy-manager' and i.state['Name'] == 'running':
                print("Terminating: {0} / {1} {2} ({3}) - [{4}]".format(
                        'us-east-1', i.id, t['Value'], i.instance_type, i.state['Name']
                ))
                client.stop_instances(InstanceIds=[i.id])
                client.terminate_instances(InstanceIds=[str(i.id)])
                break


def get_image_id():
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    return ec2.describe_images(Filters=[{'name': 'Ubuntu', 'architecture': 'x86_64'}])


def list_running_instances():
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    for i in ec2.instances.all():
        if i.tags is None:
            print('No tags')
            continue
        for t in i.tags:
            if t['Key'] == 'Name' and i.state['Name'] == 'running':
                print("{0} / {1} {2} ({3}) - [{4}]".format(
                        'us-east-1', i.id, t['Value'], i.instance_type, i.state['Name']
                ))


def list_instances():
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    for i in ec2.instances.all():
        if i.tags is None:
            print('No tags')
            continue
        for t in i.tags:
            if t['Key'] == 'Name':
                print("{0} / {1} {2} ({3}) - [{4}]".format(
                        'us-east-1', i.id, t['Value'], i.instance_type, i.state['Name']
                ))


if __name__ == '__main__':
    main()
