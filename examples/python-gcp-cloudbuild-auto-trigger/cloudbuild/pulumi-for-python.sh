#!/bin/bash

########################################################################################################
# RICCARDO
# copied from https://github.com/GoogleCloudPlatform/cloud-builders-community/tree/master/pulumi
# ..and riconfigured to use Python 🐍 instead of Node.JS (🧊.☕).
########################################################################################################

# function this_is_useless_if_you_checkin_the_pulumi_dev_yaml() {
#   pulumi config set gcp:region  "$GCP_REGION"
#   pulumi config set gcp:project "$GCP_PROJECT"
#   pulumi config set rmp-code-folder "$CODE_SUBFOLDER"
#   pulumi config set gcb_repo_type 'github'
#   pulumi config set cloud-build-access-token "$_INSECURE_SUBSTITUTION_PULUMI_ACCESS_TOKEN"
#   pulumi config set pulumi-user `pulumi whoami`
# }

# give it to me in arg if you wish :) TODO(ricc): fix this
export PULUMI_USER="${1:-palladius}"
#export PULUMI_USER=`pulumi whoami`

SCRIPT_VER="1.2_20220913"
# exit if a command returns a non-zero exit code and also print the commands and their args as they are executed.
set -e -x

# Download and install required tools.
# pulumi
curl -L https://get.pulumi.com/ | bash
export PATH=$PATH:$HOME/.pulumi/bin

# Original: use NPM
#yarn install

# Carlesso: But I'm Python so..
pip install -r requirements.txt

# Login into pulumi. This will require the "PULUMI_ACCESS_TOKEN" environment variable.
pulumi login

# Select the appropriate stack.
# TODO(ricc): use ENV VARS to fix this.
#pulumi stack select $PULUMI_USER/python-gcp-cloudbuild-auto-trigger/dev


# TROUBLESHOOT
#echo
#echo pulumi stack select $PULUMI_USER/$PULUMI_PROJECT/$PULUMI_STACK
#echo

pulumi stack select $PULUMI_USER/$PULUMI_PROJECT/$PULUMI_STACK

# TROUBLESHOOT
pulumi config

# For some reason I do not understand, I need to tell the remote system all vars that I have available HERE.
# Oh myabe because i havent checked in the code on git :) even better then :)
# Note that 'this_is_useless_if_you_checkin_the_pulumi_dev_yaml':
  pulumi config set gcp:region  "$GCP_REGION"
  pulumi config set gcp:project "$GCP_PROJECT"
  pulumi config set rmp-code-folder "$CODE_SUBFOLDER"
  pulumi config set gcb_repo_type 'github'
  pulumi config set cloud-build-access-token "$PULUMI_ACCESS_TOKEN" --secret
  pulumi config set pulumi-user `pulumi whoami`

# NERD part - this is my
pulumi config set cloud-build-executing-script-at "$(date)"
pulumi config set cloud-build-executing-script-on "$(hostname)"
pulumi config set cloud-build-executing-script-version "$SCRIPT_VER"
pulumi config set cloud-build-executing-script-gitlast "$(git show --summary | xargs)" # on single line

case $BUILD_TYPE in
  PullRequest)
      pulumi preview
    ;;
  *)
      pulumi up --yes
    ;;
esac


