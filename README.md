PyDevOps: AWS Management Library
Welcome to pydevops, a comprehensive Python library designed to streamline the management of AWS resources. This library allows you to efficiently handle operations across EC2 instances, manage IAM policies, and oversee general AWS resource management.

Installation
To get started with pydevops, install the package using pip:

bash
Copy code
pip install pydevops
Modules Overview
pydevops includes the following modules to assist in managing AWS services:

1. AwsManager
General AWS resource management with support for multiple services such as EC2, S3, IAM, and DynamoDB.

Functions:
list_instances(): Lists all EC2 instances.
create_bucket(bucket_name, region): Creates an S3 bucket in a specified region.
list_users(): Lists all IAM users.
Example:
python
Copy code
from pydevops import AwsManager

# Initialize manager
aws_manager = AwsManager(region_name='us-east-1')

# List EC2 instances
aws_manager.list_instances()

# Create an S3 bucket
aws_manager.create_bucket('my-new-bucket', 'us-east-1')
2. EC2Manager
Focused management of EC2 instances, enabling detailed instance monitoring and interaction.

Functions:
list_instances(): Retrieves all instances with their detailed information.
send_command_to_instance(instance_id, command): Sends a command to a specified instance via AWS SSM.
get_command_result(instance_id, command_id): Fetches the result of a command executed on an instance.
Example:
python
Copy code
from pydevops import EC2Manager

# Initialize EC2 manager
ec2_manager = EC2Manager(credentials_path='/secure/path/to/credentials', region='us-east-1')

# List instances
instances = ec2_manager.list_instances()
print(instances)

# Execute a command on an instance
command_id = ec2_manager.send_command_to_instance(instance_id='i-1234567890abcdef0', command='uptime')
result = ec2_manager.get_command_result('i-1234567890abcdef0', command_id)
print(result)
3. IAMManager
Management of IAM-related tasks, ensuring secure and efficient user and access key handling.

Functions:
list_users(): Lists all IAM users with their attributes.
list_old_keys(months_old=3): Identifies IAM keys that are older than the specified number of months.
Example:
python
Copy code
from pydevops import IAMManager

# Initialize IAM manager
iam_manager = IAMManager(region_name='us-west-2')

# List IAM users
users = iam_manager.list_users()
print(users)

# List old access keys
old_keys = iam_manager.list_old_keys(months_old=6)
print(old_keys)
Contributing
Contributions to pydevops are always welcome! Please feel free to fork the repository, make your changes, and submit a pull request.

License
pydevops is released under the MIT License. See the LICENSE file in the repository for more details.