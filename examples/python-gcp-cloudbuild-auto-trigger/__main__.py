"""A Google Cloud Python Pulumi program"""

import pulumi
from pulumi_gcp import storage
import pulumi_gcp as gcp
import os


# TODO Refactor in CArlessian Pulumi file :)
import lib.ric_config

from lib.ric_config import MyProject, MyRegion, AppName, AppNameLower, BitBucketRepoName,                        PulumiStack, PulumiProject, PulumiUser, ShortPulumiProject, print_red

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
    """This was SO EASY to do with BitBucket but hard on GH. Damn.

    Code: https://github.com/pulumi/pulumi-gcp/blob/master/sdk/python/pulumi_gcp/cloudbuild/trigger.py
    """

    code_local_path = pulumi.Config().require('rmp-code-folder').strip("/")
    filename_local_path = f'{code_local_path}/cloudbuild/cloudbuild.yaml'
    trigger_type = pulumi.Config().require('gcb_repo_type') # must be 'github' or 'bitbucket'
    RepoConfig["gcb_repo_type"] = trigger_type
    # raise exception unless ...

    # Common Config
    trigger_name = f"pu-{ShortPulumiProject}-meta-trigger-{trigger_type}"
    common_substitutions = {
                "_PULUMI_PROJECT": PulumiProject,
                "_PULUMI_USER": PulumiUser,
                "_PULUMI_STACK": PulumiStack,
                #"_NOTULE_DE_LI_SOLLAZZI": "Carlessian notes to self in - ENVironmental friendly", # put stuff here if you need to talk to yourself in the UI
                "_INSECURE_SUBSTITUTION_PULUMI_ACCESS_TOKEN": pulumi.Config().require('cloud-build-access-token'),
                "_CODE_SUBFOLDER":  pulumi.Config().require('rmp-code-folder'),
            }

    # Case 1. GITHUB
    if trigger_type == 'github':
        # GH documented here: https://www.pulumi.com/registry/packages/gcp/api-docs/cloudbuild/trigger/#triggergithub
        RepoConfig["gcb_gh_name"] = pulumi.Config().get('gcb_gh_name') or 'pulumi'
        RepoConfig["gcb_gh_owner"] = pulumi.Config().get('gcb_gh_owner') or 'palladius'
        RepoConfig["gcb_gh_branch"] = pulumi.Config().get('gcb_gh_branch') or "^main$"
        # trigger_template_github = gcp.cloudbuild.TriggerTriggerTemplateArgs(
        #     #branch_name=RepoConfig["branch_name"] , # "master", # not MAIN :/
        #     github=gcp.cloudbuild.TriggerGithubArgs(
        #         name=RepoConfig["gcb_gh_name"],
        #         owner=RepoConfig["gcb_gh_owner"],
        #     )
        # )
        trigger_github_args = gcp.cloudbuild.TriggerGithubArgs(
                name=RepoConfig["gcb_gh_name"],
                owner=RepoConfig["gcb_gh_owner"],
                # documented here: https://www.pulumi.com/registry/packages/gcp/api-docs/cloudbuild/trigger/#triggergithubpullrequest
                #pull_request=
                #pull_request=gcp.cloudbuild.TriggerGithubPullRequest(),
                push=gcp.cloudbuild.TriggerGithubPushArgs(
                    branch="^main$",
                ),

                #pull_request=gcp.cloudbuild.TriggerGithubPullRequest(
                #    branch='main', # RepoConfig["gcb_gh_branch"]
                #),
                #push=gcp.cloudbuild.TriggerGithubPush(
                #    branch='main', # RepoConfig["gcb_gh_branch"]
                #),
            )
        pulumi_autobuild_trigger = gcp.cloudbuild.Trigger(
            trigger_name,
            filename=filename_local_path,
            substitutions=common_substitutions,
            description="""[pulumi] This meta-trigger tries to build itself from a GitHUb repo. wOOt!
            """[0:99], # max 100 chars
            included_files=[
                f"{code_local_path}/**", # should be JUST the app part...
            ],
            tags=["pulumi","meta"],
            #trigger_template=trigger_template_bitbucket
            github=trigger_github_args,
            )

    # Case 2. BitBucket
    elif trigger_type == 'bitbucket':
        # todo when GH works, create a config which gicves everything.
        # This code is for BitBucket mirror:
        RepoConfig["gcb_branch_name"] = pulumi.Config().get('gcb_branch_name') or 'master'
        RepoConfig["gcb_repo_name"] = pulumi.Config().get('gcb_repo_name') or 'pulumi'


        trigger_template_bitbucket = gcp.cloudbuild.TriggerTriggerTemplateArgs(
                branch_name=RepoConfig["gcb_branch_name"] , # "master", # not MAIN :/
                repo_name=RepoConfig["gcb_repo_name"], # "bitbucket_palladius_gprojects", # scoperto con $ gcloud beta builds triggers describe 9667bf06-41a8-4a04-b9cf-d908ba868c4a
        )
        pulumi_autobuild_trigger = gcp.cloudbuild.Trigger(
            trigger_name,
            filename=filename_local_path,
            substitutions=common_substitutions,
            description="""[pulumi] This meta-trigger tries to build itself from a BitBucket repo. wOOt!
            """[0:99], # max 100 chars
            included_files=[
                f"{code_local_path}/**", # should be JUST the app part...
            ],
            tags=["pulumi","meta"],
            trigger_template=trigger_template_bitbucket)
    else:
        print_red(f"[FATAL] Hey! Unknown trigger_type: '{trigger_type}'. Exiting! Get your config together my friend!")
        exit(42)
    pulumi.export('cloudbuild_trigger_long_id',pulumi_autobuild_trigger.id)
    pulumi.export('cloudbuild_trigger_short_id',pulumi_autobuild_trigger.trigger_id) # short
    pulumi.export('RepoConfig',RepoConfig) # todo export array


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
