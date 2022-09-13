""" The magic part with self-made-build.
"""
import pulumi
import pulumi_gcp as gcp

from lib.ric_config import MyProject, MyRegion, AppName, AppNameLower, PulumiStack, PulumiProject, PulumiUser, ShortPulumiProject, print_red

RepoConfig = {}





def create_cloud_build_trigger():
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
                "_GCP_REGION": MyRegion,
                "_GCP_PROJECT": MyProject,
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

