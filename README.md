# Python SURBTC API Wrapper

SURBTC Python API Wrapper, Bitcoin Exchange for Chile and Colombia.
Tested on Python 3.5

[Go to SURBTC](www.surbtc.com)

## Dev Setup

Install the libs

    pip install -r requirements.txt

Rename .env.example > .env

## Installation

    pip install git+https://github.com/delta575/python-surbtc-api.git

## Usage

Setup (ApiKey/Secret requiered):

    from surbtc import SURBTC
    client = SURBTC(API_KEY, API_SECRET)

Market Pairs:

    btc-clp
    btc-cop

Open for everyone:
[www.surbtc.com](www.surbtc.com)

SURBTC API Doc:
[www.surbtc.com/docs/api](www.surbtc.com/docs/api)

## Licence

The MIT License (MIT)

Copyright (c) 2016 Felipe Aránguiz | Sebastián Aránguiz

See [LICENSE](LICENSE)

## Based on

[scottjbarr/bitfinex](https://github.com/scottjbarr/bitfinex)
