'''My first python component!

Some docs:
* https://github.com/pulumi/examples/tree/master/classic-azure-py-webserver-component
* https://github.com/pulumi/examples/blob/master/classic-azure-py-webserver-component/webserver.py
'''

import pulumi
import pulumi_gcp as gcp
#from pulumi_gcp import storage
from pulumi import asset, Input, Output, ComponentResource, ResourceOptions

from lib.ric_config import MyProject, MyRegion, AppName, AppNameLower, PulumiStack, PulumiProject, PulumiUser, ShortPulumiProject, print_red


class CloudBuildRiccComponentArgs:
    '''Arguments for tyhis component. Som3ething like:


        Cuold accept a smart MagicRepoUrl like 
        * https://bitbucket.org/palladius/gic/
        * https://github.com/pulumi/examples/

        cloud-build-access-token: <TOKEN>

        cloudbuild-repository-name: USER/REPONAME (redundant in below)
        gcb_gh_name: REPO_NAME
        gcb_gh_owner: USER
        gcb_repo_type: PROVIDER (github | bitbucket)
        rmp-code-folder: SUBFOLDER_TO_BUILD # examples/python-gcp-cloudbuild-auto-trigger/, defaults to /
        pulumi-user: PULUMI_USER  (possibly useless, eg ' palladius')

    '''
    def __init__(
        self, 
        #resource_group: core.ResourceGroup,
        #subnet: network.Subnet,
        #username: Input[str],
        #password: Input[str],
        #useless_bucket: Input[str],
        magic_repo_url: Input[str],
        code_folder: Input[str],
    ):
        #self.useless_bucket = useless_bucket
        self.magic_repo_url = magic_repo_url
        self.code_folder = code_folder


class CloudBuildRiccComponent(pulumi.ComponentResource):
    '''Riccardo vision of CBv1 Component in python.
    
    Currently supports GitHub and Bitbucket.
    
    '''
    def __init__(self, name: str, args: CloudBuildRiccComponentArgs, opts: ResourceOptions = None):
        '''Component Constructor.
        
        Documented here (thanks Ringo): https://www.pulumi.com/docs/intro/concepts/resources/components/
        Inspired by: https://github.com/pulumi/examples/blob/master/classic-azure-py-webserver-component/webserver.py
        '''
        super().__init__('pkg:index:CloudBuildRiccComponent', name, None, opts)

        child_opts = ResourceOptions(parent=self)

        # Creating a sueless bucket..
        bucket = gcp.storage.Bucket(f"cbrc-{name}-useless", 
            location="EU",
            opts=child_opts, # pulumi.ResourceOptions(parent=self)
        )

        # bucket = s3.Bucket(f"{name}-component-bucket",
        #     opts=pulumi.ResourceOptions(parent=self))
        self.register_outputs({
            "bucketUrl": bucket.url # also id, selfLink
        })
        self.register_outputs({})


        # the caller can pass an explicit GCP provider:
#         component = MyComponent('...', ResourceOptions(providers={
#            'aws': useast1,
#            'gcp': myproject,
#            'kubernetes': myk8s,
#           }))