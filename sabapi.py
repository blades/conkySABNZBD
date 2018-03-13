#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: sabapi module for conkySABNZBD
# Original Author: sabooky <sabooky@yahoo.com>
# Rewritten for new SABNZDB API output by: blades <blades@gecko.org.uk>

import urllib.parse
import urllib.request
from os.path import expanduser

DEBUG = 0


class sab:
    def __init__(self, cfgfile=''):
        if cfgfile:
            (host, port, api_key) = self.parse_cfg(cfgfile)
        self.api = 'http://%s:%s/sabnzbd/api?' % (host, port)
        self.query = {'apikey': api_key}
        self.data = {}
        self.KBps = 0
        self.pp = 6

    def connect(self, add_query, command=False):
        """connects to server using add_query(k,v pair or dict obj).
        Setting command to True returns server response (string)
        otherwise returns a urlopen object"""
        query = self.query
        query.update(add_query)
        query = urllib.parse.urlencode(query)
        if DEBUG == 1:
            print(query)
        try:
            response = urllib.request.urlopen(self.api + query)
        except IOError as e:
            # shutdown command raises a protocol error
            # this could potentially cause problems in the future
            if command and e[0] == 'http protocol error':
                    return 'ok'
            else:
                raise
        if response == "error: API Key Required":
            raise Exception('API Key required')
        if response == "error: API Key Incorrect":
            raise Exception('API Key incorrect')
        if command:
            return response.read().strip()
        return response

    def parse_cfg(self, config):
        "Reads sab config file returning (host, port, api_key)"
        f = open(expanduser(config))
        wanted = ['host', 'port', 'api_key']
        options = {}
        for line in f:
            line = line.strip()
            if line.startswith('[') and line.strip('[]') == 'misc':
                for line in f:
                    if line.startswith('['):
                        break
                    k, v = [x.strip() for x in line.split('=')]
                    if k in wanted:
                        options[k] = v
                break
        if not set(options.keys()) == set(wanted):
            return
        return [options.get(x) for x in wanted]

    def get_queue(self):
        """Returns a dict representation of qstatus"""
        query = {'mode': 'queue', 'output': 'json'}
        return self.connect(query)

    def addid(self, id):
        "add newzbin report id to sab"
        query = {'mode': 'addid', 'name': id, 'pp': self.pp}
        return self.connect(query, True)

    def addurl(self, url):
        "add url of nzb file to sab"
        query = {'mode': 'addurl', 'name': url, 'pp': self.pp}
        return self.connect(query, True)

    def pause(self):
        "pause sab"
        query = {'mode': 'pause'}
        return self.connect(query, True)

    def resume(self):
        "resume sab"
        query = {'mode': 'resume'}
        return self.connect(query, True)

    def shutdown(self):
        "shutdown sab"
        query = {'mode': 'shutdown'}
        return self.connect(query, True)
