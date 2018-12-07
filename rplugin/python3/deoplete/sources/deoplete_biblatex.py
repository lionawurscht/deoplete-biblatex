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
    record = bibtexparser.customization.add_plaintext_fields(record)
    return record


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)

        self.filetypes = ['rst', 'markdown']
        self.mark = '[bib]'
        self.name = 'biblatex'

    @property
    def __bibliography(self):
        if self.__reload_bibfile_on_change:
            mtime = os.stat(self.__bib_file).st_mtime
            if mtime != self.__bib_file_mtime:
                self.__bib_file_mtime = mtime
                self.__read_bib_file()

        return self.__bibliography_cached

    def __read_bib_file(self):
        try:
            with open(self.__bib_file) as bf:
                parser = bibtexparser.bparser.BibTexParser(
                    ignore_nonstandard_types=False,
                )
                parser.customization = bibtexparser_customizations
                bibliography = bibtexparser.load(
                    bf,
                    parser=parser,
                ).entries_dict

                self.__bibliography_cached = bibliography
        except FileNotFoundError:
            self.vim.err_write(
                '[deoplete-biblatex] No such file: {0}\n'.format(
                    self.__bib_file,
                ),
            )

    def on_init(self, context):
        bib_file = context['vars'].get(
            'deoplete#sources#biblatex#bibfile',
            '~/bibliography.bib'
        )
        bib_file = os.path.abspath(os.path.expanduser(bib_file))

        self.__bib_file = bib_file
        self.__bib_file_mtime = os.stat(bib_file).st_mtime
        self.__read_bib_file()

        pattern_delimiter = context['vars'].get(
            'deoplete#sources#biblatex#delimiter',
            ',',
        )
        pattern_start = context['vars'].get(
            'deoplete#sources#biblatex#startpattern',
            r'\[(?:[\w,]+:)?',
        )
        pattern_completed = r'(?:@?\w+-\w+{})*'.format(pattern_delimiter)
        pattern_current = r'@?\w+$'

        self.__pattern = re.compile(
            pattern_start
            + pattern_completed
            + pattern_current
        )

        reload_bibfile_on_change = context['vars'].get(
            'deoplete#sources#biblatex#reloadbibfileonchange',
            0,
        )
        reload_bibfile_on_change = bool(reload_bibfile_on_change)

        self.__reload_bibfile_on_change = reload_bibfile_on_change

        add_info = context['vars'].get(
            'deoplete#sources#biblatex#addinfo',
            0,
        )
        add_info = bool(add_info)

        self.__add_info = add_info

    def __format_info(self, entry):
        return '{title}{author}{date}'.format(
            title=('Title: {}\n'.format(entry['plain_title'])
                   if 'plain_title' in entry else ''),
            author=(
                'Author{plural}: {author}\n'.format(
                    plural='s' if len(entry['author']) > 1 else '',
                    author='; '.join(entry['author']),
                )
                if 'author' in entry else ''
            ),
            date=('Year: {}\n'.format(entry['plain_date'].split('-')[0])
                  if 'plain_date' in entry else ''),
        )

    def __entry_to_candidate(self, entry):
        candidate = {
            'abbr': entry['ID'],
            'word': entry['ID'],
            'kind': entry['ENTRYTYPE'],
        }

        if self.__add_info:
            candidate['info'] = self.__format_info(entry)

        return candidate

    def gather_candidates(self, context):
        if self.__pattern.search(context['input']):
            candidates = [
                self.__entry_to_candidate(entry)
                for entry in self.__bibliography.values()
            ]
            return candidates
        else:
            return []
