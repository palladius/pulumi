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
        * [FUTURE] also sth magic like:
        * https://github.com/pulumi/examples/tree/master/gcp-py-cloudrun-cloudsql
        * future for BB:
        # ~/git/gprojects/pulumi/20220910-kuberic
        * https://bitbucket.org/palladius/gprojects/src/master/pulumi/20220910-kuberic/

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
        cdb_access_token: Input[str],
    ):
        #self.useless_bucket = useless_bucket
        self.magic_repo_url = magic_repo_url
        self.code_folder = code_folder
        self.cdb_access_token = cdb_access_token or pulumi.Config().require('cloud-build-access-token')


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

        # Creating a USELESS bucket.. remove when all works
        bucket = gcp.storage.Bucket(
            "cbrc-{}".format(name), 
            location="EU",
            opts=child_opts, # pulumi.ResourceOptions(parent=self)
        )

        # bucket = s3.Bucket(f"{name}-component-bucket",
        #     opts=pulumi.ResourceOptions(parent=self))
        self.register_outputs({
            "bucketUrl": bucket.url # also id, selfLink
        })
        # https://github.com/pulumi/pulumi/issues/2394 
        # Calling 'registerOutputs' twice leads to a crash. #2394

        #self.register_outputs({})


        # the caller can pass an explicit GCP provider:
#         component = MyComponent('...', ResourceOptions(providers={
#            'aws': useast1,
#            'gcp': myproject,
#            'kubernetes': myk8s,
#           }))

    def register_github_endpoint(self):
        '''TODO github'''
        pass 
    def register_bitbucket_endpoint(self):
        '''TODO github'''
        pass
