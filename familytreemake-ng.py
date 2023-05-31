#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Saša Buklijaš"
__copyright__ = "Copyright 2023, Saša Buklijaš"
__license__ = "GPL"
__version__ = "3.0"

import argparse


def main():
	# Parse command line options
	parser = argparse.ArgumentParser(description=
		'Generates a family tree graph in .DOT format to STDOUT from a simple text file')
	parser.add_argument('input_file', metavar='INPUT_FILE',
		help='the formatted text file representing the family')
	args = parser.parse_args()
	print(args)

if __name__ == '__main__':
	main()
