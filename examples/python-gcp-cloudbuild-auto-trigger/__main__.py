"""A Google Cloud Python Pulumi program"""

import pulumi
from pulumi_gcp import storage
import pulumi_gcp as gcp
import os


# TODO Refactor in CArlessian Pulumi file :)
import lib.ric_config

from lib.ric_config import MyProject, MyRegion, AppName, AppNameLower, BitBucketRepoName, PulumiStack, PulumiProject


# exporting lots of stuff for my awesome README :)
def init():
    pulumi.export('myProject', MyProject)
    pulumi.export('project', MyProject)
    pulumi.export('myRegion', MyRegion)
    pulumi.export('app_name', AppName)
    pulumi.export('appNameLower', AppNameLower)
    #pulumi.export('AppName', os.environ['APPNAME'])
    pulumi.export('BitBucketRepoName', BitBucketRepoName)
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
    bucket = storage.Bucket("prova123", location="EU")
    pulumi.export('bucket_name', bucket.url)

def setup_gke():
    import lib.setup_gke



def setup_palladius_apps():
    """Reads AppConfig amd oterates through it creating nice k8s stuff"""
    import lib.setup_palladius_apps


def action05_create_cloud_build_trigger():

    # pulumi.export('cloudbuild_trigger_long_id',filename_trigger.id)
    # pulumi.export('cloudbuild_trigger_short_id',filename_trigger.trigger_id) # short
    code_local_path = pulumi.Config().require('rmp-code-folder').strip("/")

    pulumi_autobuild_trigger = gcp.cloudbuild.Trigger(
        "kuberic-pulumi-meta-trigger",
        #filename=f"{code_local_path}/cloudbuild/cloudbuild.yaml",
        filename='pulumi/2022-09-10-kuberic/cloudbuild/cloudbuild.yaml',
        substitutions={
          #  "_ARTIFACT_REPONAME": "golden-node-pulumi", # TODO pulumi.export('artifact_repo_name', my_repo.name)
          #  "_DEPLOY_REGION": MyRegion,
          #  "_REGION": MyRegion,
          #  "_DEPLOY_UNIT": "pulumi-self", # :a posso chiamare GoldeNNode ma per capirci rtispetto all'altro, poi quando funge la cambio
            "_NOTULE_SOLLAZZI": "devo prima fare OUTING di rmp-code-folder",
            "_INSECURE_SUBSTITUTION_PULUMI_ACCESS_TOKEN": pulumi.Config().require('cloud-build-access-token'),
        },
        description="""[pulumi] This trigger tried to build pulumi,with pulumi provided script.
        TODO(ricc): find proper directory when to run pulumi.sh
        """,
        included_files=[
            f"{code_local_path}/**", # should be JUST the app part...
        ],
        tags=["pulumi","meta", "wip", "fine-grained"],
        trigger_template=gcp.cloudbuild.TriggerTriggerTemplateArgs(
            branch_name="master", # not MAIN :/
            repo_name="bitbucket_palladius_gprojects", # scoperto con $ gcloud beta builds triggers describe 9667bf06-41a8-4a04-b9cf-d908ba868c4a
        ))
    pulumi.export('cloudbuild_trigger_long_id',pulumi_autobuild_trigger.id)
    pulumi.export('cloudbuild_trigger_short_id',pulumi_autobuild_trigger.trigger_id) # short


def main():
    init()
    setup_gcs()
    setup_gke()
    setup_palladius_apps()
    action05_create_cloud_build_trigger()


if __name__ == "__main__":
    main()
