# aiomassresolver
Uvloop &amp; aiodns ultra fast dns record resolver

Noticed there was not a use of aiodns out there, so I give you `aioMassResolver` - powered by uvloop, and capable of getting tens of thousands of DNS records in seconds:

<pre>
$ ./aiomassresolver.py -h
usage: Uvloop & AIODns Powered Resolver. Resolve thousands of domains in seconds.
example usage: $ python3 ./aioresolver.py --list domains.list --qtype 'A' 
       [-h] [-o OUTPUT] [-w NUM_WORKERS] [-l LIST_FILE] [-d SINGLE_QUERY]
       [-q {A,AAAA,CNAME,NS,MX,SOA,TXT,PTR}] [-W WILDCARD]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --out OUTPUT
  -w NUM_WORKERS, --workers NUM_WORKERS
                        Number of async workers to use.Increase this for
                        longer lists. Default: 1000
  -l LIST_FILE, --list LIST_FILE
                        List of ips/domains to resolve.
  -d SINGLE_QUERY, --domain SINGLE_QUERY
                        Resolve a single domain.
  -q {A,AAAA,CNAME,NS,MX,SOA,TXT,PTR}, --qtype {A,AAAA,CNAME,NS,MX,SOA,TXT,PTR}
                        DNS Query type to perform.
  -W WILDCARD, --wildcard_A WILDCARD
                        Run a wildcard_A query against a single domain.
                        Example: ./aiomassresolver.py -W taobao.com
</pre>


## Testing:

Resolve 10001 MX records in two seconds:


    $ ./aioresolver.py --list random_domains.list --qtype 'MX' --workers 10000
    ----- trunicated ------
    {'domain': 'ocs1.org', 'type': 'MX', 'data': ['alt1.aspmx.l.google.com', 'aspmx3.googlemail.com', 'aspmx.l.google.com',     'alt2.aspmx.l.google.com', 'aspmx2.googlemail.com']}
    {'domain': 'boccacciopinturas.com', 'type': 'MX', 'data': ['boccacciopinturas.com']}
    {'domain': 'boccacciopinturas.com', 'type': 'MX', 'data': ['boccacciopinturas.com']}
    {'domain': 'medinol.co.za', 'type': 'MX', 'data': ['mail.medinol.co.za']}
    {'domain': 'medinol.co.za', 'type': 'MX', 'data': ['mail.medinol.co.za']}
    {'domain': 'raelsalley.com', 'type': 'MX', 'data': ['mail.raelsalley.com']}
    {'domain': 'raelsalley.com', 'type': 'MX', 'data': ['mail.raelsalley.com']}
    {'domain': 'kuzeko.com', 'type': 'MX', 'data': ['aspmx.l.google.com']}
    {'domain': 'kuzeko.com', 'type': 'MX', 'data': ['aspmx.l.google.com']}
    {'domain': 'rik.ne.jp', 'type': 'MX', 'data': ['cure.southernx.ne.jp']}
    {'domain': 'rik.ne.jp', 'type': 'MX', 'data': ['cure.southernx.ne.jp']}
    {'domain': 'songdofish.com', 'type': 'MX', 'data': ['mail.songdofish.com']}
    {'domain': 'songdofish.com', 'type': 'MX', 'data': ['mail.songdofish.com']}
    {'domain': 'abgexpress.com', 'type': 'MX', 'data': ['mxa136v.chinaemail.cn', 'mx136v.chinaemail.cn']}
    {'domain': 'abgexpress.com', 'type': 'MX', 'data': ['mxa136v.chinaemail.cn', 'mx136v.chinaemail.cn']}
    --------------------------------------------------------------------------
    Finished! Process time: 2.015133043


Same thing but get A records:

    $ ./aioresolver.py -l random_domains.list -q 'A' -w 10000
    ----- trunicated -----
    {'domain': 'ironsolutions.com', 'type': 'A', 'data': ['192.238.15.32']}
    {'domain': 'aze.bz', 'type': 'A', 'data': ['202.172.26.48']}
    {'domain': 'usp.edu', 'type': 'A', 'data': ['204.109.15.165', '204.109.14.165']}
    {'domain': 'fanswedding.com', 'type': 'A', 'data': ['192.185.20.88']}
    {'domain': 'mobileemailvodafone.net', 'type': 'A', 'data': ['72.52.179.175']}
    {'domain': 'ibranch.in', 'type': 'A', 'data': ['70.34.40.84']}
    {'domain': 'tandemtransit.com', 'type': 'A', 'data': ['204.11.56.48']}
    {'domain': 'linuxtoy.org', 'type': 'A', 'data': ['139.162.113.238']}
    {'domain': 'hasseman.net', 'type': 'A', 'data': ['213.212.61.212']}
    {'domain': 'eurovision.net', 'type': 'A', 'data': ['193.43.93.43']}
    {'domain': 'kag.org', 'type': 'A', 'data': ['52.207.240.136']}
    {'domain': 'illuminationgallery.com', 'type': 'A', 'data': ['173.239.23.228']}
    {'domain': 'firstones.net', 'type': 'A', 'data': ['216.92.45.155']}
    {'domain': 'teknotel.net', 'type': 'A', 'data': ['77.92.99.131']}
    {'domain': 'bitcoin.it', 'type': 'A', 'data': ['104.25.120.33', '104.25.121.33']}
    {'domain': 'bestcostaricadmc.com', 'type': 'A', 'data': ['209.190.24.229']}
    {'domain': 'amarkalkoul.com', 'type': 'A', 'data': ['213.186.33.4']}
    {'domain': 'adgleathers.com', 'type': 'A', 'data': ['174.127.119.143']}
    {'domain': 'nacktcam.info', 'type': 'A', 'data': ['134.119.45.78']}
    --------------------------------------------------------------------------
    Finished! Process time: 1.837687219


As you can see, using aiodns with uvloop, we can resolve tons of domains extreemely quickly. I've truncated the output because it's too long for this readme. Try it yourself:

    $ git clone https://github.com/darkerego/aiomassresolver
    $ cd aiomassresolver
    $ pip3 install -r requirements.txt
    $ ./aioresolver.py -l random_domains.list -q 'A' -w 10000
    
    
Program also has a function for resolving wildcard A records
