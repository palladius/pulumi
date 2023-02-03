from pulumi import Config, export, get_project, get_stack, Output, ResourceOptions
# from pulumi_gcp.config import project, zone, region
# from pulumi_gcp.container import Cluster, ClusterNodeConfigArgs
# from pulumi_kubernetes import Provider
# from pulumi_kubernetes.apps.v1 import Deployment, DeploymentSpecArgs
# from pulumi_kubernetes.core.v1 import ContainerArgs, PodSpecArgs, PodTemplateSpecArgs, Service, ServicePortArgs, ServiceSpecArgs
# from pulumi_kubernetes.meta.v1 import LabelSelectorArgs, ObjectMetaArgs
#from pulumi_random import RandomPassword


def main():
    puts("This is WIP to push carlessian apps..")
    export('riccardo_notes', "Riccardo was here")
    export('riccardo_notes2', "Riccardo was here 2️⃣")
    test_cloud_run()


def test_cloud_run():
        
    cloudrun_service = gcp.cloudrun.Service("default",
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
    export('riccardo_cloudrun_url', cloudrun_service.url)
