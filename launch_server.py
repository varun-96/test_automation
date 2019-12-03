import boto3
import os.path as op
from configparser import ConfigParser


def get_config():
    """
    Read configuration file and returns it as an ordered Dict'

    Returns
    ------
    config : Ordered Dict
        contains parameter values for each file

    """
    config = ConfigParser()
    config.read(op.join(op.dirname(op.abspath(__file__)), "config.ini"))
    return config


cfg = get_config()

# Read EC2 bootstrap script as userdata
with open(op.join(op.dirname(op.abspath(__file__)), "bootstrap.sh"), "r") as bootstrap_f:
    userdata = bootstrap_f.read()

# Only launch EC2 instance when config.ini `trainable` param = True
if cfg.getboolean("automl", "trainable"):
    client = boto3.client("ec2", region_name="us-east-1")
    response = client.run_instances(
        BlockDeviceMappings=[
            {
                "DeviceName": "/dev/xvda",
                "Ebs": {
                    "DeleteOnTermination": True,
                    "VolumeSize": 16,
                    "VolumeType": "gp2",
                },
            },
        ],
        ImageId="ami-0b69ea66ff7391e80",
        InstanceType="t2.micro",
        KeyName="myprivatekey",
        MaxCount=1,
        MinCount=1,
        SecurityGroupIds=["sg-04fee80d6e3d35ba5"],
        SubnetId="subnet-bd8740f0",
        UserData=userdata,
        IamInstanceProfile={
            "Arn": "arn:aws:iam::221988645750:instance-profile/pydata_role"
        },
        InstanceInitiatedShutdownBehavior="terminate",
    )

    print(response)

else:
    print(
        "Didn't launch any server since `trainable` parameter" " in config file is set to False."
    )