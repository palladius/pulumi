#!/bin/bash

export STACK_DELENDUM="${1:-changeme}"

set -x 
set -e

echo "Beware this destroys a stack entirely (after tearing down its resources)"
pulumi stack select "$STACK_DELENDUM"
pulumi down --yes 
#pulumi destroy --yes
pulumi stack rm "$STACK_DELENDUM" --yes