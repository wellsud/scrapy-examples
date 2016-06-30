# Basic Tweets Scraper

## Overview

In this repository I will store some examples of basic tweets scrapers. The first is a basic live tweets scraper that makes a search by a specific term with the number of results defined by user.

## Requirements

* Python 2.7
* Scrapy == 1.1.0

## Install

```
 $ git clone https://github.com/wellsud/scrapy-examples.git
```
## Usage

Suppose you want to extract the last 200 live tweets about the term "brexit"

```
$ cd twitter
```


```
$ scrapy crawl live -a term=brexit -a total_results=200
```

If you want to store ina csv file just type:


```
$ scrapy crawl live -a term=brexit -a total_results=200 -o filename.csv
```

## Todo

Include spyder for:

* **Live tweets** ✓
* Photos - *Pending*
* News - *Pending*
* Videos - *Pending*
* News - *Pending*