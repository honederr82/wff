#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright 2021 Roland Honeder
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
import re


class WffValidator:
    """
        Determine if a given string is a well formed formula, based on the given alphabet.

        Attributes
        ----------
        sigma : list
            define strings with symbols in alphabet (p, p1, p2...)
        connectives : list
            used connectives (caveat: must include ¬!)
        helpers : list
            helper symbols in your alphabet definition

        Methods
        -------
        validate(input=str)
            validate input string agains wff rules
        """
    sigma: list = ['p3', 'p8', 'p145', 'p212']
    connectives: list = ['¬', '∧', '∨', '→', '↔']
    helpers: list = ['(', ')']
    alphabet: list = sigma + connectives + helpers

    symbol_table: list = []
    symbols_replaced: list = []
    parsed_input: str = ''

    def __init__(self):
        self.symbol_table = []
        self.symbols_replaced = []

    def substitute(self, result):
        """ substitute valid expressions with internal symbols. """
        result = list(set(result))
        start_idx = len(self.symbols_replaced)
        for idx, element in enumerate(result):
            lookup_key = F"[{start_idx}_{idx}]"
            self.symbols_replaced.append(lookup_key)
            self.parsed_input = self.parsed_input.replace(element, lookup_key)

    def extract_symbols(self, input: str) -> list:
        """ extract used symbols (p, p1) including negation """
        result = []
        for element in self.sigma:
            result += re.findall('[¬]*' + element, input)
        self.substitute(result)
        self.symbol_table = result

    def extract_conjunctors(self, input: str, elements: list):
        """ Extract expressions connected by conjunction in form (a ∧ b) etc. """
        result = []
        connectives = self.connectives.copy()
        connectives.remove('¬')
        for first_element in elements:
            for second_element in elements:
                result += re.findall('[¬]*[(]' + re.escape(first_element) + '[\s]?[' + ''.join(connectives) + '][\s]?' +
                                     re.escape(second_element) + '[)]', input)
        self.substitute(result)

    def validate(self, input: str) -> bool:
        """ Validate input string. """
        self.parsed_input = input
        self.extract_symbols(input)
        while self.parsed_input != '':
            last = self.parsed_input
            self.extract_conjunctors(self.parsed_input, self.symbol_table + self.symbols_replaced)
            if last == self.parsed_input: break
        return bool(re.search('^\[[0-9_]*\]$', self.parsed_input))


if __name__ == '__main__':
    wff_validator = WffValidator()
    print(wff_validator.validate('¬¬¬¬¬p3'))
