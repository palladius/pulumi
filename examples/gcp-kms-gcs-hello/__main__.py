"""A Google Cloud Python Pulumi program"""

import pulumi
from pulumi_gcp import storage

# Create a GCP resource (Storage Bucket)
gcp_kms_minimal_bucket = storage.Bucket('my-bucket', location="US")
# Export the DNS name of the bucket
pulumi.export('bucket_name', gcp_kms_minimal_bucket.url)

print("TODO(ricc): also print/output a password")
pulumi.export('password_todo', 'TODO show value of KMS')
