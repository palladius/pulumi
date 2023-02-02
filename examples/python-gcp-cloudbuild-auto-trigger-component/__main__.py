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
    bucket3 = storage.Bucket("hello-ghent-from-{}".format(PulumiStack), location="EU")
    pulumi.export('bucket_name', bucket.url) # the APpName one :)

# def setup_gke():
#     import lib.setup_gke



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

def create_cloud_build_triggers_with_new_module():

    UberReposConfig = []
    #myCloudBuildRepos = []
    myCloudBuildRepos = []
    CloudBuildAccessToken = pulumi.Config().require('cloud-build-access-token')
    # Second generation, 2B implemented:
    myNextGenerationCloudReposFromStackConfig = pulumi.Config().require_object('cbr2c_magic_repos')
    #print("DEB: myNextGenerationCloudReposFromStackConfig: ", myNextGenerationCloudReposFromStackConfig)
    for ix, magic_repo_hash in enumerate(myNextGenerationCloudReposFromStackConfig):
        print(f"DEB[cbr2c_repo #{ix}] => '''{magic_repo_hash}'''")
        myComponent = CloudBuildRiccComponent(f"configrepo{ix}", CloudBuildRiccComponentArgs(
            magic_repo_hash['repo'],
            CloudBuildAccessToken,
            None,
            None,
            magic_repo_hash['cloudbuild_subpath'],
            ix,
            magic_repo_hash['description'],            
        ))
        UberReposConfig.append(myComponent.repo_config)

    for cbr2c_repo in myCloudBuildRepos:
        UberReposConfig.append(cbr2c_repo.repo_config)
    # OUTPUTS:
    pulumi.export("cbr2c_uber_config", UberReposConfig)

def main():
    init()
    setup_apis()
    setup_gcs()
    #setup_gke()
    setup_palladius_apps()
    # Old way (lib/meta_cloud_build.py)
    if  pulumi.Config().get('activate-old-v1-build-too') == 'yes-i-am-sure':
        create_cloud_build_trigger()
    # New way (Component, currently terraforming but not auto-building, YET)
    create_cloud_build_triggers_with_new_module()
    
if __name__ == "__main__":
    main()













      # I get an error like this was NOT connected. When i validate it on GH, it has a different icons, since this is NOT my repo,
        # its a branch of another repo
        # CloudBuildRiccComponent("pally-examples",CloudBuildRiccComponentArgs(
        #     # https://github.com/palladius/examples/tree/master/gcp-py-cloudrun-cloudsql
        #     'https://github.com/palladius/examples', # Fork of https://github.com/pulumi/examples/ .. cant connect to repo i dont own :/
        #     pulumi.Config().require('cloud-build-access-token'),
        #     'gcp-py-cloudrun-cloudsql/', # https://github.com/pulumi/examples/tree/master/gcp-py-cloudrun-cloudsql
        #     'master',X
        #     # => https://github.com/palladius/examples/tree/master/gcp-py-cloudrun-cloudsql
        # )),
    # myCloudBuildRepos.append(CloudBuildRiccComponent("ricc-bitbucky-should-work",CloudBuildRiccComponentArgs(
    #         'https://bitbucket.org/palladius/gprojects/',
    #         CloudBuildAccessToken,
    #         'pulumi/20220910-kuberic/',
    #         'master',
    #     ))
    # )
    # myCloudBuildRepos.append(
    #     CloudBuildRiccComponent("riccardo-pulumi",CloudBuildRiccComponentArgs(
    #         'https://github.com/palladius/pulumi/',
    #         pulumi.Config().require('cloud-build-access-token'),
    #         'examples/python-gcp-cloudbuild-auto-trigger/',
    #         'main',
    #     ))
    # )
    # myCloudBuildRepos.append(
    #     CloudBuildRiccComponent("folder-validator-todo",CloudBuildRiccComponentArgs(
    #         'https://github.com/palladius/pulumi-folders-validator/',
    #         pulumi.Config().require('cloud-build-access-token'),
    #         'examples/gcp-py-cloudrun-cloudsql/', # just added :)
    #         'main',
    #     )),
    # )
    # myCloudBuildRepos.append(
    #     CloudBuildRiccComponent("chiabox",CloudBuildRiccComponentArgs(
    #         'https://github.com/palladius/gcp-pulumi-challenge-in-a-box/',
    #         CloudBuildAccessToken,
    #         'gcp-pulumi-challenge/', # still doesnt exist... for tomorrow
    #         'main',
    #     )),
    #)
    #]