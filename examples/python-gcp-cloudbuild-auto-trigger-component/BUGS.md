
=================================================================
[SOLVEd] Bug 2feb22


    error: an unhandled error occurred: program exited with non-zero exit code: 1
        please set a value using the command `pulumi config set python-gcp-cloudbuild-auto-trigger-component:cbr2c_magic_repos <value>`
    error: Missing required configuration variable 'python-gcp-cloudbuild-auto-trigger-component:cbr2c_magic_repos'
  pulumi:pulumi:Stack (python-gcp-cloudbuild-auto-trigger-component-staging-ghent):
Diagnostics:

=================================================================
[OPEN] Bug/002 3feb22

Maybe cross-building can be problematic and requires more thought.
Maybe I need to abandon multibuild and leave the array OUT?!?


=================================================================
ERROR: build step 0 "python" failed: step exited with non-zero status: 255
ERROR
error: provided project name "python-gcp-cloudbuild-auto-trigger-component" doesn't match Pulumi.yaml

Previewing update (palladius/python-gcp-cloudbuild-auto-trigger-component/tmpmb-dev-ghent_id1)
💬💬💬'
moved to v1


💬💬💬
+ pulumi up --yes --message '[Triggered by GCP 🏗️ Cloud Build in the 🌎‍🌫️☁️🌍☀️ 😶‍🌫️ ⛅ Cloud]
+ case $BUILD_TYPE in
💬💬💬'
moved to v1


💬💬💬
+ AUGMENTED_MESSAGE='[Triggered by GCP 🏗️ Cloud Build in the 🌎‍🌫️☁️🌍☀️ 😶‍🌫️ ⛅ Cloud]
💬💬💬'
moved to v1


💬💬💬
+ export 'AUGMENTED_MESSAGE=[Triggered by GCP 🏗️ Cloud Build in the 🌎‍🌫️☁️🌍☀️ 😶‍🌫️ ⛅ Cloud]
++ git log --format=%B -n 1
+ pulumi config set cloud-build-executing-script-gitlast 'moved to v1'
++ git log --format=%B -n 1
+ pulumi config set cloud-build-executing-script-version 1.4_20230131ghent
+ pulumi config set cloud-build-executing-script-on e8b57416830c
++ hostname
+ pulumi config set cloud-build-executing-script-at 'Fri Feb  3 09:46:27 UTC 2023'
++ date
+ pulumi config set favourite_color 'its all Orange here in the Cloud'
+ pulumi config set pulumi-user palladius
++ pulumi whoami
+ pulumi config set cloud-build-access-token pul-fcf84be07c95ffbc842a3833084a371ba9173ce3 --secret
+ pulumi config set gcb_repo_type github
+ pulumi config set rmp-code-folder examples/python-gcp-cloudbuild-auto-trigger
+ pulumi config set gcp:project cloud-build-ghent-tests
+ pulumi config set gcp:region europe-west1
IMPORTANT. These indented commands are useless if you are committing the Pulumi.STACK.yaml which in my case is .gitignored...
+ echo 'IMPORTANT. These indented commands a
=================================================================