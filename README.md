This repo contains a number of folders with self-living examples.

* 🍹[First (python-gcp-cloudbuild-auto-trigger)](https://github.com/palladius/pulumi/tree/main/examples/python-gcp-cloudbuild-auto-trigger)
  is about creating a trigger on GCP Cloud Build (in Python) which automatically launches pulumi up of its own.
  So hopefully whenever you do a commit, it will just launch a `pulumi up` :)
* 🍹[Second (python-gcp-cloudbuild-auto-trigger-component)](https://github.com/palladius/pulumi/tree/main/examples/python-gcp-cloudbuild-auto-trigger-component)
  Same as above, but a `v2` which creates a component and is a bit more parametric into variables. You give it N repos in config and it creates N autobuilds on
  your project.
* [work in progress] `gcp-py-e2e-tiamat`. A project i'm working on with Xiang (awesome Googler and pulumi *connaisseur*). More to follow.

## Contributing

Please send PRs!
