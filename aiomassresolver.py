#!/usr/bin/env python3
# encoding: utf-8
# AioMassResolver ~ uvloop & aiodns - resolve bulk dns queries extremely quickly

"""
author: darkerego ~  2019/5/19 ~ xelectron@protonmail.com
"""
import random
import string
import argparse
import aiodns
import asyncio
import ipaddress
import uvloop
from time import process_time
from colorama import init, Fore, Style

init(autoreset=True)


class AsyncResolver(object):
    # results: Dict[Any, Any]

    def __init__(self, num_workers=5, nameservers=['8.8.8.8', '8.8.4.4'], loop=None, qtype="A", debug=False):
        self.timeout = 0.1
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

        # TODO: Make this async so we can run a list of wildcard queries

    def wildcard_A(self, domain):
        genrandstr = lambda i: ''.join(random.choices(string.ascii_lowercase + string.digits, k=i))
        tasks = [asyncio.ensure_future(self.query(genrandstr(20) + '.' + domain, 'A')) for _ in range(6)]
        reqs = asyncio.gather(*tasks)
        try:
            f = self.loop.run_until_complete(reqs)
            data = list(set(map(lambda x: x[0].host, f)))
            print(Fore.GREEN + '[*] Found wildcard dns records:')
            return data
        except:
            return Fore.RED + '[!] Found no wildcard dns records.'


    async def query(self, domain, qtype):

        return await self.resolver.query(domain, qtype)

    def task_query(self, domains, output):

        tasks = []
        q = asyncio.Queue()

        for domain in domains:
            q.put_nowait(domain)

        for i in range(self.num_workers):
            tasks.append(self.do_work(q, output))

        self.loop.run_until_complete(asyncio.wait(tasks))
        return self.results

    async def do_work(self, work_queue, output):

        def writer(_data):
            """
             Logger function
            :param _data: data to write to file
            :return: -
            """
            with open(output, 'a') as ff:
                ff.write(str(_data) + "\n")

        resolver = aiodns.DNSResolver(loop=self.loop, nameservers=self.nameservers, timeout=2, tries=1)
        # resolver = aiodns.DNSResolver(loop=loop)
        while not work_queue.empty():
            domain: object = await work_queue.get()
            qtype = self.qtype
            debug = self.debug
            item = None
            try:
                if qtype == 'PTR':
                    res = await resolver.query(ipaddress.ip_address(domain).reverse_pointer, 'PTR')
                else:
                    res = await self.query(domain, self.qtype)

            except aiodns.error.DNSError as e:
                error_code: object = e.args[0]
                if self.debug:
                    print(Fore.RED + "[DEBUG]: error: " + str(e))
                if error_code == aiodns.error.ARES_ECONNREFUSED:
                    self.results = "CONNECTION_REFUSED"
                elif error_code == aiodns.error.ARES_ENODATA:
                    self.results = "NODATA"
                elif error_code == aiodns.error.ARES_ENOTFOUND:
                    self.results = "NXDOMAIN"
                elif error_code == aiodns.error.ARES_EREFUSED:
                    self.results = "REFUSED"
                elif error_code == aiodns.error.ARES_ESERVFAIL:
                    self.results = "SERVFAIL"
                elif error_code == aiodns.error.ARES_ETIMEOUT:
                    self.results = "TIMEOUT"
                else:
                    self.results[domain] = "UNKNOWN_STATUS"

            except Exception as e:
                print(str(domain) + ' error: ' + str(e))
                if debug:
                    print(Fore.RED + "[debug]: raw :" + str(e))
            else:
                self.results = res
                if qtype == 'A':
                    data = list(map(lambda x: x.host, res))
                    item = {"domain": domain, "type": "A", "data": data}
                elif qtype == 'AAAA':
                    data = list(map(lambda x: x.host, res))
                    item = {"domain": domain, "type": "AAAA", "data": data}
                elif qtype == 'CNAME':

                    data = res.cname
                    item = {"domain": domain, "type": "CNAME", "data": data}
                elif qtype == 'MX':

                    data = list(map(lambda x: x.host, res))
                    item = {"domain": domain, "type": "MX", "data": data}
                    print(item)
                elif qtype == 'NS':

                    data = list(map(lambda x: x.host, res))
                    item = {"domain": domain, "type": "NS", "data": data}
                elif qtype == 'SOA':
                    data = res.nsname
                    item = {"domain": domain, "type": "SOA", "data": data}
                elif qtype == 'TXT':
                    data = list(map(lambda x: x.text, res))
                    item = {"domain": domain, "type": "TXT", "data": data}
                elif qtype == 'SRV':
                    data = list(map(lambda x: x.host, res))
                    item = {"domain": domain, "type": "SRV", "data": data}
                elif qtype == 'NAPTR':
                    data = list(map(lambda x: x.replacement, res))
                    item = {"domain": domain, "type": "NAPTR", "data": data}
                elif qtype == 'PTR':
                    data = res.name
                    item = {"domain": data, "type": "PTR", "data": [domain]}
                else:
                    # self.results[domain] = res
                    raise ValueError('Invalid query type.')
            finally:
                if item is not None:
                    print(item)
                    writer(item)
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
        self.swarm.task_query(self.domains, self.output)


