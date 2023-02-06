"""A Google Cloud Python Pulumi program"""

import pulumi
from pulumi_gcp import storage
import pulumi_gcp as gcp
import os


# TODO Refactor in Carlessian Pulumi file :)
import lib # .ric_config

from lib.ric_config import MyProject, MyRegion, AppName, AppNameLower, PulumiStack, PulumiProject, PulumiUser, ShortPulumiProject, print_red

from lib.meta_cloud_build import create_cloud_build_trigger



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
    bucket2 = storage.Bucket(f"test-build-ghent-{ PulumiStack }", location="EU")
    bucket3 = storage.Bucket("hello-ghent-from-{}".format(PulumiStack), location="EU")
    pulumi.export('bucket_name', bucket.url) # the APpName one :)

def setup_gke():
    import lib.setup_gke



def setup_palladius_apps():
    """Reads AppConfig amd oterates through it creating nice k8s stuff"""
    from  lib.setup_palladius_apps import main as pall_main
    #lib.setup_palladius_apps.main
    pall_main()


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
    '''This is the OLD yet working code (v1) with baked in CLoudBuild library'''
    init()
    setup_apis()
    setup_gcs()
    setup_gke()
    setup_palladius_apps()
    # Old way (lib/meta_cloud_build.py)
    create_cloud_build_trigger()
    # New way (Component, currently terraforming but not auto-building, YET)
    #create_cloud_build_triggers_with_new_module() Moved to another folder :) See `../python-gcp-cloudbuild-auto-trigger` instead.
    

if __name__ == "__main__":
    main()
