# Phase 05.5: AWS Cloud - Ví Dụ Thực Tế

> **Mục tiêu:** Hands-on labs với AWS services

---

## 📁 BÀI 1: EC2 & AUTO SCALING

### Ví dụ 1.1: Launch EC2 instance với AWS CLI

```bash
# 1. Tạo key pair
aws ec2 create-key-pair --key-name my-app-key \
  --query 'KeyMaterial' --output text > my-app-key.pem
chmod 400 my-app-key.pem

# 2. Tạo security group
aws ec2 create-security-group \
  --group-name my-app-sg \
  --description "Security group for my app"

# 3. Authorize SSH access
aws ec2 authorize-security-group-ingress \
  --group-name my-app-sg \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0

# 4. Authorize HTTP access
aws ec2 authorize-security-group-ingress \
  --group-name my-app-sg \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

# 5. Launch EC2 instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --key-name my-app-key \
  --security-groups my-app-sg \
  --user-data file://user-data.sh \
  --tag-specifications 'ResourceType=instances,Tags=[{Key=Name,Value=my-app-server}]'

# 6. Get public IP
aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=my-app-server" \
  --query "Reservations[].Instances[].PublicIpAddress" \
  --output text

# 7. SSH vào instance
ssh -i my-app-key.pem ec2-user@<public-ip>
```

**user-data.sh** (auto-install software):
```bash
#!/bin/bash
yum update -y
yum install -y docker
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

# Install Java 17
amazon-linux-extras install java-openjdk17 -y

# Install Docker Compose
curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

---

### Ví dụ 1.2: Tạo Auto Scaling Group

```bash
# 1. Tạo launch template
aws ec2 create-launch-template \
  --launch-template-name my-app-template \
  --version-description v1 \
  --launch-template-data '{
    "ImageId": "ami-0c55b159cbfafe1f0",
    "InstanceType": "t3.micro",
    "KeyName": "my-app-key",
    "SecurityGroups": ["sg-xxxxx"],
    "UserData": "base64-encoded-user-data"
  }'

# 2. Tạo target group cho ALB
aws elbv2 create-target-group \
  --name my-app-tg \
  --protocol HTTP \
  --port 80 \
  --vpc-id vpc-xxxxx

# 3. Tạo Auto Scaling Group
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name my-app-asg \
  --launch-template LaunchTemplateName=my-app-template,Version=1 \
  --min-size 1 \
  --max-size 4 \
  --desired-capacity 2 \
  --target-group-arns arn:aws:elasticloadbalancing:... \
  --health-check-type ELB \
  --health-check-grace-period 300 \
  --availability-zones us-east-1a us-east-1b

# 4. Tạo scaling policy dựa trên CPU
aws autoscaling put-scaling-policy \
  --auto-scaling-group-name my-app-asg \
  --policy-name cpu-scale-up \
  --policy-type TargetTrackingScaling \
  --target-tracking-configuration '{
    "PredefinedMetricSpecification": {
      "PredefinedMetricType": "ASGAverageCPUUtilization"
    },
    "TargetValue": 70.0
  }'

# 5. Xem scaling activities
aws autoscaling describe-scaling-activities \
  --auto-scaling-group-name my-app-asg
```

---

## 📁 BÀI 2: LAMBDA & API GATEWAY

### Ví dụ 2.1: Tạo Lambda function với Python

```python
# lambda_function.py
import json
import boto3
from datetime import datetime

# Initialize clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Orders')

def lambda_handler(event, context):
    """
    Event types:
    - API Gateway: event['httpMethod'], event['body'], event['pathParameters']
    - S3: event['Records'][0]['s3']
    - EventBridge: event['source'], event['detail']
    """

    # API Gateway trigger
    if 'httpMethod' in event:
        return handle_api_request(event)

    # S3 trigger
    if 'Records' in event:
        return handle_s3_event(event)

    # Scheduled event
    return handle_scheduled_event(event)


def handle_api_request(event):
    """Handle REST API requests"""
    method = event['httpMethod']

    if method == 'GET':
        order_id = event['pathParameters']['orderId']
        response = table.get_item(Key={'orderId': order_id})

        if 'Item' in response:
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'])
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Order not found'})
            }

    elif method == 'POST':
        body = json.loads(event['body'])

        # Validate input
        if not body.get('userId') or not body.get('items'):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid input'})
            }

        # Create order
        order = {
            'orderId': f"ORD-{datetime.now().timestamp()}",
            'userId': body['userId'],
            'items': body['items'],
            'status': 'PENDING',
            'createdAt': datetime.now().isoformat()
        }

        table.put_item(Item=order)

        return {
            'statusCode': 201,
            'body': json.dumps(order)
        }


def handle_s3_event(event):
    """Handle S3 upload events"""
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        # Process file
        obj = s3.get_object(Bucket=bucket, Key=key)
        content = obj['Body'].read().decode('utf-8')

        # Do something with content
        print(f"Processed {key}: {len(content)} bytes")

    return {'statusCode': 200}


