'''My first python component! This wraps around a Cloud Build trigger and looks for a specific folder 
on BB or GH.

Some docs:
* https://github.com/pulumi/examples/tree/master/classic-azure-py-webserver-component
* https://github.com/pulumi/examples/blob/master/classic-azure-py-webserver-component/webserver.py

Supported CLoud Build repos (of 6 available):

1. GitHub (Cloud Build GitHub App)
   Build source code in response to pull requests and pushes.
   Riccardo calls it 'github'

2. GHE - nope

3. GHEE - nope

4. BB S - nope

5. BB DC - nope

6. Bitbucket Cloud (mirrored) BETA
   Build source code in response to pushes, mirrored through Cloud Source Repositories.
   Riccardo calls it 'bitbucket'

File a PR to add new functionality!
'''

import pulumi
import pulumi_gcp as gcp
#from pulumi_gcp import storage
from pulumi import asset, Input, Output, ComponentResource, ResourceOptions

from lib.ric_config import MyProject, MyRegion, AppName, AppNameLower, PulumiStack, PulumiProject, PulumiUser, ShortPulumiProject, print_red
import re

AcceptedRepos = ['bitbucket', 'github' ]
# DefaultBranchByRepo = {
#     # TODO remove default when it works :)
#     "bitbucket": "master-default", 
#     "github": "main-default",
# }

## Utilities
def infer_repo_service_from_url(url):
    if re.match("^https://github.com/", url):
        return 'github'
    if re.match("^https://bitbucket.org", url):
        return 'bitbucket'
    raise Exception(
        f"Exception: unknown GIT provider (I only know GH and BB): '{url}'"
    )

def infer_shortened_repo_service_from_url(url):
    '''Sorry for the repetition :)'''
    if re.match("^https://github.com/", url):
        return 'gh'
    if re.match("^https://bitbucket.org", url):
        return 'bb'
    raise Exception(
        f"Exception: unknown GIT provider (I only know GH and BB): {url}"
    )

def infer_repo_owner_from_url(magic_repo_url):
    '''

    https://github.com/palladius/clouddeploy-platinum-path => "palladius"
    https://bitbucket.org/palladius/foo/src/master/        => "palladius"
    '''
    # Should be the FOURTH part:
    # ['https:', '', 'bitbucket.org', 'palladius', 'foo', 'src', 'master', '']
    print(f"DEBUG: infer_repo_owner_from_url({magic_repo_url}) => { magic_repo_url.split('/')[3]}")
    return magic_repo_url.split('/')[3]

def infer_repo_name_from_url(magic_repo_url):
    '''
    https://github.com/palladius/clouddeploy-platinum-path/ => "clouddeploy-platinum-path"
    https://bitbucket.org/palladius/foo/src/master/path/to/folder        => "foo"
    '''
    # Should be the FIRTH OF FIFTH part:
    # ['https:', '', 'bitbucket.org', 'palladius', 'foo', 'src', 'master', '']
    print(f"DEBUG: infer_repo_name_from_url({magic_repo_url}) => { magic_repo_url.split('/')[4]}")
    return magic_repo_url.split('/')[4]


# OBSOLETE!!!
# def infer_branch_from_args_OBSOLETE(args):
#     '''TODO(ricc): enrich the CloudBuildRiccComponentArgs allowing also this to be specified as optional..
    
#     investigate optional prams in python, in ruby it would be SO wasy!!!
#     '''
#     return 'master'
##############################################################################################################
# BB and GH smart reghexes (I wanted to make sure that an improvement with one would also work with the other)
##############################################################################################################
# These two regexes have the following fields:
# m[0]: user
# m[1]: repo
# m[2]: branch
# m[3]: folder
##############################################################################################################
UberRegex = "^https://{service}/([a-z_-]+)/([a-z_-]+)/{src_or_tree}/([^/]*)/(.*)[/]?$"
BitbucketRegex = UberRegex.format(service='bitbucket.org', src_or_tree='src') 
#"^https://bitbucket.org/([a-z_-]+)/([a-z_-]+)/src/([^/]*)/(.*)[/]?$"
GithubRegex    =   UberRegex.format(service='github.com', src_or_tree='tree') 
#GithubRegex    =    "^https://github.com/(.*)/(.*)/tree/(.*)/(.*)$"


