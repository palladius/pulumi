

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
