# Tiamat with Pulumi

## Overview

This is a demo application for using Pulumi on Google Cloud.

![image](Tiamat_dragon_in_sci-fi_context.png)

## V1 


* [xiang] Simple app
* [xiang] Load Balancer + Bucket + SPA static in JS on bucket
* [ricc] Cloud Build to build everything


## V2

As v1, but:

* Cloud Build only builds the app (Xiang SB yaml steps 1-4).
* We delegate the Cloud Deploy the deployment part (Xiang step 5 alone)
  
Cloud DEploy coyuld have 3 steps:

* DEV: always push (v1)
* STAG: triggered if main_test.py passes (UT)
* PROD: triggered manually (or maybe with skaffold + skaffold verification to simulate integration test)




# Resources

Deck on Pulumi + Cloud Build: https://docs.google.com/presentation/d/1LgQLOznGLnmUrJg24X47dZsSAqmtEgrzSpfeaaqygGM/edit#slide=id.g204fcaa0b74_0_34