def infer_branch_from_magic_url(magic_repo_url): # eg, 'main'
    '''Will auto infer, if not, will use magic defaults.
    
    https://github.com/pulumi/pulumi/tree/master/tests/examples/formattable => "master"
    https://bitbucket.org/palladius/foo/src/master/path/to/folder        => "master"
    
    '''

    bbm = re.match(BitbucketRegex, magic_repo_url)
    if bbm:
        return bbm.group(3)
    ghm= re.match(GithubRegex, magic_repo_url)
    if ghm:
        return ghm.group(3)
    raise Exception(f"Illogical Regex for infer_branch_from_magic_url('{magic_repo_url}'): this doesnt smell either BB or GH!")
    return 'ERROR-branch' # :)
    return None 


# def get_cloudbuild_subpath(code_local_path):
#     return f"{code_local_path}/cloudbuild/cloudbuild_v2.yaml"

def infer_code_folder_from_magic_url(magic_repo_url): # eg, 'examples/my-pulumi-folder/'
    ''' TODO '''
    #return "todo/cloudbuild_v2/cloudbuild.yaml"
    bbm = re.match(BitbucketRegex, magic_repo_url)
    if bbm:
        return bbm.group(4)
    ghm= re.match(GithubRegex, magic_repo_url)
    if ghm:
        return ghm.group(4)
    raise Exception(f"Illogical Regex for infer_branch_from_magic_url('{magic_repo_url}'): this doesnt smell either BB or GH!")
    return 'ERROR-branch' # :)
    return None 


def get_cloud_build_compatible_branch(branch):
    '''You say master/main  but you really want ^main$.
        Or, if None, you want ANYTHING (".*")
    '''
    if branch == None:
        return '.*'
    return f"^{branch}$"

