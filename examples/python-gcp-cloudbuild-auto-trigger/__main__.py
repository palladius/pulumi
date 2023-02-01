"""A Google Cloud Python Pulumi program"""

import pulumi
from pulumi_gcp import storage
import pulumi_gcp as gcp
import os


# TODO Refactor in Carlessian Pulumi file :)
import lib # .ric_config

from lib.ric_config import MyProject, MyRegion, AppName, AppNameLower, PulumiStack, PulumiProject, PulumiUser, ShortPulumiProject, print_red

from lib.meta_cloud_build import create_cloud_build_trigger
from lib.cloud_build_ricc_component import *


#RepoConfig = {}

# exporting lots of stuff for my awesome README :)
def init():
    pulumi.export('myProject', MyProject)
    pulumi.export('project', MyProject)
    pulumi.export('myRegion', MyRegion)
    pulumi.export('app_name', AppName)
    pulumi.export('appNameLower', AppNameLower)
    #pulumi.export('AppName', os.environ['APPNAME'])
    #pulumi.export('BitBucketRepoName', BitBucketRepoName)
    with open('./Pulumi.README.md') as f:
        pulumi.export('readme', f.read())
    with open('./VERSION') as f:
        pulumi.export('version', f.read().rstrip())

    # config export
    pulumi.export('rmp-code-folder', pulumi.Config().get('rmp-code-folder'))
    pulumi.export('pulumi_stack', PulumiStack) # https://stackoverflow.com/questions/69078303/abstracting-configuration-in-pulumi
    pulumi.export('pulumi_project', PulumiProject) # https://stackoverflow.com/questions/69078303/abstracting-configuration-in-pulumi
    pulumi.export('riccardo_notes', "init done.")


def setup_gcs():
    bucket = storage.Bucket(AppNameLower, location="EU")
    bucket2 = storage.Bucket("test123", location="EU")
    bucket3 = storage.Bucket("hello-ghent-from-{}".format(PulumiStack), location="EU")
    pulumi.export('bucket_name', bucket.url) # the APpName one :)

def setup_gke():
    import lib.setup_gke



def setup_palladius_apps():
    """Reads AppConfig amd oterates through it creating nice k8s stuff"""
    import lib.setup_palladius_apps


def setup_apis():
    """Apparently Cloud Build API is not set up automatically. Damn. """
    GCPServicesToBeEnabled = ['container', "cloudbuild", "iam"]
    for service in GCPServicesToBeEnabled:
        project = gcp.projects.Service(
            f"enable-srv-{service}",
            disable_dependent_services=True,
            project=MyProject,
            service=f"{service}.googleapis.com")


def main():
    init()
    setup_apis()
    setup_gcs()
    setup_gke()
    setup_palladius_apps()
    create_cloud_build_trigger()
    # Component stuff
    
    UberReposConfig = []
    myCloudBuildRepos = [
        CloudBuildRiccComponent("public-examples",CloudBuildRiccComponentArgs(
            'https://github.com/palladius/examples', # Fork of https://github.com/pulumi/examples/ .. cant connect to repo i dont own :/
            'gcp-py-cloudrun-cloudsql/', # https://github.com/pulumi/examples/tree/master/gcp-py-cloudrun-cloudsql
            pulumi.Config().require('cloud-build-access-token'),
            'masterZZZ',
            # => https://github.com/palladius/examples/tree/master/gcp-py-cloudrun-cloudsql
        )),
        # CloudBuildRiccComponent("ricc-bitbucky-fails",CloudBuildRiccComponentArgs(
        #     'https://bitbucket.org/palladius/gic/',
        #     '',
        #     None,
        # )),
        CloudBuildRiccComponent("ricc-bitbucky-should-work",CloudBuildRiccComponentArgs(
            'https://bitbucket.org/palladius/gprojects/',
            'pulumi/20220910-kuberic/',
            pulumi.Config().require('cloud-build-access-token'),
            'masterZZZ',
        )),
        CloudBuildRiccComponent("riccardo-pulumi",CloudBuildRiccComponentArgs(
            'https://github.com/palladius/pulumi/',
            'examples/python-gcp-cloudbuild-auto-trigger/',
            pulumi.Config().require('cloud-build-access-token'),
            'main',
        )),
        CloudBuildRiccComponent("folder-validator-todo",CloudBuildRiccComponentArgs(
            'https://github.com/palladius/pulumi-folders-validator/',
            'examples/example1/', # still doesnt exist... for tomorrow
            pulumi.Config().require('cloud-build-access-token'),
            'main',
        )),
        CloudBuildRiccComponent("challenge-in-a-box",CloudBuildRiccComponentArgs(
            'https://github.com/palladius/gcp-pulumi-challenge-in-a-box/',
            'gcp-pulumi-challenge/', # still doesnt exist... for tomorrow
            pulumi.Config().require('cloud-build-access-token'),
            'main',
        )),
        
    ]
    # Second generation, 2B implemented:
    myNextGenerationCloudReposFromStackConfig = pulumi.Config().require('cbrc_magic_repos')
    for ix, cbrc_repo in enumerate(myNextGenerationCloudReposFromStackConfig):
        myComponent = CloudBuildRiccComponent(f"cbrc_magic_repo{ix}", CloudBuildRiccComponentArgs(
            cbrc_repo,
            None,
            pulumi.Config().require('cloud-build-access-token'),
            None,
        ))
        UberReposConfig.append(myComponent.repo_config)

    for cbrc_repo in myCloudBuildRepos:
        UberReposConfig.append(cbrc_repo.repo_config)
    #TODO output
    pulumi.export("cbrc_uber_config", UberReposConfig)


    

if __name__ == "__main__":
    main()
