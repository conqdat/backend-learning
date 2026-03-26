# Phase 05.5: AWS Cloud - Bài Tập Thực Hành

> **Thời gian:** 3-4 giờ
> **Mục tiêu:** Thực hành với AWS services qua các bài lab thực tế

---

## 📝 BÀI TẬP 1: EC2 & LOAD BALANCING (1 giờ)

### Đề bài

Triển khai ứng dụng Spring Boot lên EC2 với Load Balancer

### Phần 1: Chuẩn bị AMI

```bash
# 1. Tạo custom AMI với Java 17 + Docker
# Launch EC2 instance tạm thời
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t2.micro \
  --tag-specifications 'ResourceType=instances,Tags=[{Key=Name,Value=ami-builder}]'

# SSH và cài đặt
ssh -i key.pem ec2-user@<public-ip>

# Cài đặt trong EC2:
sudo yum update -y
sudo amazon-linux-extras install java-openjdk17 -y
sudo yum install -y docker git
sudo systemctl start docker
sudo usermod -a -G docker ec2-user

# Exit SSH, tạo AMI
aws ec2 create-image \
  --instance-id i-xxxxx \
  --name "my-app-ami-$(date +%Y%m%d)" \
  --description "Custom AMI with Java 17 and Docker"
```

### Phần 2: Tạo Launch Template

```bash
# Tạo launch template
aws ec2 create-launch-template \
  --launch-template-name my-app-template \
  --launch-template-data '{
    "ImageId": "ami-xxxxx",
    "InstanceType": "t3.micro",
    "KeyName": "my-key",
    "SecurityGroupIds": ["sg-xxxxx"],
    "UserData": "base64-encoded-script"
  }'
```

### Phần 3: Cấu hình Application Load Balancer

```bash
# 1. Tạo target group
aws elbv2 create-target-group \
  --name my-app-tg \
  --protocol HTTP \
  --port 8080 \
  --vpc-id vpc-xxxxx \
  --health-check-path /actuator/health \
  --health-check-interval-seconds 30 \
  --healthy-threshold-count 2 \
  --unhealthy-threshold-count 3

# 2. Tạo load balancer
aws elbv2 create-load-balancer \
  --name my-app-alb \
  --subnets subnet-xxxxx subnet-yyyyy \
  --security-group-ids sg-xxxxx \
  --scheme internet-facing

# 3. Tạo listener
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:...
```

### Checklist hoàn thành

- [ ] Tạo được custom AMI
- [ ] Tạo launch template với user-data
- [ ] Tạo ALB với health check
- [ ] Deploy ứng dụng Spring Boot
- [ ] Verify health check qua `/actuator/health`

---

## 📝 BÀI TẬP 2: LAMBDA & API GATEWAY (1 giờ)

### Đề bài

Xây dựng REST API cho order management dùng Lambda + DynamoDB

### Phần 1: Tạo DynamoDB table

```bash
aws dynamodb create-table \
  --table-name Orders \
  --attribute-definitions \
    AttributeName=orderId,AttributeType=S \
    AttributeName=userId,AttributeType=S \
  --key-schema \
    AttributeName=orderId,KeyType=HASH \
  --global-secondary-indexes \
    IndexName=UserIdIndex, \
    KeySchema=[{AttributeName=userId,KeyType=HASH}], \
    Projection={ProjectionType=ALL}, \
    ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5} \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --table-status ACTIVE
```

### Phần 2: Viết Lambda function

**Yêu cầu:** Tạo Lambda function với các endpoints:

```python
# TODO: Implement lambda_function.py

GET /orders/{orderId}     # Get order by ID
POST /orders              # Create new order
PUT /orders/{orderId}     # Update order
DELETE /orders/{orderId}  # Cancel order
GET /users/{userId}/orders # Get orders by user (GSI query)
```

### Phần 3: Deploy với SAM

```bash
# 1. Khởi tạo project
sam init --name order-api --runtime python3.9

# 2. Viết template.yaml
# TODO: Define resources (Lambda, DynamoDB, API Gateway)

# 3. Deploy
sam build
sam deploy --guided

# 4. Test API
curl https://xxxxx.execute-api.us-east-1.amazonaws.com/Prod/orders
```

### Checklist hoàn thành

- [ ] Tạo DynamoDB table với GSI
- [ ] Viết Lambda function cho CRUD operations
- [ ] Deploy với AWS SAM
- [ ] Test tất cả endpoints với curl
- [ ] Verify data trong DynamoDB console

---

## 📝 BÀI TẬP 3: S3 & CLOUDFRONT (45 phút)

### Đề bài

Xây dựng static website hosting với S3 + CloudFront

### Phần 1: Setup S3 bucket

```bash
# 1. Tạo bucket
aws s3 mb s3://my-app-website-<account-id>

# 2. Upload files
aws s3 sync ./website/ s3://my-app-website-<account-id>/

# 3. Cấu hình public access
aws s3api put-bucket-policy \
  --bucket my-app-website-<account-id> \
  --policy file://bucket-policy.json

# bucket-policy.json content:
# {
#   "Version": "2012-10-17",
#   "Statement": [{
#     "Sid": "PublicReadGetObject",
#     "Effect": "Allow",
#     "Principal": "*",
#     "Action": "s3:GetObject",
#     "Resource": "arn:aws:s3:::my-app-website-<account-id>/*"
#   }]
# }
```

