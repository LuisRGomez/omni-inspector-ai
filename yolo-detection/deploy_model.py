"""
Deploy YOLOv11 model to SageMaker Serverless Endpoint

This script:
1. Downloads YOLOv11 model
2. Packages it for SageMaker
3. Uploads to S3
4. Creates SageMaker model
5. Creates serverless endpoint configuration
6. Deploys endpoint

Note: For MVP, we use YOLOv11 base model (pre-trained).
Fine-tuning with custom data is optional and can be done later.
"""

import boto3
import json
import tarfile
import time
from pathlib import Path
import subprocess
import sys


class YOLODeployer:
    """Deploy YOLO model to SageMaker"""
    
    def __init__(self, config_path='sagemaker_config.json'):
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Initialize AWS clients
        self.s3 = boto3.client('s3', region_name=self.config['region'])
        self.sagemaker = boto3.client('sagemaker', region_name=self.config['region'])
        
        self.model_bucket = self.config['model_bucket']
        self.role_arn = self.config['role_arn']
        self.endpoint_name = self.config['endpoint_name']
    
    def install_ultralytics(self):
        """Install ultralytics if not already installed"""
        print("📦 Checking ultralytics installation...")
        
        try:
            import ultralytics
            print("✅ ultralytics already installed")
            return True
        except ImportError:
            print("⏳ Installing ultralytics...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "ultralytics==8.1.0", "--quiet"])
            print("✅ ultralytics installed")
            return True
    
    def download_yolo_model(self):
        """Download YOLOv11 base model"""
        print("\n📥 Downloading YOLOv11 model...")
        
        from ultralytics import YOLO
        
        # Download YOLOv11n (nano - fastest, good for serverless)
        model = YOLO('yolov11n.pt')
        
        print("✅ YOLOv11n model downloaded")
        return 'yolov11n.pt'
    
    def package_model(self, model_path):
        """Package model for SageMaker"""
        print("\n📦 Packaging model for SageMaker...")
        
        # Create model directory
        model_dir = Path('model')
        model_dir.mkdir(exist_ok=True)
        
        # Copy model file
        import shutil
        shutil.copy(model_path, model_dir / 'yolov11n.pt')
        
        # Create inference script
        inference_script = model_dir / 'inference.py'
        inference_script.write_text('''
import json
import torch
from ultralytics import YOLO

# Load model
model = None

def model_fn(model_dir):
    """Load model"""
    global model
    model = YOLO(f"{model_dir}/yolov11n.pt")
    return model

def input_fn(request_body, content_type):
    """Parse input"""
    if content_type == 'application/json':
        data = json.loads(request_body)
        return data['image_path']
    raise ValueError(f"Unsupported content type: {content_type}")

def predict_fn(image_path, model):
    """Run inference"""
    results = model(image_path)
    
    detections = []
    for result in results:
        boxes = result.boxes
        for box in boxes:
            detections.append({
                'class': int(box.cls[0]),
                'confidence': float(box.conf[0]),
                'bbox': box.xyxy[0].tolist()
            })
    
    return detections

def output_fn(prediction, accept):
    """Format output"""
    if accept == 'application/json':
        return json.dumps(prediction), accept
    raise ValueError(f"Unsupported accept type: {accept}")
''')
        
        # Create requirements.txt
        requirements = model_dir / 'requirements.txt'
        requirements.write_text('''ultralytics==8.1.0
torch==2.2.0
opencv-python-headless==4.9.0.80
''')
        
        # Create tar.gz
        tar_path = 'model.tar.gz'
        with tarfile.open(tar_path, 'w:gz') as tar:
            tar.add(model_dir, arcname='.')
        
        print(f"✅ Model packaged: {tar_path}")
        return tar_path
    
    def upload_to_s3(self, tar_path):
        """Upload model to S3"""
        print(f"\n📤 Uploading model to S3...")
        
        s3_key = 'yolo/model.tar.gz'
        
        self.s3.upload_file(
            tar_path,
            self.model_bucket,
            s3_key
        )
        
        s3_uri = f"s3://{self.model_bucket}/{s3_key}"
        print(f"✅ Model uploaded: {s3_uri}")
        return s3_uri
    
    def create_sagemaker_model(self, model_data_url):
        """Create SageMaker model"""
        print("\n🤖 Creating SageMaker model...")
        
        model_name = f"{self.endpoint_name}-model"
        
        # Check if model exists
        try:
            self.sagemaker.describe_model(ModelName=model_name)
            print(f"✅ Model already exists: {model_name}")
            return model_name
        except self.sagemaker.exceptions.ClientError:
            pass
        
        # PyTorch inference container
        # For YOLOv11, we use PyTorch 2.0 container
        container = f"763104351884.dkr.ecr.{self.config['region']}.amazonaws.com/pytorch-inference:2.0.0-cpu-py310"
        
        response = self.sagemaker.create_model(
            ModelName=model_name,
            PrimaryContainer={
                'Image': container,
                'ModelDataUrl': model_data_url,
                'Environment': {
                    'SAGEMAKER_PROGRAM': 'inference.py',
                    'SAGEMAKER_SUBMIT_DIRECTORY': model_data_url
                }
            },
            ExecutionRoleArn=self.role_arn
        )
        
        print(f"✅ SageMaker model created: {model_name}")
        return model_name
    
    def create_endpoint_config(self, model_name):
        """Create serverless endpoint configuration"""
        print("\n⚙️  Creating endpoint configuration...")
        
        config_name = f"{self.endpoint_name}-config"
        
        # Check if config exists
        try:
            self.sagemaker.describe_endpoint_config(EndpointConfigName=config_name)
            print(f"✅ Endpoint config already exists: {config_name}")
            return config_name
        except self.sagemaker.exceptions.ClientError:
            pass
        
        response = self.sagemaker.create_endpoint_config(
            EndpointConfigName=config_name,
            ProductionVariants=[
                {
                    'VariantName': 'AllTraffic',
                    'ModelName': model_name,
                    'ServerlessConfig': {
                        'MemorySizeInMB': 2048,  # 2GB memory
                        'MaxConcurrency': 5      # Max concurrent requests
                    }
                }
            ]
        )
        
        print(f"✅ Endpoint config created: {config_name}")
        return config_name
    
    def create_endpoint(self, config_name):
        """Create SageMaker endpoint"""
        print("\n🚀 Creating SageMaker endpoint...")
        print("⏳ This may take 5-10 minutes...")
        
        # Check if endpoint exists
        try:
            response = self.sagemaker.describe_endpoint(EndpointName=self.endpoint_name)
            status = response['EndpointStatus']
            
            if status == 'InService':
                print(f"✅ Endpoint already in service: {self.endpoint_name}")
                return self.endpoint_name
            elif status in ['Creating', 'Updating']:
                print(f"⏳ Endpoint is {status}...")
                self.wait_for_endpoint()
                return self.endpoint_name
            else:
                print(f"⚠️  Endpoint exists but status is: {status}")
                return self.endpoint_name
        except self.sagemaker.exceptions.ClientError:
            pass
        
        # Create endpoint
        response = self.sagemaker.create_endpoint(
            EndpointName=self.endpoint_name,
            EndpointConfigName=config_name
        )
        
        print(f"✅ Endpoint creation started: {self.endpoint_name}")
        
        # Wait for endpoint to be in service
        self.wait_for_endpoint()
        
        return self.endpoint_name
    
    def wait_for_endpoint(self):
        """Wait for endpoint to be in service"""
        print("\n⏳ Waiting for endpoint to be in service...")
        
        while True:
            response = self.sagemaker.describe_endpoint(EndpointName=self.endpoint_name)
            status = response['EndpointStatus']
            
            if status == 'InService':
                print("✅ Endpoint is in service!")
                break
            elif status == 'Failed':
                print("❌ Endpoint creation failed!")
                print(f"   Reason: {response.get('FailureReason', 'Unknown')}")
                break
            else:
                print(f"   Status: {status}... (waiting 30s)")
                time.sleep(30)
    
    def deploy(self):
        """Run complete deployment"""
        print("=" * 70)
        print("YOLO MODEL DEPLOYMENT TO SAGEMAKER")
        print("=" * 70)
        print()
        
        try:
            # Step 1: Install ultralytics
            self.install_ultralytics()
            
            # Step 2: Download YOLO model
            model_path = self.download_yolo_model()
            
            # Step 3: Package model
            tar_path = self.package_model(model_path)
            
            # Step 4: Upload to S3
            model_data_url = self.upload_to_s3(tar_path)
            
            # Step 5: Create SageMaker model
            model_name = self.create_sagemaker_model(model_data_url)
            
            # Step 6: Create endpoint configuration
            config_name = self.create_endpoint_config(model_name)
            
            # Step 7: Create endpoint
            endpoint_name = self.create_endpoint(config_name)
            
            print()
            print("=" * 70)
            print("DEPLOYMENT COMPLETE!")
            print("=" * 70)
            print()
            print(f"✅ Endpoint Name: {endpoint_name}")
            print(f"✅ Region: {self.config['region']}")
            print(f"✅ Model: YOLOv11n (base, pre-trained)")
            print()
            print("Next steps:")
            print("1. Test detection:")
            print("   python cli.py detect test_image.jpg")
            print()
            print("2. Run complete pipeline:")
            print("   cd ..")
            print("   .\\test-complete-pipeline.ps1")
            print()
            print("Note: This uses YOLOv11 base model (pre-trained).")
            print("For better accuracy on containers, you can fine-tune later.")
            print()
            
        except Exception as e:
            print(f"\n❌ Deployment failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        return True


def main():
    deployer = YOLODeployer()
    success = deployer.deploy()
    
    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()
