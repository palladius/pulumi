#!/bin/bash

#--color
pulumi stack output  PulumiUser
pulumi config get gcp:project

gcloud --project "$(pulumi config get gcp:project)" builds triggers list