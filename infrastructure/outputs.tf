###############################################################################
# Outputs for the StratoSentry NIDS AWS infrastructure.
###############################################################################

output "instance_public_ip" {
  description = "Public IP address of the StratoSentry sensor EC2 instance."
  value       = aws_instance.sensor.public_ip
}

output "instance_public_dns" {
  description = "Public DNS name of the StratoSentry sensor EC2 instance."
  value       = aws_instance.sensor.public_dns
}

output "instance_id" {
  description = "ID of the StratoSentry sensor EC2 instance."
  value       = aws_instance.sensor.id
}

output "vpc_id" {
  description = "ID of the VPC created for StratoSentry."
  value       = aws_vpc.main.id
}

output "iam_role_name" {
  description = "Name of the IAM role attached to the sensor instance profile."
  value       = aws_iam_role.sensor.name
}

output "ssh_command" {
  description = "Convenience SSH command (requires key_name to be set)."
  value       = "ssh ubuntu@${aws_instance.sensor.public_ip}"
}
