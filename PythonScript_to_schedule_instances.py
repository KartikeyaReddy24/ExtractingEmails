import boto3
import time
from datetime import datetime

now = datetime.now()


class InstanceHandler:

    AWS_REGION = "us-east-1"
    KEY_PAIR_NAME = 'Kartik_New'
    AMI_ID = 'ami-0afbd8b73fc58f69a' # Amazon Linux 2
    SUBNET_ID = 'subnet-ba1508f7'
    SECURITY_GROUP_ID = 'sg-0dfde60a3c6696001'
    INSTANCE_PROFILE =  'Boto3_admin'

    USER_DATA = '''#!/bin/bash
    chmod +x /home/ubuntu/script.sh
    ./home/ubuntu/script.sh
    '''
    
    def __init__(self):
        self.ec2_resource=boto3.resource('ec2', region_name=InstanceHandler.AWS_REGION)
        self.ec2_client=boto3.client('ec2',region_name=InstanceHandler.AWS_REGION)    

    def create_ec2_instances(self):
        instances = self.ec2_resource.create_instances(
            MinCount = 1,
            MaxCount = 64,
            ImageId=InstanceHandler.AMI_ID,
            InstanceType='t2.micro',
            KeyName=InstanceHandler.KEY_PAIR_NAME,
            SecurityGroupIds=[
                InstanceHandler.SECURITY_GROUP_ID,
            ],
            SubnetId=InstanceHandler.SUBNET_ID,
            UserData=InstanceHandler.USER_DATA,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'testo'
                        },
                    ]
                },
            ]
        )

    def termination_ec2_instances(self):
        instance_ids=[]
        for reservation in self.ec2_client.describe_instances()['Reservations']:
            for instance in reservation['Instances']:
                if instance['InstanceType'].lower()=='t2.micro':
                    instance_ids.append(instance['InstanceId'])

        print(instance_ids)

        response = self.ec2_client.terminate_instances(
            InstanceIds=instance_ids
        )
        print(response)
    
    def countdown(self,t):
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1
        
        print('\n\t\t\tFire in the hole!!')


while(True):
    instanceHandler = InstanceHandler() 
    instanceHandler.create_ec2_instances()
    print("\nCreated containers")
    instanceHandler.countdown(3600)
    instanceHandler.termination_ec2_instances()
    print("\nTerminated containers.... wait for next one hour to start new containers")
    instanceHandler.countdown(3600)






# current_time = now.strftime("%H:%M:%S")
# print("\n\t\t\tStarting time: ",current_time)
# # print("\n\t\t\tClosing the instances: ",current_time)

    # print("\n\t\t\tThe instances will terminate in: ",instanceHandler.countdown(20))

    # print("\n\t\t\tThe new instances will be crated in: ",instanceHandler.countdown(30))
