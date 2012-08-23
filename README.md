# Dynamic Chef Solo (DCS)

Dynamic Chef Solo provides an easier to produce the JSON attributes used by Chef Solo.

DSC sets up a series of JSON-like files that are combined at build time to a JSON file suitable for use by Chef Solo.  By building in concepts like environment, datacenter, purpose, and individual node attributes we can produce a richer and easier to use configuration system.

## How it works

DCS combines attributes from multiple JSON files into a single JSON file which can
be used by Chef Solo.

Attributes are combined (merged) in the following order:

1. global
2. product
3. environment
4. region
5. datacenter
6. purpose

## Running it

    bin/dcs-builder.py <path/to/your/repo> <path/to/output>

## Example

For a machine with name `ord1-maas-prod-api0`, with the following files:

* environments/prod.dyp:

`
    {
      "environment": "production",
      "auth_servers": ["https://identity.api.rackspacecloud.com/"],
      "run_list": ["role[ele-base]"]
    }
`

* regions/ord1.dyp:

`
    {
      "region": "ord1",
    }
`

* purpose/api.dyp:

`
    {
      "mail_relay": "smtp.sendgrid.com",
      "run_list": ["recipe[ele-base::api]"]
    }
`

* hosts/ord1-maas-prod-api0.dyp:

`
    {
      "internal_ip": "10.200.1.20",
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