def line_gen(list_file):
    with open(list_file, 'r') as f:
        f = f.readlines()
        for line in f:
            line = line.strip("\n")
            yield line


def get_args():

    usage = "Uvloop & AIODns Powered Resolver. Resolve thousands of domains in seconds.\n"
    usage += "example usage: $ python3 ./aioresolver.py --list domains.list --qtype 'A' "
    parser = argparse.ArgumentParser(usage)

    parser.add_argument('-o', "--out", dest='output', type=str, default='aioresolver.log')
    # parser.add_argument('-i', '--json', dest='json_output', action='store_true')
    parser.add_argument('-w', '--workers', dest='num_workers', type=int, help='Number of async workers to use.'
                                                                              'Increase this for longer lists. '
                                                                              'Default: 1000', default=1000)
    parser.add_argument('-l', '--list', dest='list_file', type=str, help='list of ips/domains to resolves')
    parser.add_argument('-d', '--domain', dest='single_query', type=str, help='Resolve a single domain.')
    parser.add_argument('-q', '--qtype', dest='qtype', help='DNS Query type to perform. Valid qtypes are:'
                                              'A, AAAA, CNAME, NS, MX, SOA, TXT, PTR', type=str, default='A',
                        choices=['A', 'AAAA', 'CNAME', 'NS', 'MX', 'SOA', 'TXT', 'PTR'])
    parser.add_argument("-W", "--wildcard_A", dest='wildcard', type=str, default=False,
                        help='Run a wildcard_A query against a single domain. Example: '
                             './aiomassresolver.py -W taobao.com')
    args = parser.parse_args()
    return args

def main():
    debug = False
    args = get_args()

    def run(domains_ips, qtype, _output, _json_output, _limit):
        _json_output = False
        resolve = Resolver(domains_ips, qtype, _output, _json_output, _limit)
        resolve.test_domain_list_resolve_ns()
    if args.output:
        output = args.output
    if args.wildcard:
        domain = args.wildcard
        resolver = AsyncResolver()
        print(resolver.wildcard_A(domain))
    else:
        limit = args.num_workers
        # output = args.output
        json_output = True  # TODO: remove this redundant argument
        _qtype = args.qtype
        if args.list_file:
            list_file = args.list_file
            print(Fore.YELLOW + 'Reading from file %s' % list_file)
            queries = line_gen(list_file)
            _queries = []
            for i in queries:
                _queries.append(i)
            t = process_time()
            run(_queries, _qtype, output, json_output, limit)
            elapsed_time = process_time() - t
            print(Fore.YELLOW + "--------------------------------------------------------------------------")
            print("Finished! Process time: " + str(elapsed_time))

        else:
            limit = 1
            _domain = []
            if args.single_query:
                _domain.append(args.single_query)
                run(_domain, _qtype, output, json_output, limit)
            else:
                print(Fore.RED + '[Error]: Specify either a list or  a query! Run --help for usage.')
                exit(1)


if __name__ == "__main__":

    try:
      main()
    except KeyboardInterrupt:
        exit(1)
