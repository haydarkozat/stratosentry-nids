###############################################################################
# Input variables for the StratoSentry NIDS AWS infrastructure.
###############################################################################

variable "aws_region" {
  description = "AWS region to deploy the infrastructure into."
  type        = string
  default     = "eu-central-1"
}

variable "instance_type" {
  description = "EC2 instance type for the sensor (free-tier friendly)."
  type        = string
  default     = "t3.micro"

  validation {
    condition     = contains(["t2.micro", "t3.micro"], var.instance_type)
    error_message = "instance_type must be either t2.micro or t3.micro."
  }
}

variable "project_name" {
  description = "Short name used to prefix and tag all resources."
  type        = string
  default     = "stratosentry"
}

variable "environment" {
  description = "Deployment environment name (used for tagging)."
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet."
  type        = string
  default     = "10.0.1.0/24"
}

variable "ssh_ingress_cidrs" {
  description = "List of CIDR blocks allowed to reach the sensor over SSH (port 22). Restrict this to your own IP in production."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "key_name" {
  description = "Name of an existing EC2 key pair for SSH access. Leave empty to launch without a key pair."
  type        = string
  default     = ""
}
