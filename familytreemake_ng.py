#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Saša Buklijaš"
__copyright__ = "Copyright 2023, Saša Buklijaš"
__license__ = "GPL"
__version__ = "3.0"

import argparse
#from pathlib import Path
import re
from dataclasses import dataclass
from enum import Flag, auto

class FTError(Exception):
    """A base class for FTError exceptions."""
    

class ParsingError(FTError):
	"""A custom exception class for parsing input file."""

	error_message = 'Incorrect person format on line number {}::"{}"'

	def __init__(self, *args):
		super().__init__(*args)
		self.args = args

	def __str__(self):
		return self.error_message.format(*self.args)


class DuplicatedPersonIDError(ParsingError):
	"""A custom exception class for duplicated person id inside input file."""

	error_message = 'Person from line={0}, have same id(already defined) '\
					'as person from line={1.first_seen_in_line}--->{1}'

	def __init__(self, *args):
		super().__init__(*args)
		self.args = args

	def __str__(self):
		return self.error_message.format(self.args[0], self.args[1])


class Family:
	"""Represents the whole family.
	"""

	def __init__(self, input_file: str):
		# TODO: make public accessors for _persons
		self._persons = dict()	# every person in family
		self._parse_input_file(input_file)
		
	def _parse_input_file(self, input_file: str):
		"""parsing input_file
			with more rigid format of input family file it is easier to parse it
		"""

		class State():
			'''When first first member of household is found,
				second member of household must also be present,
				otherwise exception is raised'''

			class Line(Flag):
				'''Representing line state, what is line'''
				EMPTY = auto()
				COMMENT = auto()
				PERSON1 = auto()	# first member of household
				PERSON2 = auto()	# second member of household
				CHILD = auto()
		
			def __init__(self):
				self.__first_member_of_household: bool = True

			def validate_file(x: Line):
				pass

		#RODO: remove if stupid idea
		#second_partner_is_next: bool = False
		household = None
		with open(input_file, "r") as f:
			for line_number, line in enumerate(f, start=1):
				print(line_number, line, end='')

				line = line.rstrip()
				# maybe I will have same in \t later, then I can make it as function
				# separated because it is not important
				if line == '':  # after rstrip() \n is ''
					#print('    # SKIP/IGNORE EMPTY LINE')
					continue
				elif line[0] == '#':  # if it is comment, just skip it
					#print('    # SKIP/IGNORE COMMENT')
					continue

				if line[0] == '\t':
					print('    # THIS IS CHILD')
					# TODO: will see how
					# parse child
					# child must start with name can not be mentioned first time
				elif len(line) >= 6:# (id=x)
					print('    # THIS IS PERSON IN UNION')
					#FIXME: delete if not needed
					#line_state = Line.PERSON
					
					regex = r'''
						# start with main_name, what is first and second name together
							# [\w ]+?, ? is there so that + is non-greedy
							# (?:[ ]*)? is there so that there can be multiple spaces after name, 
								# but we do not capture it
						^(?P<main_name>[\w ]+?)(?:[ ]*)? 

						# ( mandatory, start for attributes
						\(							

						# gender is mandatory M or F ends with ','
						(?P<gender>[M|F]),[ ]*		# male or female, end with ',', zero or more spaces allowed
		
						# id is mandatory ',' allowed zero on one time, paces allowed after ','
							# no spaces ' ' allowed in id
						id=(?P<id>[\w]+),[ ]*   	
						
						# birth_day is mandatory, because you will not add somebody who is not born
							# [\w ]+?, ? is there so that + is non-greedy
						#birth_day=(?P<birth_day>[\w ]+?)(?:,?[ ]*)? # more advanced version, add if needed
						birth_day=(?P<birth_day>[\w]+),[ ]*  

						# death_day is optional
							# [\w ]+?, ? is there so that + is non-greedy
						(?:death_day=(?P<death_day>[\w]+),[ ]*)?
						#(?:death_day=(?P<death_day>[\w ]+,))[ ]* 

						# maiden_name is optional, this is surname before marriage
						(?:maiden_name=(?P<maiden_name>[\w]+),[ ]*)?

						\)$	# end with ')', can be spaces after it in original line because of rstrip()
					'''

					match = re.search(regex, line, re.VERBOSE)
					if 	match is None:
						raise ParsingError(line_number, line, match)

					# think that this is not need anymore
					elif ('main_name', 'gender', 'id', 'birth_day') in match.groupdict():
						raise ParsingError(
							f'Incorrect person format on line number {line_number}::"{line}"\n{match.groupdict()}')
					
					else:
						exist: Person = self.__is_person_already_in_family(match.group('id'))
						if exist:
							raise DuplicatedPersonIDError(line_number, exist)
						else:
							new_person = Person(match.group('main_name'),
												match.group('gender'),
												match.group('id'),
												match.group('birth_day'),
												line_number,
												match.group('death_day'),	
												match.group('maiden_name'),)
							#TODO: do it alike property self.add_person(new_person), maybe not best idea
							self._persons[match.group('id')] = new_person

							if not(household):	# first time
								#TODO: not happy with this design, 
								# thing that everything should be handled by Family class/object
								household: Household = Household(new_person)
							else:
								household.add_householder(new_person)
								# add household to family ???
								household = None


							


						#second_partner_is_next = True

						#print(f'	GROUP: {match.groupdict()}')

					if line[0] == '(':
						raise ParsingError(line_number, line)
						# this is just id, person was defined before
						# we just need to find id and make connection

					if line[0] in (' ', '\t'):	# parsing children's
						raise ParsingError(line_number, line)
		
				else:
					raise ParsingError(line_number, line)
			
			if household:
				raise ValueError(f'Household {household}, not completed, missing second person.')
		
		return True
	
	def __is_person_already_in_family(self, id: str):
		'''Return TRUE if id/person is already in family'''

		if id in self._persons:
			return self._persons[id]
		return False
	

@dataclass(frozen=True)	# frozen=True means it can not be changed once it is created
class Person:
	"""Represents the person.
	"""
	main_name: str
	gender: str
	id: str
	birth_day: str 
	first_seen_in_line: int	  # for debug is ti is seen
	death_day: str = None
	maiden_name: str = None
	
@dataclass()
class Household:
	'''Represent union of two people,
		with or without children's'''
	person1: Person		# first person is just first parsed person
	person2: Person = None
	# currently both persons can be same gender, can be changed in future

	def add_householder(self, p: Person):
		if self.is_full():
			ValueError(f'Person {p}, is 3rd person in household. Only 2 persons allowed.')
		self.person2 = p

	# FIXME: currently not needed, keep it if you need it in future
	#def is_empty(self):
	#	return any(self.person1, self.person2)
	
	def is_full(self):
		'''Household is full, if there are both persons'''
		return all((self.person1, self.person2))

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

	print('\nfamily._persons:\n', family._persons)

if __name__ == '__main__':
	main()