### Phần 2: Tạo CloudFront distribution

```bash
aws cloudfront create-distribution \
  --origin-domain-name my-app-website-<account-id>.s3.amazonaws.com \
  --default-root-object index.html \
  --no-enable-logging \
  --enabled
```

### Phần 3: Cấu hình HTTPS & Custom Domain (optional)

```bash
# 1. Request certificate với ACM
aws acm request-certificate \
  --domain-name www.example.com \
  --validation-method DNS

# 2. Update CloudFront distribution với custom certificate
# 3. Cấu hình DNS record trong Route53
```

### Checklist hoàn thành

- [ ] Tạo S3 bucket với public policy
- [ ] Upload static files (HTML, CSS, JS)
- [ ] Tạo CloudFront distribution
- [ ] Verify HTTPS redirect
- [ ] Test cache invalidation: `aws cloudfront create-invalidation`

---

## 📝 BÀI TẬP 4: VPC TERAFORM (1 giờ)

### Đề bài

Dùng Terraform để tạo VPC với public/private subnets

### Phần 1: Viết Terraform configuration

**Yêu cầu:** Tạo các resources sau:

```hcl
# TODO: Viết trong file vpc.tf

Resources cần có:
1. VPC với CIDR 10.0.0.0/16
2. 2 public subnets (cho ALB)
3. 2 private subnets (cho EC2/RDS)
4. Internet Gateway
5. NAT Gateway
6. Route tables cho public và private
7. Security groups (alb-sg, app-sg, db-sg)
```

### Phần 2: Deploy với Terraform

```bash
# 1. Initialize
terraform init

# 2. Plan
terraform plan -out=tfplan

# 3. Apply
terraform apply tfplan

# 4. Verify
terraform output
```

### Phần 3: Test connectivity

```bash
# 1. Launch EC2 trong private subnet
aws ec2 run-instances \
  --image-id ami-xxxxx \
  --instance-type t3.micro \
  --subnet-id subnet-private-xxxxx \
  --security-group-ids sg-app \
  --no-associate-public-ip-address

# 2. SSH qua bastion host hoặc Session Manager
aws ssm start-session --target i-xxxxx

# 3. Test kết nối internet từ private subnet
curl ifconfig.me

# 4. Test kết nối đến RDS
psql -h rds-endpoint -U postgres
```

### Checklist hoàn thành

- [ ] Tạo VPC với đúng CIDR
- [ ] Tạo public/private subnets
- [ ] Cấu hình Internet Gateway + NAT Gateway
- [ ] Route tables đúng
- [ ] Security groups cho từng layer
- [ ] Test connectivity từ private subnet

---

## 📝 BÀI TẬP 5: MONITORING & ALERTING (30 phút)

### Đề bài

Cấu hình CloudWatch alarms cho application

### Phần 1: Tạo CloudWatch Alarms

```bash
# 1. CPU alarm
aws cloudwatch put-metric-alarm \
  --alarm-name "High-CPU-Alarm" \
  --alarm-description "CPU utilization > 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --dimensions Name=AutoScalingGroupName,Value=my-app-asg \
  --alarm-actions arn:aws:sns:us-east-1:123456789:alerts

# 2. Lambda errors alarm
aws cloudwatch put-metric-alarm \
  --alarm-name "Lambda-Errors-Alarm" \
  --alarm-description "Lambda function errors" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 60 \
  --threshold 0 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 1 \
  --dimensions Name=FunctionName,Value=order-api \
  --alarm-actions arn:aws:sns:us-east-1:123456789:alerts
```

### Phần 2: Tạo SNS topic và subscription

```bash
# 1. Tạo SNS topic
aws sns create-topic --name infrastructure-alerts

# 2. Subscribe email
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:123456789:infrastructure-alerts \
  --protocol email \
  --endpoint your-email@example.com

# 3. Confirm subscription qua email
```

### Phần 3: Custom metrics (optional)

```python
# TODO: Viết script Python đẩy custom metrics lên CloudWatch
# Metrics: OrdersProcessed, OrderProcessingTime, OrderErrors
```

### Checklist hoàn thành

- [ ] Tạo CPU alarm cho Auto Scaling Group
- [ ] Tạo Lambda errors alarm
- [ ] Tạo SNS topic
- [ ] Subscribe email nhận alert
- [ ] (Optional) Push custom metrics

---

## ✅ CHECKLIST HOÀN THÀNH PHASE 05.5

- [ ] Launch EC2 instance với custom AMI
- [ ] Cấu hình Auto Scaling Group
- [ ] Tạo Application Load Balancer
- [ ] Deploy Lambda function với API Gateway
- [ ] Tạo DynamoDB table và query
- [ ] Setup S3 static website
- [ ] Cấu hình CloudFront CDN
- [ ] Tạo VPC với Terraform
- [ ] Cấu hình CloudWatch alarms
- [ ] Setup SNS notifications

---

## 📤 CÁCH SUBMIT

1. Push Terraform code lên GitHub
2. Tạo file `AWS_LABS.md` với:
   - Screenshots của các resources đã tạo
   - ARN của Lambda function, DynamoDB table
   - CloudFront distribution URL
   - Output của `terraform show`
   - Khó khăn gặp phải

---

## 🔜 SAU KHI HOÀN THÀNH

Submit xong, unlock Phase 09: System Design!
