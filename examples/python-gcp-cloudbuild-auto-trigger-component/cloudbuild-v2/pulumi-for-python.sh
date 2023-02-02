#!/bin/bash

########################################################################################################
# RICCARDO script v2 (from component, more parametric)
# copied from https://github.com/GoogleCloudPlatform/cloud-builders-community/tree/master/pulumi
# ..and riconfigured to use Python 🐍 instead of Node.JS (🧊.☕).
########################################################################################################

# give it to me in arg if you wish :) TODO(ricc): fix this
export PULUMI_USER="${1:-palladius}"
#export PULUMI_USER=`pulumi whoami`

export SCRIPT_VER="1.5_230202ghent"
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

# to select user and project :)
pulumi stack select $PULUMI_USER/$PULUMI_PROJECT/$PULUMI_STACK

# This should hopefully fix the multi-id thing, let me now 
pulumi stack init --copy-config-from $PULUMI_STACK "$MULTIBUILD_STACK_ID"

# TROUBLESHOOT
pulumi config

# For some reason I do not understand, I need to tell the remote system all vars that I have available HERE.
# Oh myabe because i havent checked in the code on git :) even better then :)
# Note that 'this_is_useless_if_you_checkin_the_pulumi_dev_yaml':
  echo 'IMPORTANT. These indented commands are useless if you are committing the Pulumi.STACK.yaml which in my case is .gitignored...'
  pulumi config set gcp:region  "$GCP_REGION"
  pulumi config set gcp:project "$GCP_PROJECT"
  pulumi config set rmp-code-folder "$CODE_SUBFOLDER"
  pulumi config set gcb_repo_type 'github'
  pulumi config set cloud-build-access-token "$PULUMI_ACCESS_TOKEN" --secret
  pulumi config set pulumi-user `pulumi whoami`
  # Volcano is the Greek God of building -> and I see Volcano lava as orange.
  pulumi config set favourite_color 'its all Light Blue here in the Cloud'
  #pulumi config set cbr2c_magic_repos[2].repo bar
  #pulumi config set cbr2c_magic_repos[2].foo baz
  pulumi config set where-am-i "In the Cloud, most likely. Since v$SCRIPT_VER"

  echo 'Note theres something intrinsically broken with this use case. I have N triggers defined locally but when I trigger one to the cloud'
  pulumi config set --path 'cbr2c_magic_repos[0].repo'               'https://github.com/palladius/pulumi/tree/main/examples/python-gcp-cloudbuild-auto-trigger'
  pulumi config set --path 'cbr2c_magic_repos[0].cloudbuild_subpath' 'cloudbuild/cloudbuild.yaml'
  #pulumi config set --path 'cbr2c_magic_repos[1].repo'               'https://github.com/palladius/pulumi/tree/main/examples/python-gcp-cloudbuild-auto-trigger-component'
  #pulumi config set --path 'cbr2c_magic_repos[1].cloudbuild_subpath' 'cloudbuild-v2/cloudbuild.yaml'
  
# NERD part - this is my verbose will to see debug info in the target system. Could probably get them from verbose logs but - hey! I'm enjoying this, ok? :)
pulumi config set cloud-build-executing-script-at "$(date)"
pulumi config set cloud-build-executing-script-on "$(hostname)"
pulumi config set cloud-build-executing-script-version "$SCRIPT_VER"
# https://stackoverflow.com/questions/3357280/print-commit-message-of-a-given-commit-in-git
pulumi config set cloud-build-executing-script-gitlast "$(git log --format=%B -n 1)" # just message of last commit

# prefixing automated part on Cloud Build with the proper git log :)
export AUGMENTED_MESSAGE="[Triggered by GCP 🏗️ Cloud Build in the 🌎‍🌫️☁️🌍☀️ 😶‍🌫️ ⛅ Cloud]
💬💬💬


$(git log --format=%B -n 1)
💬💬💬"

case $BUILD_TYPE in
  # If it's a Pull request, it will output a preview. Notice that this needs to then be piggybacked into GitHub for this msg to be visible there, which will come another day.
  # But at least the CB will PRINT and result into GOOD or BAD.
  PullRequest)
      pulumi preview
      # TODO do sth with a correct or incorrect output (see above)
    ;;
  *)
      # Trigger the pulumi up => change the world.
      pulumi up --yes --message "$AUGMENTED_MESSAGE"
    ;;
esac


