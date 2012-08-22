# Dynamic Chef Solo (DCS)

Dynamic Chef Solo provides an easier to produce the JSON attributes used by Chef Solo.

DSC sets up a series of JSON-like files that are combined at build time to a JSON file suitable for use by Chef Solo.  By building in concepts like environment, datacenter, purpose, and individual node attributes we can produce a richer and easier to use configuration system.

## Running it

    bin/dcs-builder path/to/your/repo path/to/output

## Example

DCS combines the environment, datacenter, and individual node information into a single JSON file.  For a machine like `ord1-maas-prod-api0`, with the following files:

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
