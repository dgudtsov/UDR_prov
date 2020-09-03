#!/usr/bin/python
# encoding: utf-8
'''
Oracle® Communications Policy and Charging Rules Function - UDR XML profile importer

main is a description

It defines classes_and_methods

@author:     Denis Gudtsov

@copyright:  2020 All rights reserved.

@license:    Apache License

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import os
import time

import gzip

import json

import re

import xml.etree.ElementTree as ET
import lxml.etree as etree

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from xml_templates import xml_template
from xmlrpclib import boolean

__all__ = []
__version__ = 0.3
__date__ = '2020-04-28'
__updated__ = '2020-07-13'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

#chunk_size=1000000
default_chunk_size=10000000
default_skip_lines=0

string_values_separator=","

entitlements_delimiter=";"

timestamp_precision = 10000

output_dir='./output/'
filename_prefix='i_'
filename_suffix='.ixml.gz'

export_result = 'export.csv.gz'

prefix=''

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

class Generator(object):
    def __init__(self,begin,end):
        self.begin = begin
        self.end = end
        self.output_dir=output_dir
        self.xml_template=""
        return

    def generate(self):
        timestamp = int(time.time()*timestamp_precision)
    #    with open(filename_prefix+str(timestamp)+filename_suffix, 'w') as f:
        with gzip.open(self.output_dir+filename_prefix+str(timestamp)+filename_suffix, 'w') as f:
            for id in range(self.begin,self.end):
                f.write("%s\n" % self.xml_template.format(KEY=id).rstrip())
        return

class Export(object):
    def __init__(self, exml):
        self.output_dir=output_dir
        self.inputfile=exml
        return
    
    def process(self):
        
        with gzip.open(self.output_dir+export_result, 'w') as f_out:
            
            with gzip.open(self.inputfile) as f_inp:
                for data in f_inp:
#                    print data
#                    if (data.rstrip()!="") & (not re.search('<!--', data)):
# check for empty lines and xml comments
                    if (data.rstrip()!="") & (data.find('<!--')==-1):
                        result = ""
                        ents=list()
                        root = ET.fromstring(data)
                        for i in root.iter('field'):
                            if i.attrib['name'] == 'MSISDN':
                                result = i.text
                            if i.attrib['name'] == 'Entitlement':
                                if i.text is not None:
                                    ents.append(i.text)
                                    
                        # if all Entitlements on one line
                        if self.nline == False:
                            if len(ents) > 0:
                                result =  result+","+",".join(ents)
                            f_out.write("%s\n" % result)
                        else:
                    # each Entitlement on new line
                            if len(ents) > 0:
                                for e in ents:
                                    f_out.write("%s,%s\n" % (result,e))
                            else:
                                f_out.write("%s\n" % result)
                            pass
    #                    print result
                        
        return


class Bulk(object):
    def __init__(self,inputfile):
        self.output_dir=output_dir
        self.xml_template=""
        self.skip_lines=default_skip_lines
        self.chunk_size=default_chunk_size
        self.inputfile=inputfile
        
        self.ent_statistics=dict()
        return
    
    def statistics_count(self,key):

        concat_plus="+"
        stat_key=concat_plus.join(key).rstrip()
        
        if stat_key in self.ent_statistics:
            self.ent_statistics[stat_key]+=1
        else:
            self.ent_statistics[stat_key]=1

        return
    
    def statistics_dump(self):
        print "file statistics: "
        print json.dumps(self.ent_statistics,sort_keys=True,indent=True)
    
    def process(self):
        
        with gzip.open(self.inputfile) as f_inp:
            for i in range(self.skip_lines): f_inp.readline()

            exit=False
            ent_statistics=dict()
            
            while True:
                chunk=[]
                entitlements=[]
                
                new_key, old_key="",""
                
                timestamp = int(time.time()*timestamp_precision)
                with gzip.open(self.output_dir+filename_prefix+str(timestamp)+filename_suffix, 'w') as f_out:
                
                    for i in range(self.chunk_size):
                        
                        data=f_inp.readline()
                        if not data:
                            exit=True
                            break
                        
                        data_list = data.rstrip().split(string_values_separator)
                        
#                        list=["1"]
#                        new_key, ent = prefix+'{}'.format(data_list[0]) , list                        
                        new_key, ent = prefix+'{}'.format(data_list[0]) , data_list[1:]

                        
                        if ((new_key==old_key or len(entitlements)==0) and len(ent)>0):
#                            entitlements.append(ent)
                            entitlements=entitlements+ent                        
                        else:
                            entitlements_value=entitlements_delimiter
                            
                            xml_result = self.xml_template.format(KEY=old_key,Entitlement=entitlements_value.join(entitlements).rstrip())
    
                            f_out.write("%s\n" % xml_result)
                            
                            self.statistics_count(entitlements)
                            
                            entitlements=ent[:]
                            
                        old_key=new_key
                
                if exit:
                    break 
    #                    chunk.append(prefix+'{}'.format(data_list[0]))
                    
#                xml_list=process_chunk(chunk,entitlements)
#                dump_ixml(xml_list)
#                if len(chunk) < chunk_size:
#                    break
            self.statistics_dump()
        
        return

    
def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Denis Gudtsov on %s.
  Copyright 2020. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("-a", "--action", dest="action", required=False, choices=xml_template.keys(), help="action with template to use: create subscriber, delete subscriber, etc...")
        group.add_argument("-x", "--export", dest="exml", required=False, action="store_true", help="treat file passed as export from UDR")
        group.add_argument("-l", "--list", dest="list", required=False, action="store_true", help="list of all action templates")
        
        parser.add_argument("-s", "--skip", dest="skip_lines", action="store", default=default_skip_lines, type=int, help="number of lines to skip when read source file [default: %(default)d]. Is not applicable for --generate option")
        parser.add_argument("-n", "--new-line", dest="nline", required=False, default=False, action="store_true", help="export each Entitlement on new line (one ent per row)")
        parser.add_argument("-o", "--output", dest="output", default=output_dir, help="output directory where result files will be stored [default: %(default)s]")
        
        parser.add_argument("-g", "--generate", dest="generate", action="store_true", help="generate profiles using -b and -e range definition and -a template")
        
        parser.add_argument("-b", "--begin", dest="range_being", type=int, help="start of range")
        parser.add_argument("-e", "--end", dest="range_end", type=int, help="end of range")
        parser.add_argument("-c", "--chunk", dest="chunk_size", action="store", default=default_chunk_size, type=int, help="number of chunks per file [default: %(default)d]. Is not applicable for --generate option")

        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument(dest="paths", help="paths to folder(s) with source file(s) [default: %(default)s]", metavar="path", nargs='*')

        # Process arguments
        args = parser.parse_args()

        paths = args.paths
        verbose = args.verbose
        
        output = args.output
        
#        exml = args.exml
#        nline = args.nline
        
        action = args.action
        
        skip_lines = args.skip_lines
        chunk_size = args.chunk_size
        
#        gen = args.generate
#        gen_begin = args.range_being
#        gen_end = args.range_end

        if verbose > 0:
            print("Verbose mode on")

        if args.generate:
            print("generator")
            gen_begin = args.range_being
            gen_end = args.range_end

            gen = Generator(gen_begin,gen_end)
            gen.output_dir=output
            gen.xml_template=xml_template[action]
            gen.generate()
        elif args.list:
            for k,v in xml_template.iteritems():
                x = etree.fromstring(v)
                print "template: %s" % k
                print etree.tostring(x, pretty_print=True)
            pass
        elif args.exml:
            print("export translator")
            nline = args.nline
            for inpath in paths:
                exp = Export(inpath)
                exp.nline = nline
                exp.process()    
            print "export is done"
        else:
            print("processor")
            for inpath in paths:
            ### do something with inpath ###
                print("processing "+inpath)
                bulk = Bulk(inpath)
                bulk.output_dir=output
                bulk.xml_template=xml_template[action]
                bulk.chunk_size=chunk_size
                bulk.skip_lines=skip_lines
                bulk.process()
                print "processing file is done"
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
#    print (sys.argv);
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'main_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())