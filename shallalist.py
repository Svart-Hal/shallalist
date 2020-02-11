#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__	=	"Jason Brown"
__email__	=	"jason.brown@svarthal.io"
__version__	=	"0.2"
__license__	=	"Apache"
__date__	=	"20200211"


import urllib.request
from os import chown
from os import chmod
from os import system
from os import remove
from shutil import move
import subprocess
from datetime import datetime


def main():
	'''
    	Write the header file
	'''

	dnstime = datetime.today().strftime('%y%m%d%H%M')

	header = open('header.txt', 'w')
	header.write('$TTL 30 \n@ IN SOA rpz.malware.svarthal.net. hostmaster.svarthal.net. '+dnstime+' 300 1800 604800 30\n NS localhost.\n\n\n')
	header.close()

	'''
		Fetch new advertisements file and write it to disk
	'''

	shallalist = urllib.request.urlopen('https://raw.githubusercontent.com/cbuijs/shallalist/master/adv/domains')
	with open ('shallalist.txt', 'b+w') as ads:
		ads.write(shallalist.read())

	add_cname = '\t CNAME \t.'

	with open ('shallalist.txt', 'r') as cname:
		append_lines = [''.join([x.strip(), add_cname, '\n']) for x in cname.readlines()]

	with open('shallalist.txt', 'w') as append:
		append.writelines(append_lines)
	append.close()

	'''
		Open files and write to disk
	'''

	with open('header.txt', 'r') as header, open('shallalist.txt', 'r') as shallalist, open('db.adfiltering', 'w') as dbfile:
		dbfile.write(header.read() + shallalist.read().strip())
	dbfile.close()

	remove('header.txt')
	remove('shallalist.txt')

	chown('db.adfiltering', 0, 114)
	chmod('db.adfiltering', 0o644)
	move('db.adfiltering', '/etc/bind/db.ad-filtering')

if __name__ == '__main__':
	main()