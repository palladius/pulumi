SHELL := /bin/bash
PROJECT_NAME = $(shell cat Pulumi.yaml  | egrep '^name:' | cut -f 2 -d' ' )

info:
	pulumi whoami -v
	pulumi stack ls
	echo And now from Riccardo:
	echo "PROJECT_NAME: $(PROJECT_NAME)"
	pulumi config

whoami:
	pulumi whoami -v

login-gcs:
	echo 'Logging in to Google Cloud Storage'
	direnv allow .
	pulumi login "$(GOOGLE_BUCKET)"/state/$(PROJECT_NAME)/

add-secret:
	pulumi config set secret-password    --secret 'Ungueass4ble'
	pulumi config set clear-password --plaintext 'MoreGueass4ble'

login-default:
	echo reverting back to Pulumi default place.
	pulumi login https://app.pulumi.com/

up:
	direnv allow .
	pulumi up --yes
