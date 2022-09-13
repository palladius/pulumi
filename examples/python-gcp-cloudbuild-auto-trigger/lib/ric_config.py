import os
import pulumi

######################
# Functions
######################
def pyellow(str):
    print( f"\033[1;33m{str}\033[0m\n")
def print_red(str):
    print( f"\033[1;31m{str}\033[0m\n")
def puts(str):
    print( f"{str}\n")
def pulumi_whoami():
    stream = os.popen('pulumi whoami')
    output = stream.read()
    return output.rstrip()
def pulumi_com_readme_url():
    return f"https://app.pulumi.com/{ pulumi_whoami() }/{ PulumiProject }/{ PulumiStack }/readme"


AppName = "⬣ Cloud Build trigger with 🧹Pulumi in 🐍Python"
AppNameLower = "gcb-py-gh-trigger"
MyRegion = pulumi.Config('gcp').require('region')
MyProject = pulumi.Config('gcp').require('project')
#BitBucketRepoName = 'bitbucket_palladius_gprojects' # TODO(ricc): move to parameter
PulumiProject =  pulumi.get_project() # https://www.pulumi.com/docs/intro/concepts/project/#stack-settings-file
PulumiStack =  pulumi.get_stack() # https://www.pulumi.com/docs/intro/concepts/project/#stack-settings-file
PulumiUser =  pulumi.Config().require('pulumi-user') # `pulumi whoami`.rstrip() # 'palladius'
PulumiUserAlternative = pulumi_whoami()
ShortPulumiProject = PulumiProject[0:20] # I chose a very verbose name - better to shorten it :)
InterestingConfigs = [
    'cloud-build-executing-script-at',
    'cloud-build-executing-script-on',
    'cloud-build-executing-script-gitlast',
    'favourite_color',
    'pulumi-user',
]
# only once do..
for config_name in InterestingConfigs:
    pulumi.export(config_name, pulumi.Config().get(config_name))

pulumi.export('PulumiUser', PulumiUser)
pulumi.export('PulumiUserAlternative', PulumiUserAlternative)
pulumi.export('pulumi-readme-url', pulumi_com_readme_url() )

#https://app.pulumi.com/palladius/python-gcp-cloudbuild-auto-trigger/staging/readme
