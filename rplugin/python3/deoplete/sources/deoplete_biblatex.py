#!/usr/bin/env
# Standard Library
import os
import re

# Third Party
import bibtexparser

# This Module
from deoplete.logger import getLogger
from deoplete.util import load_external_module

# Local Folder
from .base import Base

load_external_module(__file__, "sources/deoplete_biblatex")

logger = getLogger(__name__)


# MY_CODES = {"lion:": "test", "tandem:": "test"}


class CustomizationError(Exception):
    pass


def bibtexparser_customizations(record):
    record = bibtexparser.customization.author(record)
    record = bibtexparser.customization.editor(record)
    try:
        record = bibtexparser.customization.add_plaintext_fields(record)
    except AttributeError:
        logger.debug(
            (
                "Could add plaintext fields for record with ID: {}. "
                "This will be ignored."
            ).format(record["ID"])
        )
        pass

    return record


BIBTEXPARSER_BOOL_OPTIONS = {
    "common_strings",
    "add_missing_from_crossref",
    "interpolate_strings",
    "homogenize_fields",
    "ignore_nonstandard_types",
}

BIBTEXPARSER_DEFAULTS_KWARGS = {
    "ignore_nonstandard_types": False,
    "common_strings": True,
}


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)

        self.filetypes = ["rst", "markdown"]
        self.mark = "[bib]"
        self.name = "biblatex"

        self.parser_kwargs = BIBTEXPARSER_DEFAULTS_KWARGS.copy()
        self.options = {}

    @property
    def __bibliography(self):
        if self.options["reload_bibfile_on_change"]:
            mtime = os.stat(self.__bib_file).st_mtime

            if mtime != self.__bib_file_mtime:
                self.__bib_file_mtime = mtime
                self.__read_bib_file()

        return self.__bibliography_cached

    def __read_bib_file(self):
        try:
            with open(self.__bib_file) as bf:
                parser = bibtexparser.bparser.BibTexParser(**self.parser_kwargs)
                parser.customization = bibtexparser_customizations
                bibliography = bibtexparser.load(bf, parser=parser).entries_dict

                self.__bibliography_cached = bibliography
        except FileNotFoundError:
            self.vim.err_write(
                "[deoplete-biblatex] No such file: {0}\n".format(self.__bib_file)
            )

    def on_init(self, context):
        bib_file = context["vars"].get(
            "deoplete#sources#biblatex#bibfile", "~/bibliography.bib"
        )
        bib_file = os.path.abspath(os.path.expanduser(bib_file))

        custom_parser_kwargs = {
            opt: context["vars"].get("deoplete#sources#biblatex#{}".format(opt), None)
            for opt in BIBTEXPARSER_BOOL_OPTIONS
        }
        custom_parser_kwargs = {
            k: bool(v) for k, v in custom_parser_kwargs.items() if v is not None
        }
        self.parser_kwargs.update(custom_parser_kwargs)

        self.__bib_file = bib_file
        self.__bib_file_mtime = os.stat(bib_file).st_mtime
        self.__read_bib_file()

        pattern_delimiter = context["vars"].get(
            "deoplete#sources#biblatex#delimiter", ","
        )
        pattern_start = context["vars"].get(
            "deoplete#sources#biblatex#startpattern", r"\[(?:[\w,]+:)?"
        )
        pattern_key = context["vars"].get(
            "deoplete#sources#biblatex#keypattern", r"@?[\w-]+"
        )

        pattern_current = r"{}$".format(pattern_key)
        pattern_completed = r"(?:{}{})*".format(pattern_key, pattern_delimiter)

        self.__pattern = re.compile(pattern_start + pattern_completed + pattern_current)

        self.__get_bool_options(context, ["reload_bibfile_on_change", "add_info"])

    def __get_bool_options(self, context, options):
        """
        Get boolean options from the configuration and store them in the format "__<option>"
        In the configuration they should be given without the underscores.
        """

        for opt in options:
            value = context["vars"].get(
                "deoplete#sources#biblatex#{}".format(opt.replace("_", "")), 0
            )
            value = bool(value)
            self.options[opt] = value

    def __format_info(self, entry):
        return "{title}{author}{date}".format(
            title=(
                "Title: {}\n".format(entry["plain_title"])
                if "plain_title" in entry
                else ""
            ),
            author=(
                "Author{plural}: {author}\n".format(
                    plural="s" if len(entry["author"]) > 1 else "",
                    author="; ".join(entry["author"]),
                )
                if "author" in entry
                else ""
            ),
            date=(
                "Year: {}\n".format(entry["plain_date"].split("-")[0])
                if "plain_date" in entry
                else ""
            ),
        )

    def __entry_to_candidate(self, entry):
        candidate = {
            "abbr": entry["ID"],
            "word": entry["ID"],
            "kind": entry["ENTRYTYPE"],
        }

        if self.options["add_info"]:
            candidate["info"] = self.__format_info(entry)

        return candidate

    def gather_candidates(self, context):
        if self.__pattern.search(context["input"]):
            candidates = [
                self.__entry_to_candidate(entry)
                for entry in self.__bibliography.values()
            ]

            return candidates
        else:
            return []
