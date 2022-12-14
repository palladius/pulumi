from pulumi import Config, export, get_project, get_stack, Output, ResourceOptions
from pulumi_gcp.config import project, zone
from pulumi_gcp.container import Cluster, ClusterNodeConfigArgs
from pulumi_kubernetes import Provider
from pulumi_kubernetes.apps.v1 import Deployment, DeploymentSpecArgs
from pulumi_kubernetes.core.v1 import ContainerArgs, PodSpecArgs, PodTemplateSpecArgs, Service, ServicePortArgs, ServiceSpecArgs
from pulumi_kubernetes.meta.v1 import LabelSelectorArgs, ObjectMetaArgs
from pulumi_random import RandomPassword

#import lib.ric_config
from lib.ric_config import PulumiProject, ShortPulumiProject, PulumiStack, pyellow, puts

# Read in some configurable settings for our cluster:
config = Config(None)

# Config of GKE cluster.
NODE_COUNT = config.get_int('node_count') or 3
NODE_MACHINE_TYPE = config.get('node_machine_type') or 'n1-standard-1'
USERNAME = config.get('username') or 'admin'
PASSWORD = config.get_secret('password') or RandomPassword("password", length=20, special=True).result
MASTER_VERSION = config.get('master_version')

# Now, actually create the GKE cluster.

cluster_name = f'pu-{ShortPulumiProject}-{PulumiStack}' # max 40 chars!

k8s_cluster = Cluster(
    #'gke-cluster',
    cluster_name,
    initial_node_count=NODE_COUNT,
    node_version=MASTER_VERSION,
    min_master_version=MASTER_VERSION,
    node_config=ClusterNodeConfigArgs(
        machine_type=NODE_MACHINE_TYPE,
        oauth_scopes=[
            'https://www.googleapis.com/auth/compute',
            'https://www.googleapis.com/auth/devstorage.read_only',
            'https://www.googleapis.com/auth/logging.write',
            'https://www.googleapis.com/auth/monitoring'
        ],
    ),
)

# Manufacture a GKE-style Kubeconfig. Note that this is slightly "different" because of the way GKE requires
# gcloud to be in the picture for cluster authentication (rather than using the client cert/key directly).
k8s_info = Output.all(k8s_cluster.name, k8s_cluster.endpoint, k8s_cluster.master_auth)

#puts(info)
#pyellow(k8s_info)
#pyellow(f"[RiccALOPF] lambda info: {info}")

k8s_config = k8s_info.apply(
    lambda info: """apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: {0}
    server: https://{1}
  name: {2}
contexts:
- context:
    cluster: {2}
    user: {2}
  name: {2}
current-context: {2}
kind: Config
preferences: {{}}
users:
- name: {2}
  user:
    auth-provider:
      config:
        cmd-args: config config-helper --format=json
        cmd-path: gcloud
        expiry-key: '{{.credential.token_expiry}}'
        token-key: '{{.credential.access_token}}'
      name: gcp
""".format(info[2]['cluster_ca_certificate'], info[1], '{0}_{1}_{2}'.format(project, zone, info[0])))

# Make a Kubernetes provider instance that uses our cluster from above.
k8s_provider = Provider('gke_k8s', kubeconfig=k8s_config)

# Create a canary deployment to test that this cluster works.
labels = { 'app': 'canary-{0}-{1}'.format(get_project(), get_stack()) }
canary = Deployment('canary',
    spec=DeploymentSpecArgs(
        selector=LabelSelectorArgs(match_labels=labels),
        replicas=1,
        template=PodTemplateSpecArgs(
            metadata=ObjectMetaArgs(labels=labels),
            spec=PodSpecArgs(containers=[ContainerArgs(name='nginx', image='nginx')]),
        ),
    ), opts=ResourceOptions(provider=k8s_provider)
)

ingress = Service('ingress',
    spec=ServiceSpecArgs(
        type='LoadBalancer',
        selector=labels,
        ports=[ServicePortArgs(port=80)],
    ), opts=ResourceOptions(provider=k8s_provider)
)

# Finally, export the kubeconfig so that the client can easily access the cluster.
export('kubeconfig', k8s_config)
# Export the k8s ingress IP to access the canary deployment
export('ingress_ip', ingress.status.apply(lambda status: status.load_balancer.ingress[0].ip))
# would be `ingress.status.load_balancer.ingress[0].ip`
export('k8s_cluster_name', k8s_cluster.name)
