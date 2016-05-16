import boto3


def main():
    list_instances()


def create_instance():
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    ec2.create_instances()


def list_running_instances():
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        print(instance.id, instance.instance_type)


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
