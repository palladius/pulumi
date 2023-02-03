
from thsi docs: https://www.pulumi.com/templates/static-website/gcp/ I got here :)

Deploy with pulumi! 

1. `curl -fsSL https://get.pulumi.com | sh`
1. `mkdir static-website-gcp-python && cd static-website-gcp-python`
1. `pulumi new https://github.com/pulumi/templates/tree/master/static-website-gcp-python -s palladius/static-website-gcp-python/dev` =>  I dont know how, but this ulls data from the cloud with the config I gave on UI. So awesome! :)
1. `pulumi up`