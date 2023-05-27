use strict;
use warnings;
use AWS::CLIWrapper;
use Getopt::Long;

sub print_usage {
    print "Usage: perl script.pl [--region=<region>]\n";
    print "region (optional): The AWS region to use. If not provided, the default region is us-west-2.\n";
}

# Parse command line options
my $region = 'us-west-2';
GetOptions('region=s' => \$region);

# Create an instance of the AWS CLI Wrapper
my $aws = AWS::CLIWrapper->new;

# Initialize counters
my %counts;
$counts{'EC2 Instances'} = 0;
$counts{'Security Groups'} = 0;
$counts{'Network ACLs'} = 0;
$counts{'S3 Buckets'} = 0;
$counts{'RDS Instances'} = 0;
$counts{'Secrets'} = 0;
$counts{'Amazon EKS Clusters'} = 0;
$counts{'Amazon ECS Clusters'} = 0;
$counts{'EC2 Volumes'} = 0;
$counts{'EC2 Images'} = 0;
$counts{'RDS Snapshots'} = 0;
$counts{'EC2 Snapshots'} = 0;

# Open the output file for writing
my $output_file = "listAwsRes_$region.txt";
open(my $fh, '>', $output_file) or die "Could not open file '$output_file' for writing: $!";

# List EC2 instances
my $ec2_instances = $aws->ec2('describe-instances');
for my $reservation (@{$ec2_instances->{Reservations}}) {
    for my $instance (@{$reservation->{Instances}}) {
        $counts{'EC2 Instances'}++;
        my $instance_id = $instance->{InstanceId};
        print_and_write("EC2 Instance ID: $instance_id\n");
    }
}

# List security groups
my $security_groups = $aws->ec2('describe-security-groups');
for my $group (@{$security_groups->{SecurityGroups}}) {
    $counts{'Security Groups'}++;
    my $group_id = $group->{GroupId};
    print_and_write("Security Group ID: $group_id\n");
}

# List network ACLs
my $network_acls = $aws->ec2('describe-network-acls');
for my $acl (@{$network_acls->{NetworkAcls}}) {
    $counts{'Network ACLs'}++;
    my $acl_id = $acl->{NetworkAclId};
    print_and_write("Network ACL ID: $acl_id\n");
}

# List S3 buckets
my $s3_buckets = $aws->s3('list-buckets');
for my $bucket (@{$s3_buckets->{Buckets}}) {
    $counts{'S3 Buckets'}++;
    my $bucket_name = $bucket->{Name};
    print_and_write("S3 Bucket: $bucket_name\n");
}

# List RDS instances
my $rds_instances = $aws->rds('describe-db-instances');
for my $instance (@{$rds_instances->{DBInstances}}) {
    $counts{'RDS Instances'}++;
    my $instance_id = $instance->{DBInstanceIdentifier};
    print_and_write("RDS Instance ID: $instance_id\n");
}

# List Secrets Manager secrets
my $secrets = $aws->secretsmanager('list-secrets');
for my $secret (@{$secrets->{SecretList}}) {
    $counts{'Secrets'}++;
    my $secret_name = $secret->{Name};
    print_and_write("Secret Name: $secret_name\n");
}

# List Amazon EKS clusters
my $eks_clusters = $aws->eks('list-clusters');
for my $cluster_name (@{$eks_clusters->{clusters}}) {
    $counts{'Amazon EKS Clusters'}++;
    print_and_write("EKS Cluster Name: $cluster_name\n");
}

# List Amazon ECS clusters
my $ecs_clusters = $aws->ecs('list-clusters');
for my $cluster_arn (@{$ecs_clusters->{clusterArns}}) {
    $counts{'Amazon ECS Clusters'}++;
    print_and_write("ECS Cluster ARN: $cluster_arn\n");
}

# List EC2 volumes
my $ec2_volumes = $aws->ec2('describe-volumes');
for my $volume (@{$ec2_volumes->{Volumes}}) {
    $counts{'EC2 Volumes'}++;
    my $volume_id = $volume->{VolumeId};
    print_and_write("EC2 Volume ID: $volume_id\n");
}

# List EC2 images
my $ec2_images = $aws->ec2('describe-images', { Owners => ['self'] });
for my $image (@{$ec2_images->{Images}}) {
    $counts{'EC2 Images'}++;
    my $image_id = $image->{ImageId};
    print_and_write("EC2 Image ID: $image_id\n");
}

# List RDS snapshots
my $rds_snapshots = $aws->rds('describe-db-snapshots');
for my $snapshot (@{$rds_snapshots->{DBSnapshots}}) {
    $counts{'RDS Snapshots'}++;
    my $snapshot_arn = $snapshot->{DBSnapshotArn};
    print_and_write("RDS Snapshot ARN: $snapshot_arn\n");
}

# List EC2 snapshots
my $ec2_snapshots = $aws->ec2('describe-snapshots', { OwnerIds => ['self'] });
for my $snapshot (@{$ec2_snapshots->{Snapshots}}) {
    $counts{'EC2 Snapshots'}++;
    my $snapshot_id = $snapshot->{SnapshotId};
    print_and_write("EC2 Snapshot ID: $snapshot_id\n");
}

# Close the output file
close($fh);

# Output counts
my $count_output = "Resource counts for region $region:\n";
my $total_count = 0;
foreach my $resource (sort keys %counts) {
    my $count = $counts{$resource};
    $count_output .= "$resource: $count\n";
    $total_count += $count;
}
$count_output .= "Total Resources: $total_count\n";

print $count_output;
print "Output written to $output_file\n";

# Print to console and write to file
sub print_and_write {
    my $line = shift;
    print $line;
    print $fh $line;
}

