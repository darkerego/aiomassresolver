# aiomassresolver
Uvloop &amp; aiodns ultra fast dns record resolver

Noticed there was not a use of aiodns out there, so I give you `aioMassResolver` - powered by uvloop, and capable of getting tens of thousands of DNS records in seconds:

<pre>

usage: aioMassResolver.py [-h] [--demo] [-o OUTPUT] [-i] [-w NUM_WORKERS]
                       [-l LIST_FILE] [-d SINGLE_QUERY] [-q QTYPE]

optional arguments:
  -h, --help            show this help message and exit
  --demo                Demo mode. Show me what you got.
  -o OUTPUT, --out OUTPUT
  -i, --json
  -w NUM_WORKERS, --workers NUM_WORKERS
                        Number of async workers
  -l LIST_FILE, --list LIST_FILE
                        list of ips/domains to resolve
  -d SINGLE_QUERY, --domain SINGLE_QUERY
                        Resolve a single domain/ip.
  -q QTYPE, --qtype QTYPE
                        DNS Query type to perform. Valid qtypes are:A, AAAA,
                        CNAME, NS, MX, SOA, TXT, and PTR
