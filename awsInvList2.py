import boto3
import sys

def print_usage():
    print("Usage: python script.py [region]")
    print("region (optional): The AWS region to use. If not provided, the default region is us-west-2.")

# Check if the region parameter is provided
if len(sys.argv) > 2:
    print("Error: Too many arguments.")
    print_usage()
    sys.exit(1)

# Set the default region to us-west-2 if no parameter is provided
region = sys.argv[1] if len(sys.argv) > 1 else 'us-west-2'

# Create a session using your AWS credentials and the provided region
session = boto3.Session(region_name=region)

# Create clients for different AWS services
ec2_client = session.client('ec2')
s3_client = session.client('s3')
rds_client = session.client('rds')
secrets_client = session.client('secretsmanager')
eks_client = session.client('eks')
ecs_client = session.client('ecs')

# Initialize counters
ec2_count = 0
security_group_count = 0
network_acl_count = 0
s3_bucket_count = 0
rds_instance_count = 0
secret_count = 0
eks_cluster_count = 0
ecs_cluster_count = 0
ec2_volume_count = 0
ec2_image_count = 0
rds_snapshot_count = 0
ec2_snapshot_count = 0

# Open the output file for writing
output_file = open(f"listAwsRes_{region}.txt", "w")

# List EC2 instances
response = ec2_client.describe_instances()
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        ec2_count += 1
        instance_id = instance['InstanceId']
        output_line = f"EC2 Instance ID: {instance_id}\n"
        output_file.write(output_line)
        print(output_line)

# List security groups
response = ec2_client.describe_security_groups()
for group in response['SecurityGroups']:
    security_group_count += 1
    group_id = group['GroupId']
    output_line = f"Security Group ID: {group_id}\n"
    output_file.write(output_line)
    print(output_line)

# List network ACLs
response = ec2_client.describe_network_acls()
for acl in response['NetworkAcls']:
    network_acl_count += 1
    acl_id = acl['NetworkAclId']
    output_line = f"Network ACL ID: {acl_id}\n"
    output_file.write(output_line)
    print(output_line)

# List S3 buckets
response = s3_client.list_buckets()
for bucket in response['Buckets']:
    s3_bucket_count += 1
    bucket_name = bucket['Name']
    output_line = f"S3 Bucket: {bucket_name}\n"
    output_file.write(output_line)
    print(output_line)

# List RDS instances
response = rds_client.describe_db_instances()
for instance in response['DBInstances']:
    rds_instance_count += 1
    instance_id = instance['DBInstanceIdentifier']
    output_line = f"RDS Instance ID: {instance_id}\n"
    output_file.write(output_line)
    print(output_line)

# List Secrets Manager secrets
response = secrets_client.list_secrets()
for secret in response['SecretList']:
    secret_count += 1
    secret_name = secret['Name']
    output_line = f"Secret Name: {secret_name}\n"
    output_file.write(output_line)
    print(output_line)

# List Amazon EKS clusters
response = eks_client.list_clusters()
for cluster_name in response['clusters']:
    eks_cluster_count += 1
    output_line = f"EKS Cluster Name: {cluster_name}\n"
    output_file.write(output_line)
    print(output_line)

# List Amazon ECS clusters
response = ecs_client.list_clusters()
for cluster_arn in response['clusterArns']:
    ecs_cluster_count += 1
    output_line = f"ECS Cluster ARN: {cluster_arn}\n"
    output_file.write(output_line)
    print(output_line)

# List EC2 volumes
response = ec2_client.describe_volumes()
for volume in response['Volumes']:
    ec2_volume_count += 1
    volume_id = volume['VolumeId']
    output_line = f"EC2 Volume ID: {volume_id}\n"
    output_file.write(output_line)
    print(output_line)

# List EC2 images
response = ec2_client.describe_images(Owners=['self'])
for image in response['Images']:
    ec2_image_count += 1
    image_id = image['ImageId']
    output_line = f"EC2 Image ID: {image_id}\n"
    output_file.write(output_line)
    print(output_line)

# List RDS snapshots
response = rds_client.describe_db_snapshots()
for snapshot in response['DBSnapshots']:
    rds_snapshot_count += 1
    snapshot_arn = snapshot['DBSnapshotArn']
    output_line = f"RDS Snapshot ARN: {snapshot_arn}\n"
    output_file.write(output_line)
    print(output_line)

# List EC2 snapshots
response = ec2_client.describe_snapshots(OwnerIds=['self'])
for snapshot in response['Snapshots']:
    ec2_snapshot_count += 1
    snapshot_id = snapshot['SnapshotId']
    output_line = f"EC2 Snapshot ID: {snapshot_id}\n"
    output_file.write(output_line)
    print(output_line)

# Close the output file
output_file.close()

# Output counts
count_output = f"\nResource counts for region {region}:\n"
count_output += f"EC2 Instances: {ec2_count}\n"
count_output += f"Security Groups: {security_group_count}\n"
count_output += f"Network ACLs: {network_acl_count}\n"
count_output += f"S3 Buckets: {s3_bucket_count}\n"
count_output += f"RDS Instances: {rds_instance_count}\n"
count_output += f"Secrets: {secret_count}\n"
count_output += f"Amazon EKS Clusters: {eks_cluster_count}\n"
count_output += f"Amazon ECS Clusters: {ecs_cluster_count}\n"
count_output += f"EC2 Volumes: {ec2_volume_count}\n"
count_output += f"EC2 Images: {ec2_image_count}\n"
count_output += f"RDS Snapshots: {rds_snapshot_count}\n"
count_output += f"EC2 Snapshots: {ec2_snapshot_count}\n"
count_output += f"Total Resources: {ec2_count + security_group_count + network_acl_count + s3_bucket_count + rds_instance_count + secret_count + eks_cluster_count + ecs_cluster_count + ec2_volume_count + ec2_image_count + rds_snapshot_count + ec2_snapshot_count}\n"

print(count_output)
with open(f"listAwsRes_{region}.txt", "a") as count_file:
    count_file.write(count_output)

