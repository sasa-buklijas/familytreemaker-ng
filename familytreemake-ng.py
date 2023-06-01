#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Saša Buklijaš"
__copyright__ = "Copyright 2023, Saša Buklijaš"
__license__ = "GPL"
__version__ = "3.0"

import argparse

class FTError(Exception):
    """A base class for FTError exceptions."""
    
class ParsingError(FTError):
	"""A custom exception class for parsing input file."""


class Family:
	"""Represents the whole family.
	"""

	def __init__(self, input_file: str):
		# parsing input_file
		# with more rigid format of input family file it is easier to parse it
		with open(input_file, "r") as f:
			for line_number, line in enumerate(f):
				print(line_number, line, end='')

				line = line.rstrip()
				# maybe I will have same in \t later, then I can make it as function
				# separated because it is not important
				if line == '':  # after rstrip() \n is ''
					print('    # SKIP/IGNORE EMPTY LINE')
					continue
				elif line[0] == '#':  # if it is comment, just skip it
					print('    # SKIP/IGNORE COMMENT')
					continue

				if line[0] == '\t':
					print('    # THIS IS CHILD')
				elif len(line) >= 6:# (id=x)
					print('    # THIS IS PERSON IN UNION')
				else:
					raise ParsingError(f'Do not know how to parse line number {line_number}::{line}')

class Person:
	"""Represents the person.
	"""

	def __init__(self, line_to_parse: str):
		pass


def main():
	# Parse command line options
	parser = argparse.ArgumentParser(description=
		'Generates a family tree graph in .DOT format to STDOUT from a simple text file')
	parser.add_argument('input_file', metavar='INPUT_FILE',
		help='the formatted text file representing the family')
	args = parser.parse_args()
	#print(args)

	# Create the family
	family = Family(args.input_file)

if __name__ == '__main__':
	main()
