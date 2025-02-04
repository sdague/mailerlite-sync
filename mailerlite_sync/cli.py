import csv
import os
import time

import click
import mailerlite as MailerLite


FIELD_MAP = {
    "name": "First Name",
    "last_name": "Last Name",
    "engagement_segment": "Engagement Segment",
    "congressional_district": "Congressional District",
    "intro_call_date": "Date Of Intro Call",
    "notes": "Notes/Comments",
    "state": "Mailing State/Province",
    "city": "Mailing City"
}

NOT_FOUND = {'message': 'Resource not found.'}

missing_emails = []

def find_record(records, email):
    for rec in records:
        if rec['email'] == email:
            return rec

        
def extra_emails(records, roster):
    extras = []
    for rec in records:
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
        roster_field = row[v]
        if roster_field and ml_field != roster_field:
            click.echo(f'Updating {email} {k}: {ml_field} => {roster_field}')
            click.echo(ml_rec)
            fields[k] = roster_field
    return fields


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
                roster_emails.append(email)
                response = find_record(records, email)

                if not response or not response.get('fields'):
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
    click.echo("Extra emails")
    click.echo(extras)
    click.echo('Missing emails')
    click.echo(missing_emails)
    
    with open(roster) as f:
        ros = csv.DictReader(f)
        for row in ros:
            email = row['Email']
            if email in missing_emails:
                fields = collect_fields(row)
                try:
                    click.echo(f"Adding email {email}")
                    response = client.subscribers.create(email, fields=fields)
                except Exception as e:
                    print(e)
