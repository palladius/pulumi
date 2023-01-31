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
import re


## Utilities
def infer_repo_service_from_name(url):
        if re.match("^https://github.com/", url):
            return 'github'
        if re.match("^https://bitbucket.org", url):
            return 'bitbucket'
        raise Exception(
            f"Exception: unknown GIT provider (I only know GH and BB): {url}"
        )


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
        self.gcb_repo_type = infer_repo_service_from_name(magic_repo_url)


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
            "cbrc_bucket_url": bucket.url,                  # also id, selfLink
            "cbrc_gcb_repo_type": args.gcb_repo_type,
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


        
    def create_cloud_build_trigger(self):
        """This was SO EASY to do with BitBucket but hard on GH. Damn.

        Code: https://github.com/pulumi/pulumi-gcp/blob/master/sdk/python/pulumi_gcp/cloudbuild/trigger.py
        """

        code_local_path = code_folder.strip("/") # pulumi.Config().require('rmp-code-folder').strip("/")
        filename_local_path = f'{code_local_path}/cloudbuild/cloudbuild.yaml'
        trigger_type = gcb_repo_type # pulumi.Config().require('gcb_repo_type') # must be 'github' or 'bitbucket'
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
            RepoConfig["gcb_gh_owner"] = pulumi.Config().get('gcb_gh_owner') or DefaultGithubOwner
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
                    repo_name=RepoConfig["gcb_repo_name"], # eg, "bitbucket_palladius_gprojects", # scoperto con $ gcloud beta builds triggers describe 9667bf06-41a8-4a04-b9cf-d908ba868c4a
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

