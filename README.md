# Async Up Bank API

This project is a async fork of jcwillox/up-bank-api. I've attempted to keep most things the same but I have changed a fair bit.

If there's any issues please let me know.

[![Project version](https://img.shields.io/pypi/v/up-bank-api?style=flat-square)](https://pypi.python.org/pypi/async-up-bank-api)
[![Supported python versions](https://img.shields.io/pypi/pyversions/up-bank-api?style=flat-square)](https://pypi.python.org/pypi/async-up-bank-api)
[![License](https://img.shields.io/github/license/jcwillox/up-bank-api?style=flat-square)](https://github.com/unchartedshark/async-up-bank-api/blob/master/LICENSE)
![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/unchartedshark/async-up-bank-api?style=flat-square)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is an unofficial python wrapper (client) for the australian bank Up's API.

- 🕶️ [The Up Website](https://up.com.au)
- 📖 [Up API Documentation](https://developer.up.com.au)
- [Up API on Github](https://github.com/up-banking/api)

## Installation

```shell
$ pip install async-up-bank-api
```


## Usage

The code is fully typed and documented so I'd recommend just having a look at the code, or letting syntax completion take the wheel.

To use this library you will need a personal access token which can be retrieved from https://developer.up.com.au. When using this library you can either provide the token directly or use the environment variable `UP_TOKEN`.
