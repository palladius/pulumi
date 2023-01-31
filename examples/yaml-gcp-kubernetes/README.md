# https://www.pulumi.com/templates/kubernetes/gcp/

This works beautifully but its REALLY unreadable :)


## First execution BUG

```
Diagnostics:
  pulumi:pulumi:Stack (yaml-gcp-kubernetes-dev):
    error: update failed

  gcp:container:Cluster (gke-cluster):
    error: 1 error occurred:
    	* googleapi: Error 400: Failed precondition when calling the ServiceConsumerManager: tenantmanager::185014: Consumer 16939241969 should enable service:container.googleapis.com before generating a service account.
    com.google.api.tenant.error.TenantManagerException: Consumer 16939241969 should enable service:container.googleapis.com before generating a service account.
```

### fix 

fix: enable GKE API: https://console.cloud.google.com/marketplace/product/google/container.googleapis.com?returnUrl=%2Fkubernetes%3Freferrer%3Dsearch%26project%3Dpulumi-prova&project=pulumi-prova