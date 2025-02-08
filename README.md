# mailerlite-sync

[![PyPI](https://img.shields.io/pypi/v/mailerlite-sync.svg)](https://pypi.org/project/mailerlite-sync/)
[![Changelog](https://img.shields.io/github/v/release/sdague/mailerlite-sync?include_prereleases&label=changelog)](https://github.com/sdague/mailerlite-sync/releases)
[![Tests](https://github.com/sdague/mailerlite-sync/actions/workflows/test.yml/badge.svg)](https://github.com/sdague/mailerlite-sync/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sdague/mailerlite-sync/blob/master/LICENSE)

Sync CCL Roster to Mailerlite.

This tool is useful for me to sync the Citizens Climate Lobby Chapter
roster into a mailerlite mailing list. Which includes a bunch of
custom fields syncing across to it.

It's provided without much support. It works for me, and maybe there
are others where this is helpful. You'll need to have the level of
expertise to install and run python code.

## Installation

Install this tool using `pip`:
```bash
git clone https://github.com/sdague/mailerlite-sync
cd mailerlite-sync
pip install -e . 
```
## Usage

### Get Mailerlite API Key

You'll need to get a mailerlite API.

Then you'll need to:

```bash
export ML_TOKEN="YOUR TOKEN.................."
```

### Sync

Download the roster to your chapter as a csv file. 

```bash
mailerlite-sync sync chapter-roster.csv
```

This will go through the csv file and ensure that every entry in it is
added to your roster in mailer lite.

NOTE: there are a bunch of custom fields I've defined so that I can
segment by district or engagement segment. This might blow up if those
fields aren't set. 

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd mailerlite-sync
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
