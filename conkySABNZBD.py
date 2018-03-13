#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: sabnzbd status information
# Original Creator: sabooky <sabooky@yahoo.com>
# Rewritten for new SABNZDB API by: blades <blades@gecko.org.uk>
# Also reuses elements of code from Kaivalagi's conkyForecast code
# for reading in files and parsing templates

import sys
from sabapi import sab
from optparse import OptionParser
from json import load
import os
import codecs


def parse_file(filename, default_content):
    """parse templates if provided; else use default output"""
    if filename is None or filename == "":
        # create default template
        template = default_content
    else:
        # load the template file contents
        try:
            fileinput = codecs.open(os.path.expanduser(filename), encoding='utf-8')
            template = fileinput.read()
            fileinput.close()
            # lose the final "\n" which should always be there...
            template = template[0:len(template)-1]
        except:
            print("Template file not found!")
            sys.exit(2)
    return template


def fillTemplate(options, template, json):
    output = ""
    end = False
    a = 0
    # a and b are indexes in the template string
    # moving from left to right the string is processed
    # b is index of the opening bracket and a of the closing bracket
    # everything between b and a is a template that needs to be parsed
    while not end:
        b = template.find('[', a)
        if b == -1:
            b = len(template)
            end = True
        # if there is something between a and b, append it straight to output
        if b > a:
            output += template[a:b]
            # check for the escape char (if we are not at the end)
            if template[b - 1] == '\\' and not end:
                # if its there, replace it by the bracket
                output = output[:-1] + '['
                # skip the bracket in the input string and continue from the beginning
                a = b + 1
                continue
        if end:
            break
        a = template.find(']', b)
        if a == -1:
            print("Missing terminal bracket (]) for a template item")
            return ""
        # if there is some template text...
        if a > b + 1:
            variable = template[b+1:a]
            # do jobs template
            if variable == "jobs":
                for key, slot in enumerate(json["slots"]):
                    if key < options.jobCount:
                        output += fillTemplate(options, options.jobTemplateFile, slot)
            else:
                output += str(json[variable])
        a = a + 1
    return output


def writeOutput(options, json):
    output = fillTemplate(options, options.templateFile, json)
    print(output.encode("utf-8"))

# parse command line options
parser = OptionParser()
parser.add_option("-c", "--config", default="/opt/sabnzbd/sabnzbd.ini", dest="configFile", help="Path to sabnzbd.ini file", metavar="CONFIGFILE")
parser.add_option("-t", "--template", dest="templateFile", help="Path to template output file", metavar="TEMPLATEFILE")
parser.add_option("-j", "--jobtemplate", dest="jobTemplateFile", help="Path to job template output file", metavar="JOBTEMPLATEFILE")
parser.add_option("-k", "--jobcount", default="all", dest="jobCount", help="Number of jobs to write out")
(options, args) = parser.parse_args()

sabnzbd = sab(cfgfile=options.configFile)
jsonstring = sabnzbd.get_queue()
json = load(jsonstring)
if options.jobCount == "all":
    options.jobCount = len(json["queue"]["slots"])
options.jobCount = int(options.jobCount) - 1
options.templateFile = parse_file(options.templateFile, "Total ETA: [eta]\n")
options.jobTemplateFile = parse_file(options.jobTemplateFile, "[filename]: [percentage]% of [size] - ETA [timeleft]\n")
writeOutput(options, json["queue"])
