#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Saša Buklijaš"
__copyright__ = "Copyright 2023, Saša Buklijaš"
__license__ = "GPL"
__version__ = "3.0"

import argparse

class Family:
	"""Represents the whole family.
	"""
	
	def __init__(self, input_file: str):
		# parsing input_file
		with open(input_file, "r") as f:
			for line_number, line in enumerate(f):
				print(line_number, line, end='')


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
