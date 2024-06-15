import pulumi
import pulumi_cloudflare as cloudflare

config = pulumi.Config()

account_id = config.require('accountId')
zones = config.require_object("zones")

def create_dns_record(zone_id, entry):
    cf_record = cloudflare.Record(f"{entry['type']}-{entry['name'].replace('.', '-')}-record",
                                  zone_id=zone_id,
                                  name=entry['name'],
                                  type=entry['type'],
                                  value=entry['value'],
                                  priority=entry.get('priority'),
                                  ttl=60,
                                  proxied=False)
    pulumi.export(f"record_id_{entry['name'].replace('.', '-')}", cf_record.id)

for zone in zones:
    zone_name = zone['name']
    zone_id = cloudflare.get_zone_output(name=zone_name).id

    records = zone.get('records', [])

    for entry in records.get('general', []):
        create_dns_record(zone_id, entry)

    for entry in records.get('mail', []):
        create_dns_record(zone_id, entry)
