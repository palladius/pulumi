# ${outputs.app_name} v${outputs.version} (AutoKube and AutoBuild)

This part 1 is a super cool project from **Riccardo**. This is a pulumization of my very first sample app.

Self: Code is contained in [GH palladius/pulumi](https://github.com/palladius/pulumi/), under `python-gcp-cloudbuild-auto-trigger` (TODO make this an `outputs.code_path`)

## 😃 What works 😃

Testing how to get the ⬢GCP⬡ config:

* ⬢ ProjectId (as output): **${outputs.myProject}**
* ⬢ Region (as output): **${outputs.myRegion}**

What I've created here:

* 🧹AppName: **${outputs.appNameLower}** (Native)
* ⬢ GCS Bucket: **`${outputs.bucket_name}`** (useless but why not)
* ⬢ GKE Cluster  **`${outputs.k8s_cluster_name}`** (all clusters: https://console.cloud.google.com/kubernetes/list/overview?project=${outputs.myProject})
  * ⬢ Nginx service with public Ip: http://${outputs.ingress_ip}/

Pulumi config:

* 🧹 pulumi_stack:  **`${outputs.pulumi_stack}`**
* 🧹 pulumi_project:  **`${outputs.pulumi_project}`**
* 🥑 My fav color is **${outputs.favourite_color}**, because color is important.

* CloudBuild 🏗️ trigger 🔫: ${outputs.cloudbuild_trigger_long_id}
  * ALL Triggers: https://console.cloud.google.com/cloud-build/triggers?project=${outputs.project}

# What's amazing

* **Cloud Build 🏗️ Automation WORKS**!!!
* TODO image when it works from README :)

# What's still missing 😞😰🙄

* sample Carlessian manifests (code in)

# Cloud Build Latest stats

Riccardo, getting more&more sophisticated here. Cloud Build shell script `pulumi.sh` is now tracing a few thingies you might wanna check:

```
pulumi config set cloud-build-executing-script-at      "$(date)"
pulumi config set cloud-build-executing-script-on      "$(hostname)"
pulumi config set cloud-build-executing-script-version "$SCRIPT_VER"
pulumi config set cloud-build-executing-script-gitlast "$(git show --summary | xargs)"
```
.. which brings us to these outputs being created by every successful invokation of Cloud Build:

* ⬡ Date =>  **${outputs.cloud-build-executing-script-at}**
* ⬡ **Hostname** (not so meaningful) =>  **${outputs.cloud-build-executing-script-on}**
* ⬡ Script version =>  <tt>${outputs.cloud-build-executing-script-version}</tt>
* ⬡ Git Last **comment** =>  **<tt>${outputs.cloud-build-executing-script-gitlast}'</tt>**

# TODOs

* make this a reusable module.
* Use GCP for secrets management (`KMS` or `GCS`) as promised to cstanger@
* Looks like Chris is impressed by this REAMDE.

# More pointers

Googlers, see go/ricc-pulumi

*RiccardoNotes*: **${outputs.riccardo_notes}**

This is VERY meta: ${outputs.pulumi-readme-url}
