# Python SURBTC API Wrapper

SURBTC Python API Wrapper, Bitcoin Exchange for Chile and Colombia.
Tested on Python 3.5

[Go to SURBTC](https://www.surbtc.com)

## Dev Setup

Install the libs

    pip install -r requirements.txt

Rename .env.example > .env

## Installation

    pip install git+https://github.com/delta575/python-surbtc-api.git

## Usage

### Setup Public:

    from surbtc import SURBTC
    client = SURBTC.Public()

### Setup Auth (ApiKey/Secret requiered, Test is optional (default: False)):

    from surbtc import SURBTC
    client = SURBTC.Auth(API_KEY, API_SECRET, TEST)

## Market Pairs:

    btc-clp
    btc-cop

Open for everyone:
[www.surbtc.com](https://www.surbtc.com)

SURBTC API Doc:
[www.surbtc.com/docs/api](https://www.surbtc.com/docs/api)

## Licence

The MIT License (MIT)

Copyright (c) 2016 Felipe Aránguiz | Sebastián Aránguiz

See [LICENSE](LICENSE)

## Based on

[scottjbarr/bitfinex](https://github.com/scottjbarr/bitfinex)
