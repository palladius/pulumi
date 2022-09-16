"""A Google Cloud Python Pulumi program"""

import pulumi
from pulumi_gcp import storage

# Create a GCP resource (Storage Bucket)
gcp_kms_minimal_bucket = storage.Bucket('my-bucket', location="US")
# Export the DNS name of the bucket
pulumi.export('bucket_name', gcp_kms_minimal_bucket.url)

print("TODO(ricc): also print/output a password")

# pulumi.export('clear-password',  pulumi.Config().require_secret('clear-password'))
# pulumi.export('secret-password', pulumi.Config().require_secret('secret-password'))
