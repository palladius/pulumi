#!/bin/bash

export STACK_DELENDUM="${1:-changeme}"

set -x 
set -e

echo "Beware this destroys a stack entirely (after tearing down its resources)"
echo '🅰️ Also note this turns off Cloud Build API, so consider removing that and adding to the README as a prerequisite.'
pulumi stack select "$STACK_DELENDUM"
pulumi down --yes 
#pulumi destroy --yes
pulumi stack rm "$STACK_DELENDUM" --yes