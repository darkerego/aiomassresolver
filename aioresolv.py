#!/usr/bin/env python
# encoding: utf-8
# AioMassResolver ~ uvloop & aiodns - resolve bulk dns queries extremely quickly
# xelectron@protonmail.com

"""
@author: darkerego
@time: 2019/5/16
"""
import random
import string
from typing import Dict, Any
import argparse
import aiodns
import asyncio
import ipaddress
import uvloop


class AsyncResolver(object):
    results: Dict[Any, Any]

    def __init__(self, num_workers=5, nameservers=['8.8.8.8', '8.8.4.4'], loop=None, qtype="A", debug=False):
        self.timeout = 0.1
        # self.loop = uvloop.new_event_loop()  # use uvloop
        # self.loop = asyncio.get_event_loop()
        self.loop = uvloop.new_event_loop()  # use uvloop
        asyncio.set_event_loop(self.loop)
        self.resolver = aiodns.DNSResolver(timeout=self.timeout, loop=self.loop)
        self.nameservers = nameservers
        self.resolver.nameservers = nameservers
        self.qtype = qtype
        self.debug = debug
        self.num_workers = num_workers
        self.results = {}

        """
        Functions for later implementation
        """

    def wildcard_A(self, domain):
        genrandstr = lambda i: ''.join(random.choices(string.ascii_lowercase + string.digits, k=i))
        tasks = [asyncio.ensure_future(self.query(genrandstr(20) + '.' + domain, 'A')) for _ in range(6)]
        reqs = asyncio.gather(*tasks)
        try:
            f = self.loop.run_until_complete(reqs)
            data = list(set(map(lambda x: x[0].host, f)))
            print('[*] Found wildcard dns record:{data}'.format(data=data))
            return data
        except:
            print('[*] Not Found wildcard dns record')
            return False

    def query_A(self, domain):
        """query DNS A records.
        ex: {'domain': 'www.google.com','type': 'A','data': [u'93.46.8.89']}}
        """
        f = self.query(domain, 'A')
        result = self.loop.run_until_complete(f)
        data = list(map(lambda x: x.host, result))
        item = {"domain": domain, "type": "A", "data": data}
        return item

    def query_AAAA(self, domain):
        """query DNS AAAA records.
        ex: {'domain': 'www.google.com','type': 'AAAA','data': [u'2404:6800:4005:809::200e']}}
        """
        f = self.query(domain, 'A')
        result = self.loop.run_until_complete(f)
        data = list(map(lambda x: x.host, result))
        item = {"domain": domain, "type": "AAAA", "data": data}
        return item

    def query_CNAME(self, domain):
        """query DNS CNAME records.
        ex: {'domain': 'www.baidu.com','type': 'CNAME','data': [u'www.a.shifen.com']}}
        """
        f = self.query(domain, 'CNAME')
        result = self.loop.run_until_complete(f)
        data = result.cname
        item = {"domain": domain, "type": "CNAME", "data": data}
        return item

    def query_MX(self, domain):
        """query DNS MX records.
        ex: {'domain':'google.com', 'type': 'MX', 'data': ['aspmx.l.google.com.',
                                                           'alt3.aspmx.l.google.com.',
                                                           'alt4.aspmx.l.google.com.',
                                                           'alt1.aspmx.l.google.com.',
                                                           'alt2.aspmx.l.google.com.']}}
        """
        f = self.query(domain, 'MX')
        result = self.loop.run_until_complete(f)
        data = list(map(lambda x: x.host, result))
        item = {"domain": domain, "type": "MX", "data": data}
        return item

    def query_NS(self, domain):
        """query DNS NS records.
        ex: {'domain': 'google.com','type':'NS','data': ['ns3.google.com.',
                                                        'ns1.google.com.',
                                                        'ns4.google.com.',
                                                        'ns2.google.com.']}}
        """
        f = self.query(domain, 'NS')
        result = self.loop.run_until_complete(f)
        data = list(map(lambda x: x.host, result))
        item = {"domain": domain, "type": "NS", "data": data}
        return item

    def query_SOA(self, domain):
        """query DNS SOA records.
        ex: {'domain': 'google.com', 'type': 'SOA', 'data': ['ns4.google.com.']}}
        """
        f = self.query(domain, 'SOA')
        result = self.loop.run_until_complete(f)
        data = result.nsname
        item = {"domain": domain, "type": "SOA", "data": data}
        return item

    def query_SRV(self, domain):
        """query DNS SRV records.,ex:
        {'domain','xmpp-server._tcp.jabber.org', 'type': 'SRV', 'data': ['hermes2v6.jabber.org','hermes2.jabber.org']}
        """
        f = self.query(domain, 'SRV')
        result = self.loop.run_until_complete(f)
        data = list(map(lambda x: x.host, result))
        item = {"domain": domain, "type": "SRV", "data": data}
        return item

    def query_TXT(self, domain):
        """query DNS TXT records, normally, it includes [SPF] information.
        ex: {'domain': 'yahoo.com', 'type': 'TXT', 'data': ['v=spf1 redirect=_spf.mail.yahoo.com']}}
        """
        f = self.query(domain, 'TXT')
        result = self.loop.run_until_complete(f)
        data = list(map(lambda x: x.text, result))
        item = {"domain": domain, "type": "TXT", "data": data}
        return item

    def query_NAPTR(self, domain):
        """query DNS NAPTR records, ex:
        {'domain': 'sip2sip.info', 'type': 'NAPTR', 'data': ['_sip._udp.sip2sip.info',
                                                            '_sip._tcp.sip2sip.info',
                                                            '_sips._tcp.sip2sip.info']}}
        """
        f = self.query(domain, 'NAPTR')
        result = self.loop.run_until_complete(f)
        data = list(map(lambda x: x.replacement, result))
        item = {"domain": domain, "type": "NAPTR", "data": data}
        return item

    def query_PTR(self, ip):
        """query DNS PTR records, ex:
        {'domain': 'google-public-dns-a.google.com', 'type': 'PTR', 'data': '8.8.8.8'}}
        """
        f = self.query(ipaddress.ip_address(ip).reverse_pointer, 'PTR')
        result = self.loop.run_until_complete(f)
        data = result.name
        item = {"domain": data, "type": "PTR", "data": [ip]}
        return item

    """async def _query(self, domain, qtype):
         self.domain = domain
         self.qtype = qtype
         # return await self.resolver.query(domain, type)
         if domain is not None:
            if qtype == 'wildcard_A':
                return self.wildcard_A(domain)
            elif qtype == 'A':
                return self.query_A(domain)
            elif qtype == 'AAAA':
                return self.query_AAAA(domain)
            elif qtype == 'CNAME':
                return self.query_CNAME(domain)
            elif qtype == 'MX':
                return self.query_MX(domain)
            elif qtype == 'NS':
                return self.query_NS(domain)
            elif qtype == "SOA":
                return self.query_SOA(domain)
            elif qtype == 'TXT':
                return self.query_TXT(domain)
            elif qtype == 'SRV':
                return self.query_SRV(domain)
            elif qtype == 'NAPTR':
                return self.query_NAPTR(domain)
            elif qtype == 'PTR':
                return self.query_PTR(domain)
            else:
                return 'Error: Invalid dns record qtype'"""

    async def query(self, domain, qtype):
        return await self.resolver.query(domain, qtype)

    def task_query(self, domains):

        tasks = []
        q = asyncio.Queue()

        for domain in domains:
            q.put_nowait(domain)

        for i in range(self.num_workers):
            tasks.append(self.do_work(q))

        self.loop.run_until_complete(asyncio.wait(tasks))
        return self.results

    async def do_work(self, work_queue):
        resolver = aiodns.DNSResolver(loop=self.loop, nameservers=self.nameservers, timeout=2, tries=1)
        # resolver = aiodns.DNSResolver(loop=loop)
        while not work_queue.empty():
            domain = await work_queue.get()
            qtype = self.qtype
            debug = self.debug
            try:
                if qtype == 'PTR':
                    res = await resolver.query(ipaddress.ip_address(domain).reverse_pointer, 'PTR')
                else:
                    res = await self.query(domain, self.qtype)

            except aiodns.error.DNSError as e:
                error_code: object = e.args[0]
                if self.debug:
                    print("[DEBUG]: error: " + str(e))
                if error_code == aiodns.error.ARES_ECONNREFUSED:
                    self.results[domain] = "CONNECTION_REFUSED"
                elif error_code == aiodns.error.ARES_ENODATA:
                    self.results[domain] = "NODATA"
                elif error_code == aiodns.error.ARES_ENOTFOUND:
                    self.results[domain] = "NXDOMAIN"
                elif error_code == aiodns.error.ARES_EREFUSED:
                    self.results[domain] = "REFUSED"
                elif error_code == aiodns.error.ARES_ESERVFAIL:
                    self.results[domain] = "SERVFAIL"
                elif error_code == aiodns.error.ARES_ETIMEOUT:
                    self.results[domain] = "TIMEOUT"
                else:
                    self.results[domain] = "UNKNOWN_STATUS"

            except Exception as e:
                print(str(domain + ' error: ' + str(e)))
                if debug:
                    print("[debug]: raw :" + str(e))
            else:
                self.results[domain] = res
                res = str(res)
                print(res)

            work_queue.task_done()


