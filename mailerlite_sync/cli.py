import csv
import os
import time
import datetime

import click
import mailerlite as MailerLite


FIELD_MAP = {
    "name": "First Name",
    "last_name": "Last Name",
    "engagement_segment": "Engagement Segment",
    "congressional_district": "Congressional District",
    "chapter_change_date": "Group Change Date",
    "state_assembly_district": "State Assembly District",
    "state_senate_district": "State District Upper House",
    "intro_call_date": "Date Of Intro Call",
    "joined_ccl": "Date Added to Database",
    "z_i_p": "Mailing Zip/Postal Code",
    "notes": "Notes/Comments",
    "state": "Mailing State/Province",
    "city": "Mailing City"
}

DROP = ["Long Term Unengaged"]

DATES = [
    "Date Of Intro Call",
    "Date Added to Database",
    "Group Change Date"
]

NOT_FOUND = {'message': 'Resource not found.'}

missing_emails = []

def normalize_field(name, value):
    if value and name in DATES:
        return datetime.datetime.fromisoformat(value).date().strftime("%Y-%m-%d")
    else:
        return value

def find_record(records, email):
    for rec in records:
        if rec['email'] == email:
            return rec

        
def extra_emails(records, roster):
    extras = []
    for rec in records:
        print(rec)
        for email in roster:
            if rec['email'] == email:
                break
        else:
            extras.append(rec['email'])
    return extras


def collect_fields(row):
    fields = {}
    for k, v in FIELD_MAP.items():
        roster_field = row[v]
        fields[k] = roster_field
    return fields


def needs_update(ml_rec, row):
    # If the user unsubscribed, we can't update them
    if ml_rec['status'] in ('unsubscribed', 'bounced'):
        return        
    
    email = ml_rec['email']
    fields = {}
    for k, v in FIELD_MAP.items():
        ml_field = ml_rec['fields'][k]
        roster_field = normalize_field(v, row[v])
        if roster_field and ml_field != roster_field:
            click.echo(f'Updating {email} {k}: {ml_field} => {roster_field}')
            click.echo(ml_rec)
            fields[k] = roster_field
    return fields

def add_to_whole_roster(client, subid):
    resp = client.groups.list(filter={'name': 'Whole Roster'})
    data = resp['data'][0]
    
    client.subscribers.assign_subscriber_to_group(subid, int(data['id']))

def collect_ml(client):
    resp = client.subscribers.list(limit=1000)
    return resp['data']


@click.group()
@click.version_option()
def cli():
    "Sync CCL Roster to Mailerlite"


@cli.command(name="sync")
@click.argument(
    "roster"
)
@click.option(
    "--token",
    default=lambda: os.environ.get("ML_TOKEN", ""),
    help="Token for mailerlite",
)
def first_command(roster, token):
    "Command description goes here"
    client = MailerLite.Client({
        'api_key': token
    })

    records = collect_ml(client)
    roster_emails = []
    with open(roster) as f:
        ros = csv.DictReader(f)
        for row in ros:
            email = row['Email']
            if email:
                # click.echo(row)
                # click.echo(email)
                # This ensures that we don't add in new long term unengaged
                roster_emails.append(email)
                response = find_record(records, email)
                if not response or not response.get('fields'):
                    if row['Engagement Segment'] not in DROP:
                        click.echo(f"Missing record for {email}")
                        missing_emails.append(email)
                    continue

                fields = needs_update(response, row)
                if fields:
                    response = client.subscribers.update(email, fields=fields)
                    click.echo(response)
                else:
                    click.echo(f"{email} unchanged")
    extras = extra_emails(records, roster_emails)
    click.echo("Extra emails (" + str(len(extras)) + "):\n\t" + "\n\t".join(sorted(extras)))
    click.echo('Missing emails:\n\t' + "\n\t".join(sorted(missing_emails)))
    
    with open(roster) as f:
        ros = csv.DictReader(f)
        for row in ros:
            email = row['Email']
            if email in missing_emails:
                fields = collect_fields(row)
                try:
                    click.echo(f"Adding email {email}")
                    response = client.subscribers.create(email, fields=fields)
                    click.echo(response)
                    subid = response['data']['id']
                    add_to_whole_roster(client, int(subid))
                    click.echo(f"Added to roster subscription group")
                except Exception as e:
                    print(e)
