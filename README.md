PyDevOps: AWS Management Library
pydevops is a Python library designed to facilitate the management of AWS resources within a DevOps context. This library provides a set of tools to manage EC2 instances, handle IAM operations, and oversee general AWS resource management efficiently and securely.

Installation
bash
Copy code
pip install pydevops  # Placeholder for actual installation command
Modules
1. AwsManager
The AwsManager class is designed for general AWS resource management, providing functionalities to interact with multiple AWS services like EC2, S3, IAM, and DynamoDB.

Features:
Start, stop, and terminate EC2 instances.
List and create S3 buckets.
Manage IAM users and their access keys.
Example Usage:
python
Copy code
from pydevops import AwsManager

aws_manager = AwsManager(region_name='us-east-1')
aws_manager.list_instances()
aws_manager.create_bucket('my-new-bucket')
2. EC2Manager
EC2Manager focuses specifically on managing AWS EC2 instances, facilitating operations such as listing, monitoring, and executing system commands via AWS SSM.

Features:
List all EC2 instances.
Send commands to instances using SSM.
Retrieve and handle outputs from these commands.
Example Usage:
python
Copy code
from pydevops import EC2Manager

ec2_manager = EC2Manager(credentials_path='/path/to/credentials', region='us-east-1')
instances = ec2_manager.list_instances()
print(instances)

command_id = ec2_manager.send_command_to_instance(instance_id='i-1234567890abcdef0', command='uptime')
result = ec2_manager.get_command_result('i-1234567890abcdef0', command_id)
print(result)
3. IAMManager
IAMManager is tailored for managing AWS Identity and Access Management (IAM) tasks, such as user and access key management.

Features:
List IAM users and their details.
Find old access keys and analyze their permissions.
Securely manage IAM configurations.
Example Usage:
python
Copy code
from pydevops import IAMManager

iam_manager = IAMManager(region_name='us-east-1')
users = iam_manager.list_users()
print(users)

old_keys = iam_manager.list_old_keys(months_old=6)
print(old_keys)
Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your new features or fixes.

License
Distributed under the MIT License. See LICENSE file for more information.

Contact
Your Name - Your Email - Your Twitter/GitHub
