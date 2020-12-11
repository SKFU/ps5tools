[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

# PS5 Tools

Usage: main.py [-h] [-v] {analyze,dns} ..

positional arguments:
  {analyze,dns}  Choose one of these options
    analyze      Analyze PS5 file
    dns          Redirect PS5 traffic via DNS

optional arguments:
  -h, --help     show this help message and exit
  -v             Verbose mode


# Analyze Mode

usage: main.py analyze [-h] [-e] file

positional arguments:
  file        PS5 Input File

optional arguments:
  -h, --help  show this help message and exit
  -e          Extract given file if possible


# DNS Mode

usage: main.py dns [-h] domain a_record

positional arguments:
  domain      Domain to redirect
  a_record    A record to point to

optional arguments:
  -h, --help  show this help message and exit
