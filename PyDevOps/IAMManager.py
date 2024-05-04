import boto3
import logging
from datetime import datetime, timedelta

class IAMManager:
    def __init__(self, region_name='us-east-1'):
        self.iam = boto3.client('iam', region_name=region_name)
        self.logger = logging.getLogger(__name__)

    def list_old_keys(self, months_old=3):
        try:
            threshold_date = datetime.now() - timedelta(days=30 * months_old)
            users = self.iam.list_users()
            result = []
            for user in users['Users']:
                keys_response = self.iam.list_access_keys(UserName=user['UserName'])
                for key in keys_response['AccessKeyMetadata']:
                    key_creation_date = key['CreateDate']
                    age = (datetime.now() - key_creation_date).days / 30
                    key_last_used_info = self.iam.get_access_key_last_used(AccessKeyId=key['AccessKeyId'])

                    key_info = {
                        'Key ID': key['AccessKeyId'],
                        'User': user['UserName'],
                        'Creation Date': key_creation_date,
                        'Age in Months': round(age, 2),
                        'Last Used Date': key_last_used_info.get('AccessKeyLastUsed', {}).get('LastUsedDate', 'Never'),
                        'Permissions': self.get_key_permissions(key['AccessKeyId'])
                    }
                    if key_creation_date < threshold_date:
                        result.append(key_info)
                        self.logger.info(f"Old key found: {key_info}")

            return result
        except boto3.exceptions.Boto3Error as e:
            self.logger.error(f"Failed to list or evaluate IAM keys: {e}")
            return None

    def get_key_permissions(self, access_key_id):
        # This would need a custom implementation that checks attached policies
        # and any inline policies directly attached to the user.
        # This is a placeholder and needs a detailed implementation based on your AWS setup.
        return "List of permissions"

# Example usage:
if __name__ == "__main__":
    iam_manager = IAMManager(region_name='your-region-here')
    old_keys = iam_manager.list_old_keys(months_old=3)
    for key in old_keys:
        print(key)
