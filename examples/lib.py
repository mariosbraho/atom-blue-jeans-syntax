# -*- coding: utf-8 -*-
import itertools
import codecs
from matcher import matcher


class Transliteration(object):

    def __init__(self, word, max_diphthong_length=2):
        self.word = word
        self.max_diphthong_length = 2
        self.result = []
        self._transliterate()

    def _transliterate(self):
        letters = list(self.word)
        all_combinations = self._combine(letters)
        diphthong_combinations = self._diphthong_combine(all_combinations)
        latin_combinations = self._to_latin(diphthong_combinations)
        min_length_combinations = self._min_length(latin_combinations)
        print('hello')
        # fixed_pronounced = self._fixed_pronounced(min_length_combinations)
        self.result = self._final_combine(min_length_combinations)

    def _combine(self, letters):
        if len(letters) < 2:
            return [letters]
        return [[letters[0]] + x for x in self._combine(letters[1:])] + \
            self._combine([letters[0] + letters[1]] + letters[2:])

    def _diphthong_combine(self, all_combinations):
        diphthong_combinations = []
        for combination in all_combinations:
            exceeds_max_diphthong_length = False
            for item in combination:
                if len(item) > self.max_diphthong_length:
                    exceeds_max_diphthong_length = True
            if not exceeds_max_diphthong_length:
                diphthong_combinations.append(combination)
        return diphthong_combinations

    def _to_latin(self, combinations):
        keys = matcher.keys()
        latin_combinations = []
        for combination in combinations:
            latin_combination = []
            not_applicable = False
            for letter in combination:
                if letter in keys:
                    latin_combination.append(matcher[letter])
                else:
                    not_applicable = True
            if not not_applicable:
                latin_combinations.append(latin_combination)
        return latin_combinations

    def _min_length(self, latin_combinations):
        min_length_combinations = []
        combinations_length = []
        for combination in latin_combinations:
            combinations_length.append(len(combination))
        min_length_combination = min(combinations_length)
        for combination in latin_combinations:
            if len(combination) == min_length_combination:
                min_length_combinations.append(combination)
        return min_length_combinations

    def _fixed_pronounced(self, min_length_combinations):
        fixed_pronounced = []
        multi_pronounce_rules = matcher['multi_pronounce']
        for index, combination in enumerate(min_length_combinations):
            for index_letters, letters in enumerate(combination):
                letter = [letter for letter in letters if letter in multi_pronounce_rules.keys()]
                if len(letter) > 0:
                    if len(combination) > index_letters:
                        pass
        return fixed_pronounced

    def _final_combine(self, min_length_combinations):
        final_words = []
        for index, combination in enumerate(min_length_combinations):
            word_combinations = list(itertools.product(*combination))
            for word_combination in word_combinations:
                word = ''.join(word_combination)
                if word not in final_words:
                    final_words.append(word)
        return final_words
