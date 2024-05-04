import boto3

class AwsManager:
    def __init__(self, region_name='us-east-1'):
        self.ec2 = boto3.resource('ec2', region_name=region_name)
        self.ec2_client = boto3.client('ec2', region_name=region_name)
        self.s3 = boto3.client('s3', region_name=region_name)
        self.iam = boto3.client('iam', region_name=region_name)
        self.dynamodb = boto3.client('dynamodb', region_name=region_name)

    def list_instances(self):
        instances = self.ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'stopped']}])
        for instance in instances:
            print(f"ID: {instance.id}, Type: {instance.instance_type}, State: {instance.state['Name']}")

    def start_instance(self, instance_id):
        self.ec2_client.start_instances(InstanceIds=[instance_id])
        print(f"Instance {instance_id} started.")

    def stop_instance(self, instance_id):
        self.ec2_client.stop_instances(InstanceIds=[instance_id])
        print(f"Instance {instance_id} stopped.")

    def terminate_instance(self, instance_id):
        self.ec2_client.terminate_instances(InstanceIds=[instance_id])
        print(f"Instance {instance_id} terminated.")

    def list_buckets(self):
        response = self.s3.list_buckets()
        for bucket in response['Buckets']:
            print(f"Bucket Name: {bucket['Name']}")

    def create_bucket(self, bucket_name, region=None):
        if region is None:
            self.s3.create_bucket(Bucket=bucket_name)
        else:
            self.s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
        print(f"Bucket {bucket_name} created.")

    def list_users(self):
        response = self.iam.list_users()
        for user in response['Users']:
            print(f"User: {user['UserName']}, ARN: {user['Arn']}")

    # Add more methods here based on the suggested methods

# Example usage
if __name__ == "__main__":
    aws_manager = AwsManager(region_name='your-region-here')
    aws_manager.list_instances()
    # Call other methods as needed
