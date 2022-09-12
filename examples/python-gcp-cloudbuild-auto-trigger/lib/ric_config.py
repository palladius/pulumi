import pulumi

AppName = "⬣ Cloud Build trigger with 🧹Pulumi in 🐍 Python"
AppNameLower = "gcb-py-gh-trigger"
MyRegion = pulumi.Config('gcp').require('region')
MyProject = pulumi.Config('gcp').require('project')
BitBucketRepoName = 'bitbucket_palladius_gprojects' # TODO(ricc): move to parameter
PulumiProject =  pulumi.get_project() # https://www.pulumi.com/docs/intro/concepts/project/#stack-settings-file
PulumiStack =  pulumi.get_stack() # https://www.pulumi.com/docs/intro/concepts/project/#stack-settings-file
ShortPulumiProject = PulumiProject[0:20] # I chose a very verbose name - better to shorten it :)

InterestingConfigs = [
    'cloud-build-executing-script-at',
    'cloud-build-executing-script-on',
    'cloud-build-executing-script-gitlast',
    'favourite_color']
#pulumi.export(, pulumi.Config().require('favourite_color'))
# only once do..
for config_name in InterestingConfigs:
    pulumi.export(config_name, pulumi.Config().get(config_name))


def pyellow(str):
    print( f"\033[1;33m{str}\033[0m\n")
def print_red(str):
    print( f"\033[1;31m{str}\033[0m\n")
def puts(str):
    print( f"{str}\n")
