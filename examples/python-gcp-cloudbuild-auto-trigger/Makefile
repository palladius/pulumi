

install-deps:
	venv/bin/pip install -r requirements.txt

# broken, its an OUTPUT not a config. Silly me
see-on-web:
	echo Open this with browser:
	pulumi stack output pulumi-readme-url
	open `pulumi stack output pulumi-readme-url`

curl-nginx:
	open http://`pulumi stack output ingress_ip`/


render-readme-for-that-snob-of-cstanger:
	pulumi stack output readme > README-rendered-cstanger.md

# In case you have different backends.. I'm now moving between GCS and Official Pulumi
login-with-default-backend:
	pulumi login https://api.pulumi.com/

# In case you have different backends.. Good to show current state :)
whoami:
	 pulumi whoami -v 2>/dev/null

up:
	pulumi up --yes --message 'Issued from Makefile (💄 make up)'

# thanks SO :)
tag-example:
	git tag 1.0 -a
	git push origin --tag

# MAazing great idea :)
#	gcp-annotate palladius-devrel-tests 'Used by Pulumi on '
install-python-and-virtualenv:
	sudo apt-get install python-is-python3
	sudo apt-get install -y python3-pip
	sudo apt-get install -y python3-venv
	python3 -m venv venv
	# run this every time you add a new dependency..
	venv/bin/pip install -r requirements.txt
