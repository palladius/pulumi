import pulumi

AppName = "Pulumi🥑Ricc🧊Kube"
AppNameLower = "kuberic"
MyRegion = pulumi.Config('gcp').require('region')
MyProject = pulumi.Config('gcp').require('project')
BitBucketRepoName = 'bitbucket_palladius_gprojects' # TODO(ricc): move to parameter
PulumiProject =  pulumi.get_project() # https://www.pulumi.com/docs/intro/concepts/project/#stack-settings-file
PulumiStack =  pulumi.get_stack() # https://www.pulumi.com/docs/intro/concepts/project/#stack-settings-file

InterestingConfigs = [
    'cloud-build-executing-script-at',
    'cloud-build-executing-script-on',
    'cloud-build-executing-script-gitlast',
    'favourite_color']
#pulumi.export(, pulumi.Config().require('favourite_color'))
# only once do..
for config_name in :
    pulumi.export(config_name, pulumi.Config().require(config_name))


def pyellow(str):
    print( f"\033[1;33m{str}\033[0m\n")
def puts(str):
    print( f"{str}\n")