class Resolver:
    """
    Wrapper class for swarm resolver
    """
    def __init__(self, domains, qtype, output, json_output, num_workers=100):
        """

        :param domains: list of ips to query
        :param output: name of output file
        :param json_output: json output or not
        :param num_workers: number of async workers
        :return:
        """
        self.loop = uvloop.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.domains = domains
        self.num_workers = num_workers
        self.qtype = qtype
        self.output = output
        self.swarm = AsyncResolver(qtype=qtype, num_workers=num_workers, loop=self.loop)
        self.json_output = json_output

    def tearDown(self):
        self.swarm = None

    def test_domain_list_resolve_ns(self):
        self.swarm.task_query(self.domains)


def line_gen(list_file):
    with open(list_file, 'r') as f:
        f = f.readlines()
        for line in f:
            line = line.strip("\n")
            yield line


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", dest='demo', action='store_true', default=False,
                        help='Demo mode. Show me what you got.')
    parser.add_argument('-o', "--out", dest='output', type=str, default='aioresolver.log')
    parser.add_argument('-i', '--json', dest='json_output', action='store_true')
    parser.add_argument('-w', '--workers', dest='num_workers', type=int, help='Number of async workers', default=1000)
    parser.add_argument('-l', '--list', dest='list_file', type=str, help='list of ips/domains to resolves')
    parser.add_argument('-d', '--domain', dest='single_query', type=str, help='Resolve a single domain.')
    parser.add_argument('-q', '--qtype', dest='qtype', help='DNS Query type to perform. Valid qtypes are:'
                                              'A, AAAA, CNAME, NS, MX, SOA, TXT, PTR', type=str, default='A')
    args = parser.parse_args()
    return args

