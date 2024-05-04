import boto3
import pandas as pd
import os
from botocore.exceptions import ClientError
from cryptography.fernet import Fernet
import time
import logging
from datetime import datetime
from io import StringIO

class EC2Manager:
    """
    A class to manage AWS EC2 instances and execute commands using SSM.

    Attributes:
        aws_access_key_id (str): AWS access key ID.
        aws_secret_access_key (str): AWS secret access key.
        region (str): AWS region name.
        ec2 (boto3.client): Boto3 EC2 client.
        ssm (boto3.client): Boto3 SSM client.
    """

    def __init__(self, credentials_path, region):
        """
        Initializes the EC2Manager with credentials and region.

        Parameters:
            credentials_path (str): Path to the encrypted credentials file.
            region (str): AWS region to configure the services.
        """
        self.aws_access_key_id, self.aws_secret_access_key = self.decrypt_credentials(credentials_path)
        self.region = region
        self.ec2 = boto3.client('ec2', aws_access_key_id=self.aws_access_key_id,
                                aws_secret_access_key=self.aws_secret_access_key, region_name=self.region)
        self.ssm = boto3.client('ssm', aws_access_key_id=self.aws_access_key_id,
                                aws_secret_access_key=self.aws_secret_access_key, region_name=self.region)

    def decrypt_credentials(self, credentials_path):
        """
        Decrypts credentials stored at a given path.

        Parameters:
            credentials_path (str): Path to the encrypted credentials file.

        Returns:
            tuple: A tuple containing AWS access key ID and secret access key.
        """
        # Placeholder for decryption logic
        return "YOUR_ACCESS_KEY", "YOUR_SECRET_KEY"  # Should replace with actual decryption logic

    def list_instances(self):
        """
        Lists all EC2 instances in the specified region.

        Returns:
            list: A list of dictionaries, each containing details of an EC2 instance.
        """
        try:
            response = self.ec2.describe_instances()
            instances = []
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instances.append(instance)
            return instances
        except ClientError as e:
            print(f"An error occurred: {e}")
            return []

    def send_command_to_instance(self, instance_id, command):
        """
        Sends a command to an EC2 instance using SSM.

        Parameters:
            instance_id (str): ID of the EC2 instance.
            command (str): Shell command to execute on the instance.

        Returns:
            str: Command ID if successful, None otherwise.
        """
        try:
            response = self.ssm.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunShellScript",
                Parameters={'commands': [command]}
            )
            return response['Command']['CommandId']
        except ClientError as e:
            print(f"Error sending command to {instance_id}: {e}")
            return None

    def get_command_result(self, instance_id, command_id):
        """
        Retrieves the result of a command executed on an EC2 instance.

        Parameters:
            instance_id (str): ID of the EC2 instance.
            command_id (str): ID of the command sent to the instance.

        Returns:
            dict: A dictionary containing the status and output of the command.
        """
        try:
            output = self.ssm.get_command_invocation(
                CommandId=command_id,
                InstanceId=instance_id
            )
            return {
                'InstanceId': instance_id,
                'Status': output['Status'],
                'Output': output['StandardOutputContent']
            }
        except ClientError as e:
            print(f"Error getting command result for {instance_id} with command ID {command_id}: {e}")
            return {'InstanceId': instance_id, 'Status': 'Error', 'Output': str(e)}

    def run_commands_on_instances(self, instances, commands):
        """
        Executes a list of commands on a list of instances.

        Parameters:
            instances (list): A list of instance IDs.
            commands (list): A list of commands to execute.

        Returns:
            pd.DataFrame: A DataFrame containing the results of the executed commands.
        """
        results = []
        for instance_id in instances:
            for command in commands:
                command_id = self.send_command_to_instance(instance_id, command)
                if command_id:
                    time.sleep(2)  # Delay for command execution
                    result = self.get_command_result(instance_id, command_id)
                    results.append(result)
        return pd.DataFrame(results)

    @staticmethod
    def create_folder(folder_name, path):
        """
        Creates a folder at a specified path.

        Parameters:
            folder_name (str): The name of the folder to create.
            path (str): The path where the folder will be created.
        """
        folder_path = os.path.join(path, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder created successfully at: {folder_path}")
        else:
            print(f"Folder already exists at: {folder_path}")
