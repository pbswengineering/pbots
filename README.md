<a href="https://www.bernardi.cloud/">
    <img src=".readme-files/pbots-logo-72.png" alt="PBOTS logo" title="PBOTS" align="right" height="72" />
</a>

# PBOTS
> A collection of scrapers for institutional bulletin boards!

[![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/github/license/bernarpa/pbots.svg)](https://opensource.org/licenses/AGPL-3.0)
[![GitHub issues](https://img.shields.io/github/issues/bernarpa/pbots.svg)](https://github.com/bernarpa/pbots/issues)

## Table of contents

- [What is PBOTS](#what-is-pbots)
- [Usage](#usage)
- [Setup](#setup)
    - [Configuration file](#configuration-file)
    - [Mailing list subscribers](#mailing-list-subscribers)
    - [Cron scheduling](#cron-scheduling)
- [License](#license)

## What is PBOTS

PBOTS is a collection of web scrapers and a mailing system to notify subscribers
about various institutional bulletin boards updates. Each bulletin board is
assumed to contain a series of publications, possibly with one or more
attachments.

In the PBOTS model a publication is described by the following fields, which
may or may not be provided by each bulletin board:

  * URL
  * Number
  * Publisher
  * Publication type
  * Subject
  * Publication start date
  * Publication end date

The attachments, instead, are described by the following fields:

  * URL
  * Name

So far, PBOTS provides scrapers for the following bulletin boards:

  * Municipality of Acquasparta
  * Municipality of Montecastrilli, general series
  * Municipality of Montecastrilli, weddings series
  * Regione Umbria, general series
  * Regione Umbria, announcements series
  * Regione Umbria, information and communication series
  * I. C. "A. De Filis", Terni

## Usage

PBOTS is a command line application. The general usage pattern is as follows:

```
$ ./run.sh BULLETIN_BOARD_ID
```

To retrieve the list of available bulletin boards and their numerical
identifiers execute `run.sh` without arguments:

```
$ ./run.sh
```

## Setup

### Configuration file

Before running PBOTS you will need to create a `settings.py` file in the root
directory of the project. You should create it by copying `settings.py-sample`
and modifying its content as per your needs.

### Mailing list subscribers

PBOTS creates a SQLite3 database file named `pbots.db` in the project root
directory, if it doesn't already exist. Publications, attachments and
mailing list members are stored in this database.

The person identified by the parameters `DEFAULT_SUBSCRIBER_NAME` and 
`DEFAULT_SUBSCRIBER_EMAIL` from `settings.py` is automatically subscribed
to the mailing lists of all supported bulleting boards. To subscribe further
people you will need to add the following information to the
database table `pbots_mailinglistmember`:

  * Name
  * Email
  * Bulletin board ID

To retrieve the list of bulletin board identifiers you may refer to the
`pbots_source` table or execute `run.sh` without arguments.

### Cron scheduling

You might want to add some rows to your crontab to execute the PBOTS 
scrapers periodically. For example:

```
# Albo Pretorio del Comune di Acquasparta
0 16 * * * /home/rnd/github/pbots/run.sh 1
# Albo Pretorio del Comune di Montecastrilli
0 10 * * * /home/rnd/github/pbots/run.sh 2
# Bollettino della Regione Umbria, serie generale
0 12 * * * /home/rnd/github/pbots/run.sh 3
# Bollettino della Regione Umbria, serie avvisi e concorsi
15 12 * * * /home/rnd/github/pbots/run.sh 4
# Bollettino della Regione Umbria, serie informazioni e comunicazione
30 12 * * * /home/rnd/github/pbots/run.sh 5
# Albo Pretorio dell'I. C. "A. De Filis", Terni
30 16 * * * /home/rnd/github/pbots/run.sh 6
# Matrimoni del comune di Montecastrilli
30 10 * * * /home/rnd/github/pbots/run.sh 7
# USR Umbria
25 * * * * /home/rnd/github/pbots/run.sh 8
# UST Terni
35 * * * * /home/rnd/github/pbots/run.sh 9
```

## License

PBOTS is licensed under the terms of the GNU Affero General Public License version 3.

