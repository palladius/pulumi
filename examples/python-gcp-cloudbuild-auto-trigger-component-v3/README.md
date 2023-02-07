Things I learnt talking to Ringo for v3:

Ringo:

* separate VERY well CBuild stuff from non-CB stuff.
* dont use `if`s inside the Github/Bitbucket component, rather an Abstract Class with subclasses.

Ricc:

* make sure you can wrap generic variables in its execution value (maybe as a Hash of key/vals per component invokation?)
* the build stuff will be some kind of `build-dev` and `build-prod` stacks. Then the repos 1,2,3  will just invoke this code boilerplate
* create a python library installable with pip - but start with a stupid symlink, whch the build can download from the cloud.
* standardiZe like uild stuff with similar prefix, with version baked in, sth like: `rmp-v3-XXX`.

a
bvcdefghijklmnopqrs