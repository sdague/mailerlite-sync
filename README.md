# mailerlite-sync

[![PyPI](https://img.shields.io/pypi/v/mailerlite-sync.svg)](https://pypi.org/project/mailerlite-sync/)
[![Changelog](https://img.shields.io/github/v/release/sdague/mailerlite-sync?include_prereleases&label=changelog)](https://github.com/sdague/mailerlite-sync/releases)
[![Tests](https://github.com/sdague/mailerlite-sync/actions/workflows/test.yml/badge.svg)](https://github.com/sdague/mailerlite-sync/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sdague/mailerlite-sync/blob/master/LICENSE)

Sync CCL Roster to Mailerlite

## Installation

Install this tool using `pip`:
```bash
pip install mailerlite-sync
```
## Usage

For help, run:
```bash
mailerlite-sync --help
```
You can also use:
```bash
python -m mailerlite_sync --help
```
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
