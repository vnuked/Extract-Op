#!/usr/bin/env python

import sys
import re
import commands

exp = r'([0-9a-fA-f]{2})\s'
exp2 = r'\s<.*>'

def findop(pat, text):
	m = re.findall(pat, text)
	if m:
		while len(m) > 6:
			m.pop()
		return m
	return None

def parse_content(data):
	ndata = []

	for line in data:
		found = re.findall(exp2, line)
		if found:
			for fd in found:
				line = line.replace(fd, '')
		ndata.append(line)
	return ndata

def main():
	matches = []
	comm = 'objdump -d %s' %(sys.argv[1])
	sc = ''

	status, out = commands.getstatusoutput(comm)
	if status:
		sys.stderr.write('Unable to use objdump..\n')
		sys.stderr.write('Exiting..\n')
		sys.exit(-1)

	content = out.split('\n')
	ncontent = parse_content(content)

	for line in ncontent:
		mt = findop(exp, line)
		if mt:
			matches += mt

	if not matches:
		sys.stderr.write('No Match Found..\n')
		sys.stderr.write('Exiting..\n')
		sys.exit(-1)

	for op in matches:
		sc += '\\x%s' %(op)
	print sc

if __name__ == '__main__':
	if len(sys.argv) != 2:
		sys.stderr.write('Invalid Command Line Arguments..\n')
		sys.stderr.write('Exiting..\n')
		sys.exit(-1)
	else:
		main()

