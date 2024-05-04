import boto3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AwsManager:
    def __init__(self, region_name='us-east-1'):
        self.ec2 = boto3.resource('ec2', region_name=region_name)
        self.ec2_client = boto3.client('ec2', region_name=region_name)
        self.s3 = boto3.client('s3', region_name=region_name)
        self.iam = boto3.client('iam', region_name=region_name)
        self.dynamodb = boto3.client('dynamodb', region_name=region_name)

    def list_instances(self):
        try:
            instances = self.ec2.instances.filter(
                Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'stopped']}])
            for instance in instances:
                logger.info(f"ID: {instance.id}, Type: {instance.instance_type}, State: {instance.state['Name']}")
        except boto3.exceptions.Boto3Error as e:
            logger.error(f"Failed to list instances: {e}")

    def start_instance(self, instance_id):
        try:
            self.ec2_client.start_instances(InstanceIds=[instance_id])
            logger.info(f"Instance {instance_id} started.")
        except boto3.exceptions.Boto3Error as e:
            logger.error(f"Failed to start instance {instance_id}: {e}")

    def stop_instance(self, instance_id):
        try:
            self.ec2_client.stop_instances(InstanceIds=[instance_id])
            logger.info(f"Instance {instance_id} stopped.")
        except boto3.exceptions.Boto3Error as e:
            logger.error(f"Failed to stop instance {instance_id}: {e}")

    def terminate_instance(self, instance_id):
        try:
            self.ec2_client.terminate_instances(InstanceIds=[instance_id])
            logger.info(f"Instance {instance_id} terminated.")
        except boto3.exceptions.Boto3Error as e:
            logger.error(f"Failed to terminate instance {instance_id}: {e}")

    def list_buckets(self):
        try:
            response = self.s3.list_buckets()
            for bucket in response['Buckets']:
                logger.info(f"Bucket Name: {bucket['Name']}")
        except boto3.exceptions.Boto3Error as e:
            logger.error(f"Failed to list buckets: {e}")

    def create_bucket(self, bucket_name, region=None):
        try:
            if region is None:
                self.s3.create_bucket(Bucket=bucket_name)
            else:
                self.s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
            logger.info(f"Bucket {bucket_name} created.")
        except boto3.exceptions.Boto3Error as e:
            logger.error(f"Failed to create bucket {bucket_name}: {e}")

    def list_users(self):
        try:
            response = self.iam.list_users()
            for user in response['Users']:
                logger.info(f"User: {user['UserName']}, ARN: {user['Arn']}")
        except boto3.exceptions.Boto3Error as e:
            logger.error(f"Failed to list IAM users: {e}")

# Example usage
if __name__ == "__main__":
    aws_manager = AwsManager(region_name='your-region-here')
    aws_manager.list_instances()
    # Call other methods as needed
