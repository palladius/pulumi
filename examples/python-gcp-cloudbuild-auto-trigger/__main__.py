"""A Google Cloud Python Pulumi program"""

import pulumi
from pulumi_gcp import storage
import pulumi_gcp as gcp
import os


# TODO Refactor in CArlessian Pulumi file :)
import lib.ric_config

from lib.ric_config import MyProject, MyRegion, AppName, AppNameLower, BitBucketRepoName, PulumiStack, PulumiProject

RepoConfig = {}

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

    # Setting up repo..
    RepoConfig["branch_name"] = pulumi.Config().get('gcb_branch_name') or 'master'
    RepoConfig["repo_name"] = pulumi.Config().get('gcb_repo_name') or 'pulumi'


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

    code_local_path = pulumi.Config().require('rmp-code-folder').strip("/")
    filename_local_path = f'{code_local_path}/cloudbuild/cloudbuild.yaml'

    pulumi_autobuild_trigger = gcp.cloudbuild.Trigger(
        f"pu-{PulumiProject}-meta-trigger",
        filename=filename_local_path,
        substitutions={
          #  "_ARTIFACT_REPONAME": "golden-node-pulumi", # TODO pulumi.export('artifact_repo_name', my_repo.name)
          #  "_DEPLOY_REGION": MyRegion,
          #  "_REGION": MyRegion,
          #  "_DEPLOY_UNIT": "pulumi-self", # :a posso chiamare GoldeNNode ma per capirci rtispetto all'altro, poi quando funge la cambio
            "_PULUMI_PROJECT": PulumiProject,
            "_PULUMI_STACK": PulumiStack,
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
            branch_name=RepoConfig["branch_name"] , # "master", # not MAIN :/
            repo_name=RepoConfig["repo_name"], # "bitbucket_palladius_gprojects", # scoperto con $ gcloud beta builds triggers describe 9667bf06-41a8-4a04-b9cf-d908ba868c4a
        ))
    pulumi.export('cloudbuild_trigger_long_id',pulumi_autobuild_trigger.id)
    pulumi.export('cloudbuild_trigger_short_id',pulumi_autobuild_trigger.trigger_id) # short

def setup_apis():
    """Apparently Cloud Build API is not set up automatically. Damn. """
    for service in ['container', "cloudbuild", "iam"]:
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
    action05_create_cloud_build_trigger()


if __name__ == "__main__":
    main()