def handle_scheduled_event(event):
    """Handle scheduled events (CloudWatch Events)"""
    # Daily cleanup, report generation, etc.
    print("Running scheduled task...")
    return {'statusCode': 200}
```

---

### Ví dụ 2.2: Deploy Lambda với AWS SAM

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Timeout: 30
    MemorySize: 256
    Runtime: python3.9

Resources:
  OrderFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: order-api
      CodeUri: ./src/
      Handler: lambda_function.lambda_handler
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref OrdersTable
        - S3ReadPolicy:
            BucketName: !Ref UploadBucket
      Events:
        GetOrder:
          Type: Api
          Properties:
            Path: /orders/{orderId}
            Method: GET
        CreateOrder:
          Type: Api
          Properties:
            Path: /orders
            Method: POST
        S3Upload:
          Type: S3
          Properties:
            Bucket: !Ref UploadBucket
            Events: s3:ObjectCreated:*
        DailyCleanup:
          Type: Schedule
          Properties:
            Schedule: rate(1 day)
            Input: '{"task": "cleanup"}'

  OrdersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: Orders
      AttributeDefinitions:
        - AttributeName: orderId
          AttributeType: S
      KeySchema:
        - AttributeName: orderId
          KeyType: HASH
      BillingMode: PAY_PER_REQUEST

  UploadBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub 'order-uploads-${AWS::AccountId}'

Outputs:
  ApiEndpoint:
    Description: API Gateway endpoint URL
    Value: !Sub 'https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/'
```

**Deploy commands:**
```bash
# 1. Package
sam package \
  --template-file template.yaml \
  --s3-bucket my-deployment-bucket \
  --output-template-file packaged.yaml

# 2. Deploy
sam deploy \
  --template-file packaged.yaml \
  --stack-name order-api-stack \
  --capabilities CAPABILITY_IAM \
  --region us-east-1

# 3. Invoke function locally
sam local invoke OrderFunction --event event.json

# 4. Test API
curl https://xxxxx.execute-api.us-east-1.amazonaws.com/Prod/orders/ORD-123
```

---

## 📁 BÀI 3: S3 & CLOUDFRONT

### Ví dụ 3.1: Upload files với S3 SDK

```python
import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')

def upload_file(file_name, bucket, object_name=None):
    """Upload file to S3"""
    if object_name is None:
        object_name = file_name

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(f"Uploaded {file_name} to {bucket}/{object_name}")
    except ClientError as e:
        print(f"Error: {e}")
        return False
    return True

def generate_presigned_url(bucket, key, expiration=3600):
    """Generate pre-signed URL for temporary access"""
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=expiration
        )
        return url
    except ClientError as e:
        print(f"Error: {e}")
        return None

def setup_lifecycle_policy(bucket):
    """Setup lifecycle policy for cost optimization"""
    lifecycle_configuration = {
        'Rules': [
            {
                'ID': 'MoveToIA',
                'Status': 'Enabled',
                'Prefix': '',
                'Transitions': [
                    {
                        'Days': 30,
                        'StorageClass': 'STANDARD_IA'
                    },
                    {
                        'Days': 90,
                        'StorageClass': 'GLACIER'
                    }
                ],
                'Expiration': {
                    'Days': 365
                }
            }
        ]
    }

    s3_client.put_bucket_lifecycle_configuration(
        Bucket=bucket,
        LifecycleConfiguration=lifecycle_configuration
    )

# Usage
upload_file('report.pdf', 'my-app-bucket', 'reports/2024/report.pdf')
url = generate_presigned_url('my-app-bucket', 'reports/2024/report.pdf', expiration=600)
print(f"Download URL (expires in 10 min): {url}")
```

---

### Ví dụ 3.2: CloudFront distribution với Terraform

```hcl
# main.tf
provider "aws" {
  region = "us-east-1"
}

# S3 bucket for static content
resource "aws_s3_bucket" "cdn_bucket" {
  bucket = "my-app-cdn-${data.aws_caller_identity.current.account_id}"
}

resource "aws_s3_bucket_public_access_block" "cdn_bucket" {
  bucket = aws_s3_bucket.cdn_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "cdn_bucket" {
  bucket = aws_s3_bucket.cdn_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.cdn_bucket.arn}/*"
      }
    ]
  })
}

# CloudFront distribution
resource "aws_cloudfront_distribution" "cdn" {
  origin {
    domain_name = aws_s3_bucket.cdn_bucket.bucket_regional_domain_name
    origin_id   = "S3-${aws_s3_bucket.cdn_bucket.id}"

    s3_origin_config {
      origin_access_identity = ""
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "CDN for my app"
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${aws_s3_bucket.cdn_bucket.id}"

    forwarded_values {
      query_string = false
      headers      = ["*"]

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
    compress               = true
  }

  # Custom error responses
  custom_error_response {
    error_code            = 404
    response_page_path    = "/index.html"
    response_code         = 200
    error_caching_min_ttl = 300
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

output "cloudfront_domain" {
  value = aws_cloudfront_distribution.cdn.domain_name
}
```

