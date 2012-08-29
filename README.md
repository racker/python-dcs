# Dynamic Chef Solo (DCS)

Dynamic Chef Solo provides an easier to produce the JSON attributes used by Chef Solo.

DSC sets up a series of JSON-like files that are combined at build time to a JSON file suitable for use by Chef Solo.  By building in concepts like environment, datacenter, purpose, and individual node attributes we can produce a richer and easier to use configuration system.

## Installation

`sudo pip install dcs`

## How it works

DCS combines attributes from multiple JSON files into a single JSON file which
can be used by Chef Solo.

Attributes are combined (merged) in the following order:

1. global
2. product
3. environment
4. region
5. data center
6. purpose

Attributes are inferred from the node name which means the name needs to be in
the following format:

`(?P<datacenter>\w+)(?P<datacenter_number>\d+)-(?P<product>\w+)-(?P<environment>\w+)-(?P<purpose>\w+)(?P<purpose_number>\d+)(\..*){0,1}$`

Example attribute values using the name `dfw1-maas-stage-api0` with a node file
stored in `nodes/dfw1-maas-stage-api0.k1k.me.dyp`:

* region: `dfw` (file: `region/dfw.dyp`)
* datacenter: `dfw1` (file: `datacenter/dfw1.dyp`)
* product: `maas` (file: `product/maas.dyp`)
* environment: `stage` (file: `environment/stage.dyp`)
* purpose: `api` (file: `purpose/api.dyp`)

## Running it

`bin/dcs-builder.py [--validate] --source=<path to the directory with attributes files> --output=<output directory>`

## Example

For a machine with name `ord1-maas-prod-api0`, with the following files:

* environment/prod.dyp:

`
    {
      "environment": "production",
      "auth_servers": ["https://identity.api.rackspacecloud.com/"],
      "run_list": ["role[ele-base]"]
    }
`

* region/ord1.dyp:

`
    {
      "region": "ord1"
    }
`

* purpose/api.dyp:

`
    {
      "mail_relay": "smtp.sendgrid.com",
      "run_list": ["recipe[ele-base::api]"]
    }
`

* nodes/ord1-maas-prod-api0.k1k.me.dyp:

`
    {
      "internal_ip": "10.200.1.20"
    }
`


These sources would be compiled into a single `ord1-maas-prod-api0.json` suitable for use by `chef-solo`:

    {
      "internal_ip": "10.200.1.20",
      "mail_relay": "smtp.sendgrid.com",
      "region": "ord1",
      "environment": "production",
      "auth_servers": ["https://identity.api.rackspacecloud.com/"],
      "run_list": ["role[ele-base]",
                   "recipe[ele-base::api]"]
    }

Another example can be found [here](https://github.com/racker/python-dcs/tree/master/examples/example-1).
