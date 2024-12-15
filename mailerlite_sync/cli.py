import csv
import os
import time

import click
import mailerlite as MailerLite


FIELD_MAP = {
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

    with open(roster) as f:
        roster = csv.DictReader(f)
        for row in roster:
            email = row['Email']
            if email:
                # click.echo(row)
                # click.echo(email)
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
    click.echo('Missing emails')
    click.echo(missing_emails)
