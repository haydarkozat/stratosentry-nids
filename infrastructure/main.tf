###############################################################################
# StratoSentry NIDS - AWS Infrastructure
#
# Provisions a minimal, self-contained AWS environment for running the
# StratoSentry sensor on a single EC2 instance with permissions to ship logs
# to CloudWatch Logs (so the future boto3-based logger can authenticate via
# the instance role, with no static credentials).
###############################################################################

terraform {
  required_version = ">= 1.3.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# ---------------------------------------------------------------------------
# Data sources
# ---------------------------------------------------------------------------

# Available AZs in the selected region (the public subnet lands in the first).
data "aws_availability_zones" "available" {
  state = "available"
}

# Latest official Canonical Ubuntu 22.04 LTS (Jammy) AMI for the region.
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}

# ---------------------------------------------------------------------------
# Networking: VPC, public subnet, internet gateway, route table
# ---------------------------------------------------------------------------

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-igw"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidr
  availability_zone       = data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-subnet"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# ---------------------------------------------------------------------------
# Security: SSH inbound, all outbound
# ---------------------------------------------------------------------------

resource "aws_security_group" "sensor" {
  name        = "${var.project_name}-sensor-sg"
  description = "Allow SSH inbound and all outbound traffic for the StratoSentry sensor"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.ssh_ingress_cidrs
  }

  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-sensor-sg"
  }
}

# ---------------------------------------------------------------------------
# IAM: role + instance profile for CloudWatch Logs access
# ---------------------------------------------------------------------------

data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "sensor" {
  name               = "${var.project_name}-sensor-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json

  tags = {
    Name = "${var.project_name}-sensor-role"
  }
}

# Least-privilege policy: create/manage log groups & streams and put events.
data "aws_iam_policy_document" "cloudwatch_logs" {
  statement {
    sid    = "StratoSentryCloudWatchLogs"
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:DescribeLogGroups",
      "logs:DescribeLogStreams",
    ]

    resources = ["arn:aws:logs:*:*:*"]
  }
}

resource "aws_iam_role_policy" "cloudwatch_logs" {
  name   = "${var.project_name}-cloudwatch-logs"
  role   = aws_iam_role.sensor.id
  policy = data.aws_iam_policy_document.cloudwatch_logs.json
}

resource "aws_iam_instance_profile" "sensor" {
  name = "${var.project_name}-sensor-profile"
  role = aws_iam_role.sensor.name
}

# ---------------------------------------------------------------------------
# Compute: EC2 sensor instance
# ---------------------------------------------------------------------------

resource "aws_instance" "sensor" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.sensor.id]
  iam_instance_profile   = aws_iam_instance_profile.sensor.name
  key_name               = var.key_name != "" ? var.key_name : null

  user_data = <<-EOF
    #!/bin/bash
    set -euxo pipefail
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -y
    apt-get upgrade -y
    apt-get install -y python3 python3-pip
  EOF

  tags = {
    Name = "${var.project_name}-sensor"
  }
}
