from pulumi import Config, export, get_project, get_stack, Output, ResourceOptions

#import pulumi
import pulumi_gcp as gcp

# from pulumi_gcp.config import project, zone, region
# from pulumi_gcp.container import Cluster, ClusterNodeConfigArgs
# from pulumi_kubernetes import Provider
# from pulumi_kubernetes.apps.v1 import Deployment, DeploymentSpecArgs
# from pulumi_kubernetes.core.v1 import ContainerArgs, PodSpecArgs, PodTemplateSpecArgs, Service, ServicePortArgs, ServiceSpecArgs
# from pulumi_kubernetes.meta.v1 import LabelSelectorArgs, ObjectMetaArgs
#from pulumi_random import RandomPassword



def test_cloud_run():
    '''Boilerplate from https://www.pulumi.com/registry/packages/gcp/api-docs/cloudrun/service/.
    '''
    cloudrun_service = gcp.cloudrun.Service("default1",
        location="us-central1",
        template=gcp.cloudrun.ServiceTemplateArgs(
            spec=gcp.cloudrun.ServiceTemplateSpecArgs(
                containers=[gcp.cloudrun.ServiceTemplateSpecContainerArgs(
                    image="us-docker.pkg.dev/cloudrun/container/hello",
                )],
            ),
        ),
        traffics=[gcp.cloudrun.ServiceTrafficArgs(
            latest_revision=True,
            percent=100,
        )])
    cloudrun_service_noauth = gcp.cloudrun.Service("cloudrun_service_noauth2",
            location="us-central1",
            template=gcp.cloudrun.ServiceTemplateArgs(
                spec=gcp.cloudrun.ServiceTemplateSpecArgs(
                    containers=[gcp.cloudrun.ServiceTemplateSpecContainerArgs(
                        image="us-docker.pkg.dev/cloudrun/container/hello",
                    )],
                ),
            ))
    noauth_iam_policy = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
        role="roles/run.invoker",
        members=["allUsers"],
    )])
    noauth_iam_policy = gcp.cloudrun.IamPolicy("noauthIamPolicy",
        location=cloudrun_service_noauth.location,
        project=cloudrun_service_noauth.project,
        service=cloudrun_service_noauth.name,
        policy_data=noauth_iam_policy.policy_data)
    export('riccardo_cloudrun_url', cloudrun_service.id)
    export('riccardo_cloudrun_statuses', cloudrun_service.statuses)

def main():
    #puts("This is WIP to push carlessian apps..")
    export('riccardo_notes', "Riccardo was here")
    export('riccardo_notes2', "Riccardo was here 2️⃣")
    test_cloud_run()