---

## 📁 BÀI 4: VPC & NETWORKING

### Ví dụ 4.1: VPC Architecture với Terraform

```hcl
# vpc.tf
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "my-app-vpc"
  }
}

# Public subnets (for ALB, NAT Gateway)
resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-a"
    Type = "public"
  }
}

resource "aws_subnet" "public_b" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-b"
    Type = "public"
  }
}

# Private subnets (for EC2, RDS)
resource "aws_subnet" "private_a" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.10.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "private-subnet-a"
    Type = "private"
  }
}

resource "aws_subnet" "private_b" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.11.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "private-subnet-b"
    Type = "private"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "my-app-igw"
  }
}

# NAT Gateway (for private subnet internet access)
resource "aws_eip" "nat" {
  domain = "vpc"
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_a.id

  tags = {
    Name = "my-app-nat"
  }
}

# Route tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "public-rt"
  }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }

  tags = {
    Name = "private-rt"
  }
}

# Route table associations
resource "aws_route_table_association" "public_a" {
  subnet_id      = aws_subnet.public_a.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_b" {
  subnet_id      = aws_subnet.public_b.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private_a" {
  subnet_id      = aws_subnet.private_a.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "private_b" {
  subnet_id      = aws_subnet.private_b.id
  route_table_id = aws_route_table.private.id
}

# Security Groups
resource "aws_security_group" "alb" {
  name        = "alb-sg"
  description = "Security group for ALB"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "app" {
  name        = "app-sg"
  description = "Security group for application"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "db" {
  name        = "db-sg"
  description = "Security group for database"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }
}
```

---

## 📁 BÀI 5: IAM & SECURITY

### Ví dụ 5.1: IAM Policies

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3Read",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-app-bucket",
        "arn:aws:s3:::my-app-bucket/*"
      ]
    },
    {
      "Sid": "AllowDynamoDB",
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Query"
      ],
      "Resource": "arn:aws:dynamodb:us-east-1:123456789:table/Orders"
    },
    {
      "Sid": "AllowCloudWatchLogs",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

---

### Ví dụ 5.2: Lambda execution role với Terraform

```hcl
resource "aws_iam_role" "lambda_role" {
  name = "lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_custom" {
  name = "lambda-custom-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "arn:aws:s3:::my-app-bucket/*"
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:Query"
        ]
        Resource = aws_dynamodb_table.orders.arn
      }
    ]
  })
}
```

---

## 📁 BÀI 6: MONITORING & ALERTING

### Ví dụ 6.1: CloudWatch Alarms với Terraform

```hcl
# CPU alarm
resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "high-cpu-utilization"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This alarm monitors EC2 CPU utilization"
  alarm_actions       = [aws_sns_topic.alerts.arn]

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.main.name
  }
}

# Memory alarm (requires CloudWatch agent)
resource "aws_cloudwatch_metric_alarm" "memory_high" {
  alarm_name          = "high-memory-utilization"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "MemoryUtilization"
  namespace           = "CWAgent"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This alarm monitors memory utilization"
  alarm_actions       = [aws_sns_topic.alerts.arn]
}

# Lambda errors alarm
resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "lambda-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = "60"
  statistic           = "Sum"
  threshold           = "0"
  alarm_description   = "This alarm monitors Lambda function errors"
  alarm_actions       = [aws_sns_topic.alerts.arn]

  dimensions = {
    FunctionName = aws_lambda_function.my_function.function_name
  }
}

# SNS topic for alerts
resource "aws_sns_topic" "alerts" {
  name = "infrastructure-alerts"
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = "devops@example.com"
}
```

---

### Ví dụ 6.2: Custom metrics với Python

```python
import boto3
from datetime import datetime

cloudwatch = boto3.client('cloudwatch')

def put_custom_metric(metric_name, value, unit='Count'):
    """Put custom metric to CloudWatch"""
    cloudwatch.put_metric_data(
        Namespace='MyApp',
        MetricData=[
            {
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit,
                'Timestamp': datetime.utcnow(),
                'Dimensions': [
                    {
                        'Name': 'Environment',
                        'Value': 'Production'
                    },
                    {
                        'Name': 'Service',
                        'Value': 'OrderService'
                    }
                ]
            }
        ]
    )

# Usage in application
def process_order(order):
    start_time = datetime.now()

    try:
        # Process order logic
        put_custom_metric('OrdersProcessed', 1, 'Count')
    except Exception as e:
        put_custom_metric('OrderProcessingErrors', 1, 'Count')
        raise
    finally:
        duration = (datetime.now() - start_time).total_seconds()
        put_custom_metric('OrderProcessingTime', duration, 'Seconds')
```

---

## 📝 BÀI TẬP THỰC HÀNH

Xem `03-exercises.md` để làm bài tập!

---

## 🔗 TÀI LIỆU THAM KHẢO

1. [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/)
2. [AWS Terraform Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
3. [AWS SAM Developer Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/)
4. [CloudWatch Metrics and Dimensions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CW_Support_For_AWS.html)
