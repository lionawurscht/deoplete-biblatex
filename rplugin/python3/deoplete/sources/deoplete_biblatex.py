#!/usr/bin/env
import re
import os

from .base import Base
from deoplete.util import load_external_module

import bibtexparser

load_external_module(__file__, 'sources/deoplete_biblatex')

MY_CODES = {
    'lion:': 'test',
    'tandem:': 'test',
}


def bibtexparser_customizations(record):
    record = bibtexparser.customization.author(record)
    record = bibtexparser.customization.editor(record)
    return record


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)

        self.__pattern = re.compile(r'\[(?:[\w,]*:)?(?:\w+,)*\w+$')

        self.filetypes = ['rst', 'markdown']
        self.mark = '[bib]'
        self.name = 'biblatex'

    def on_init(self, context):
        self.__bib_file = context['vars'].get(
            'deoplete#sources#biblatex#bibfile',
            '~/bibliography.bib'
        )
        self.__bib_file = os.path.abspath(os.path.expanduser(self.__bib_file))
        try:
            with open(self.__bib_file) as bf:
                parser = bibtexparser.bparser.BibTexParser(
                    ignore_nonstandard_types=False,
                )
                parser.customization = bibtexparser_customizations
                self.__bibliography = bibtexparser.load(
                    bf,
                    parser=parser,
                ).entries_dict
        except FileNotFoundError:
            self.vim.err_write(
                '[deoplete-biblatex] No such file: {0}\n'.format(
                    self.__bib_file,
                ),
            )

        pattern_delimiter = context['vars'].get(
            'deoplete#sources#biblatex#delimiter',
            ',',
        )
        pattern_start = context['vars'].get(
            'deoplete#sources#biblatex#startpattern',
            r'\[(?:[\w,]+:)?',
        )
        pattern_completed = r'(?:\w+{})*'.format(pattern_delimiter)
        pattern_current = r'\w+$'

        self.__pattern = re.compile(
            pattern_start
            + pattern_completed
            + pattern_current
        )

    def gather_candidates(self, context):
        if self.__pattern.search(context['input']):
            return [{'word': v['ID'], 'kind': v['ENTRYTYPE']}
                    for (k, v) in self.__bibliography.items()]
        else:
            return []
