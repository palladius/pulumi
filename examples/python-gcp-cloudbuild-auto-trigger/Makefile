

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
