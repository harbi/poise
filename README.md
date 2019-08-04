# Poise

> Poise, a CLI for retrieving quotes on Goodreads.

<p align="center"><img src="/img/demo.gif?raw=true"/></p>

## Installation

```bash
pip install poise-cli
```

## Usage

> You can use the `--help` option to get more details about the commands and their options.

```bash
poise -k <keyword> [options]
```

Options

```
-c, --count                  Number of quotes to retrieve     [integer] [default: 1]
-l, --language               Quotes preferred language        [string]  [default: en]
-f, --format [json|xml|csv]  File format of the output        [string]  [default: json]
```

## License

This project is under the MIT license.
