#!/usr/bin/env
import re

from deoplete.util import Base


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)

        self.__pattern = re.compile(r'[')

        self.filetypes = ['rst']
        self.mark = '[bib]'
        self.matchers = ['matcher_length', 'matcher_full_fuzzy']
        self.name = 'biblatex'

    def gather_candidates(self, context):
        return [{'word': "lion", 'kind': "test"}]

    def get_complete_position(self, context):
        match = self.__pattern.search(context['input'])
        return match.start() if match is not None else -1