#        self.repo_owner = infer_repo_owner_from_url(magic_repo_url)
#        self.repo_name = infer_repo_name_from_url(magic_repo_url)
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
        #subnet: network.Subnet,
        #username: Input[str],
        #password: Input[str],
        magic_repo_url: Input[str],
        cdb_access_token: Input[str], # TODO make this mandatory.
        code_folder: Input[str],
        code_branch: Input[str],
        cloudbuild_subpath: Input[str],
        id: Input[str],
        description: Input[str],
    ):
        #self.useless_bucket = useless_bucket
        self.magic_repo_url = magic_repo_url
        self.cdb_access_token = cdb_access_token # or pulumi.Config().require('cloud-build-access-token')
        self.gcb_repo_type = infer_repo_service_from_url(magic_repo_url) # github or bitbucket
        self.gcb_repo_type_short = infer_shortened_repo_service_from_url(magic_repo_url) # BB or GH
        self.repo_owner = infer_repo_owner_from_url(magic_repo_url) # eg, 'palladius'
        self.repo_name = infer_repo_name_from_url(magic_repo_url) # eg, 'kubernetes'
        #self.id = f"tmp-multibuild-{id}" # str(id)
        self.id = f"id{id}" # str(id)
        self.description = description or "No description provided 😭"

        # This is reccommended but the secopnd also works: https://stackoverflow.com/questions/7338501/python-assign-value-if-none-exists
        #self.path_to_cloudbuild = "cloudbuild-v2/cloudbuild.yaml" if cloudbuild_subpath is None else cloudbuild_subpath
        self.path_to_cloudbuild = cloudbuild_subpath or "cloudbuild-v2/cloudbuild.yaml" # if cloudbuild_subpath is None else cloudbuild_subpath

        if code_folder == None and code_branch == None:
            # In this case, I'll use AUTO parsign from URL
            self.branch = infer_branch_from_magic_url(magic_repo_url) # eg, 'main'
            self.code_folder = infer_code_folder_from_magic_url(magic_repo_url) # eg, 'examples/my-pulumi-folder/'
        else:
            self.branch = code_branch # main, master, ..
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

        #self.args = args
        self.name = name

        # # Creating a USELESS bucket.. remove when all works
        # bucket = gcp.storage.Bucket(
        #     "cbr2c-{}".format(name), 
        #     location="EU",
        #     opts=child_opts, # pulumi.ResourceOptions(parent=self)
        # )

        self.create_cloud_build_trigger(args, child_opts)

        # self.register_outputs({
        #     f"cbr2c_{name}_bucket_url": bucket.url,                  # also id, selfLink
        #     #"cbr2c_gcb_repo_type": args.gcb_repo_type,
        # })
        # Calling 'registerOutputs' twice leads to a crash. See https://github.com/pulumi/pulumi/issues/2394 


        
    def create_cloud_build_trigger(self, args, child_opts):
        """This was SO EASY to do with BitBucket but hard on GH. Damn.

        Code: https://github.com/pulumi/pulumi-gcp/blob/master/sdk/python/pulumi_gcp/cloudbuild/trigger.py

        TODO(ricc): dont assume CB yaml is in /cloudbuild/cloudbuild.yaml but make it parametric :)
        """

        #child_opts = ResourceOptions(parent=self)
        RepoConfig = {}

        code_local_path = args.code_folder.strip("/") # pulumi.Config().require('rmp-code-folder').strip("/")
        filename_local_path = f'{code_local_path}/{args.path_to_cloudbuild}' # cloudbuild/cloudbuild.yaml-ish
        trigger_type = args.gcb_repo_type # pulumi.Config().require('gcb_repo_type') # must be 'github' or 'bitbucket'
        RepoConfig["cbr2c_magic_repo_url"] = args.magic_repo_url
        RepoConfig["gcb_repo_type"] = trigger_type
        RepoConfig["cbr2c_name"] = self.name
        RepoConfig["gcb_repo_type_short"] = args.gcb_repo_type_short # infer_shortened_repo_service_from_url(args.code_url)
        RepoConfig["cbr2c_multibuild_id"] = args.id
        RepoConfig["cbr2c_description"] = args.description
        
        
        # raise exception unless ...
        repo_owner = args.repo_owner # infer_repo_owner_from_url(args.magic_repo_url)
        repo_name  = args.repo_name # infer_repo_name_from_url(args.magic_repo_url)
        gcb_branch_name = args.branch

        RepoConfig["miniUrl"] = f"{args.gcb_repo_type_short}://{repo_owner}:{repo_name}/^{gcb_branch_name}"

        if repo_owner.__str__ == '': 
            raise Exception(f"[{name}] Empty repo_owner - failing: {repo_owner}")
        if repo_name.__str__ == '': 
            raise Exception(f"[{name}] Empty repo_name - failing: {repo_name}")

        # Common Config
        #trigger_name = f"cbr2c-{ShortPulumiProject}-tr-{trigger_type}"
        trigger_name = f"cbr2c-{args.id}-{self.name}-{args.gcb_repo_type_short}" # -trigger
        sanitized_trigger_name = trigger_name.replace("_", "-")
        common_substitutions = {
                    "_PULUMI_PROJECT": PulumiProject,
                    "_PULUMI_USER": PulumiUser,
                    "_PULUMI_STACK": PulumiStack,
                    #"_NOTULE_DE_LI_SOLLAZZI": "Carlessian notes to self in - ENVironmental friendly", # put stuff here if you need to talk to yourself in the UI
                    "_INSECURE_SUBSTITUTION_PULUMI_ACCESS_TOKEN": args.cdb_access_token, # pulumi.Config().require('cloud-build-access-token'),
                    "_CODE_SUBFOLDER": args.code_folder, #  pulumi.Config().require('rmp-code-folder'),
                    "_GCP_REGION": MyRegion,
                    "_GCP_PROJECT": MyProject,
                    "_MULTIBUILD_STACK_ID": f"tmp-multibuild-{args.id}", # args.id,
                }

        # Case 1. GITHUB
        if trigger_type == 'github':
            # GH documented here: https://www.pulumi.com/registry/packages/gcp/api-docs/cloudbuild/trigger/#triggergithub
            RepoConfig["gcb_gh_name"] = repo_name  # pulumi.Config().get('gcb_gh_name') or 'pulumi'
            RepoConfig["gcb_gh_owner"] = repo_owner  # pulumi.Config().get('gcb_gh_owner') or DefaultGithubOwner
            RepoConfig["gcb_gh_branch"] = get_cloud_build_compatible_branch(gcb_branch_name)  # f"^{gcb_branch_name}$", master
            # trigger_template_github = gcp.cloudbuild.TriggerTriggerTemplateArgs(
            #     #branch_name=RepoConfig["branch_name"] , # "master", # not MAIN :/
            #     github=gcp.cloudbuild.TriggerGithubArgs(
            #         name=RepoConfig["gcb_gh_name"],
            #         owner=RepoConfig["gcb_gh_owner"],
            #     )
            # )
            #sanitized_repo_name = repo_name.replace("_", "-")
            trigger_github_args = gcp.cloudbuild.TriggerGithubArgs(
                    # This doesnt exist on GitHub -> MaYBE i CAN REMOVE?!?
                    #name= f"{ self.name }-gh-{ github_username }",
                    #name=sanitized_repo_name,
                    name=repo_name,
                    owner=RepoConfig["gcb_gh_owner"],
                    # documented here: https://www.pulumi.com/registry/packages/gcp/api-docs/cloudbuild/trigger/#triggergithubpullrequest
                    push=gcp.cloudbuild.TriggerGithubPushArgs(
                        branch=gcb_branch_name
                    ),
                    #pull_request=gcp.cloudbuild.TriggerGithubPullRequest(
                    #    branch='main', # RepoConfig["gcb_gh_branch"]
                    #),
                    #push=gcp.cloudbuild.TriggerGithubPush(
                    #    branch='main', # RepoConfig["gcb_gh_branch"]
                    #),
                )
            print(f"DEB pre trigger fail: trigger_name=#{trigger_name}, filename={filename_local_path}, trigger_github_args={trigger_github_args}")
            pulumi_autobuild_trigger = gcp.cloudbuild.Trigger(
                sanitized_trigger_name,
                filename=filename_local_path,
                substitutions=common_substitutions,
                description=f"""[pulumi] {args.description}
                --
                This meta-trigger tries to build itself from a GitHUb repo.
                See https://github.com/palladius/pulumi for more info
                """[0:99], # max 100 chars
                included_files=[
                    f"{code_local_path}/**", # should be JUST the app part...
                ],
                tags=["pulumi","meta", "github", 'cbr2c'],
                #trigger_template=trigger_template_bitbucket
                github=trigger_github_args,
                opts=child_opts, 
                )

        # Case 2. BitBucket
        elif trigger_type == 'bitbucket':
            # This code is for BitBucket mirror:
            RepoConfig["gcb_branch_name"] = get_cloud_build_compatible_branch(gcb_branch_name) # pulumi.Config().get('gcb_branch_name') or 'master'
            # Google uses sth like this 'bitbucket_palladius_gprojects' so you need to use same nomenclature
            RepoConfig["gcb_bb_name"] = f"bitbucket_{repo_owner}_{repo_name}" 
            RepoConfig["gcb_bb_owner"] = repo_owner 

            trigger_template_bitbucket = gcp.cloudbuild.TriggerTriggerTemplateArgs(
                    branch_name=RepoConfig["gcb_branch_name"] , # "master", # not MAIN :/
                    repo_name=RepoConfig["gcb_bb_name"], # eg, "bitbucket_palladius_gprojects", # scoperto con $ gcloud beta builds triggers describe 9667bf06-41a8-4a04-b9cf-d908ba868c4a
                    #opts=child_opts, 
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
                tags=["pulumi","meta", "module", "github", 'cbr2c'],
                trigger_template=trigger_template_bitbucket,
                opts=child_opts, 
            )
        else:
            #print_red(f"[FATAL] Hey! Unknown trigger_type: '{trigger_type}'. Exiting! Get your config together my friend!")
            raise Exception(
                f"[FATAL] Hey! Unknown trigger_type: '{trigger_type}'. Exiting! Get your config together my friend!"
            )
            #exit(42)
        pulumi.export('cbr2c_cbt_long_id', pulumi_autobuild_trigger.id)
        pulumi.export('cbr2c_cbt_short_id', pulumi_autobuild_trigger.trigger_id) # short
        pulumi.export(f"cbr2c_config_{self.name}", RepoConfig) # todo export array
        self.repo_config = RepoConfig
        return True
        