def main():
    debug = False
    args = get_args()

    def run(domains_ips, qtype, _output, _json_output, _limit):
        _output = 'resolver.log'
        _json_output = False
        resolve = Resolver(domains_ips, qtype, _output, _json_output, _limit)
        resolve.test_domain_list_resolve_ns()

    if args.demo:
        demo = AsyncResolver()
        print(demo.wildcard_A('taobao.com'))
        print(demo.query_A('google.com'))
        print(demo.query_AAAA('google.com'))
        print(demo.query_CNAME('www.baidu.com'))
        print(demo.query_NS('google.com'))
        print(demo.query_MX('google.com'))
        print(demo.query_SOA('google.com'))
        print(demo.query_TXT('google.com'))
        print(demo.query_PTR('8.8.8.8'))
    else:
        limit = args.num_workers
        output = args.output
        json_output = args.json_output
        _qtype = args.qtype
        if args.list_file:
            list_file = args.list_file
            ips = line_gen(list_file)
            _ips = []
            for i in ips:
                _ips.append(i)
            run(_ips, _qtype, output, json_output, limit)

        else:
            limit = 1
            _domain = []
            if args.single_query:
                _domain.append(args.single_query)
                run(_domain, _qtype, output, json_output, limit)
            else:
                print('Specify either a list or  a query!')
                exit(1)


if __name__ == "__main__":

    try:
      main()
    except KeyboardInterrupt:
        exit(1)
