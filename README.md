<a href="https://www.bernardi.cloud/">
    <img src=".readme-files/pbots-logo-72.png" alt="PBOTS logo" title="PBOTS" align="right" height="72" />
</a>

# PBOTS
> A collection of scrapers for online bulletin boards!

[![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/github/license/bernarpa/pbots.svg)](https://opensource.org/licenses/AGPL-3.0)
[![GitHub issues](https://img.shields.io/github/issues/bernarpa/pbots.svg)](https://github.com/bernarpa/pbots/issues)

## Table of content

- [What is PBOTS](#what-is-pbots)
- [Setup](#setup)
- [License](#license)

## What is PBOTS

PBOTS is a collection of web scrapers and a mailing system to notify updates of online bulletin boards.

So far, PBOTS provides scrapers for the following bulletin boards:

  * Municipality of Acquasparta
  * Municipality of Montecastrilli, general series
  * Municipality of Montecastrilli, weddings series
  * Regione Umbria, general series
  * Regione Umbria, announcements series
  * Regione Umbria, information and communication series
  * I. C. "A. De Filis", Terni
  
### Setup

You might want to add some rows to your crontab to run the PBOTS scrapers periodically. For example:

```
# Albo Pretorio del Comune di Acquasparta
0 16 * * * /home/rnd/anaconda3/bin/python /home/rnd/github/pbots/run.sh 1
# Albo Pretorio del Comune di Montecastrilli
0 10 * * * /home/rnd/anaconda3/bin/python /home/rnd/github/pbots/run.sh 2
# Bollettino della Regione Umbria, serie generale
0 12 * * * /home/rnd/anaconda3/bin/python /home/rnd/github/pbots/run.sh 3
# Bollettino della Regione Umbria, serie avvisi e concorsi
15 12 * * * /home/rnd/anaconda3/bin/python /home/rnd/github/pbots/run.sh 4
# Bollettino della Regione Umbria, serie informazioni e comunicazione
30 12 * * * /home/rnd/anaconda3/bin/python /home/rnd/github/pbots/run.sh 5
# Albo Pretorio dell'I. C. "A. De Filis", Terni
30 16 * * * /home/rnd/anaconda3/bin/python /home/rnd/github/pbots/run.sh 6
# Matrimoni del comune di Montecastrilli
30 10 * * * /home/rnd/anaconda3/bin/python /home/rnd/github/pbots/run.sh 7
```

# License

PBOTS is licensed under the terms of the GNU Affero General Public License version 3.

