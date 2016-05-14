import boto3


def main():
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
