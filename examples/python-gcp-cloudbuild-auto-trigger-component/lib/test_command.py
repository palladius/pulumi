from pulumi_command import local
import pulumi 

# https://www.pulumi.com/registry/packages/command/

def add_some_random_commands():
    random = local.Command("random",
        create="openssl rand -hex 16"
    )
    randomness = local.Command("randomness",
        create="openssl rand -hex 16"
    )
    uname = local.Command("uname",
        create="uname"
    )
    hostname = local.Command("hostname",
        create="hostname"
    )

    # just me playing around for when I need this :)
    pulumi.export("ricc_command_random", random.stdout)
    pulumi.export("ricc_command_randomness", randomness.stdout)
    pulumi.export("ricc_command_uname", uname.stdout)
    pulumi.export("ricc_command_hostname", hostname.stdout)
    

