"""
Setup AWS SageMaker infrastructure for YOLO detection
Creates IAM roles, S3 buckets, and prepares for model deployment
"""

import boto3
import json
import time
from pathlib import Path


class SageMakerSetup:
    """Setup SageMaker infrastructure"""
    
    def __init__(self, aws_profile='omni-inspector', region='us-east-1'):
        session = boto3.Session(profile_name=aws_profile, region_name=region)
        self.iam = session.client('iam')
        self.s3 = session.client('s3')
        self.sagemaker = session.client('sagemaker')
        self.sts = session.client('sts')
        self.region = region
        
        # Get account ID
        self.account_id = self.sts.get_caller_identity()['Account']
    
    def create_sagemaker_role(self):
        """Create IAM role for SageMaker"""
        role_name = 'OmniInspectorSageMakerRole'
        
        # Trust policy
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "sagemaker.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        
        # Check if role exists
        try:
            role = self.iam.get_role(RoleName=role_name)
            print(f"✅ Role already exists: {role_name}")
            return role['Role']['Arn']
        except self.iam.exceptions.NoSuchEntityException:
            pass
        
        # Create role
        print(f"Creating IAM role: {role_name}...")
        role = self.iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Role for Omni-Inspector SageMaker endpoints'
        )
        
        # Attach policies
        policies = [
            'arn:aws:iam::aws:policy/AmazonSageMakerFullAccess',
            'arn:aws:iam::aws:policy/AmazonS3FullAccess'
        ]
        
        for policy_arn in policies:
            self.iam.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )
        
        print(f"✅ Role created: {role['Role']['Arn']}")
        print("⏳ Waiting for role to propagate...")
        time.sleep(10)  # Wait for IAM propagation
        
        return role['Role']['Arn']
    
    def create_model_bucket(self):
        """Create S3 bucket for YOLO models"""
        bucket_name = f'omni-inspector-models-{self.account_id}'
        
        # Check if bucket exists
        try:
            self.s3.head_bucket(Bucket=bucket_name)
            print(f"✅ Bucket already exists: {bucket_name}")
            return bucket_name
        except:
            pass
        
        # Create bucket
        print(f"Creating S3 bucket: {bucket_name}...")
        
        if self.region == 'us-east-1':
            self.s3.create_bucket(Bucket=bucket_name)
        else:
            self.s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': self.region}
            )
        
        # Enable versioning
        self.s3.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={'Status': 'Enabled'}
        )
        
        # Enable encryption
        self.s3.put_bucket_encryption(
            Bucket=bucket_name,
            ServerSideEncryptionConfiguration={
                'Rules': [{
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256'
                    }
                }]
            }
        )
        
        print(f"✅ Bucket created: {bucket_name}")
        return bucket_name
    
    def check_endpoint(self, endpoint_name='omni-inspector-yolo'):
        """Check if SageMaker endpoint exists"""
        try:
            response = self.sagemaker.describe_endpoint(EndpointName=endpoint_name)
            status = response['EndpointStatus']
            print(f"✅ Endpoint exists: {endpoint_name}")
            print(f"   Status: {status}")
            return True
        except self.sagemaker.exceptions.ClientError:
            print(f"❌ Endpoint not found: {endpoint_name}")
            return False
    
    def setup_all(self):
        """Run complete setup"""
        print("=" * 70)
        print("SAGEMAKER SETUP")
        print("=" * 70)
        print()
        
        print(f"Account ID: {self.account_id}")
        print(f"Region: {self.region}")
        print()
        
        # Create IAM role
        role_arn = self.create_sagemaker_role()
        print()
        
        # Create S3 bucket
        bucket_name = self.create_model_bucket()
        print()
        
        # Check endpoint
        self.check_endpoint()
        print()
        
        # Save configuration
        config = {
            'account_id': self.account_id,
            'region': self.region,
            'role_arn': role_arn,
            'model_bucket': bucket_name,
            'endpoint_name': 'omni-inspector-yolo'
        }
        
        config_path = Path(__file__).parent / 'sagemaker_config.json'
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Configuration saved to: {config_path}")
        print()
        
        print("=" * 70)
        print("SETUP COMPLETE")
        print("=" * 70)
        print()
        print("Next steps:")
        print("1. Deploy YOLO model:")
        print("   python deploy_model.py")
        print()
        print("2. Test detection:")
        print("   python cli.py detect test_image.jpg")
        print()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Setup SageMaker infrastructure')
    parser.add_argument('--profile', default='omni-inspector', help='AWS profile')
    parser.add_argument('--region', default='us-east-1', help='AWS region')
    parser.add_argument('--check-endpoint', action='store_true', help='Only check endpoint')
    
    args = parser.parse_args()
    
    setup = SageMakerSetup(aws_profile=args.profile, region=args.region)
    
    if args.check_endpoint:
        setup.check_endpoint()
    else:
        setup.setup_all()


if __name__ == '__main__':
    main()
