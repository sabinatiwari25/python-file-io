#! /usr/bin/env python3

import sys
import re

def find_iter(in_stream, target_regex,
        start_regex = None,
        stop_regex = None):
    """
    Iterates over all matches of `target_regex` found in `in_stream`.

    Parameters
    ----------
    in_stream : A file object (or any iterable of strings)
        The input stream to be searched for `target_regex`.

    target_regex : A regular expression object
        The target pattern to be found in `in_stream`.

    start_regex : None or a regular expression object
        A pattern that must be matched within `in_stream` before searching for
        `target_regex` begins. Searching for `target_regex` will begin on the
        line AFTER `start_regex` is found. If `None`, searching begins at the
        first line.

    stop_regex : None or a regular expression object
        If this pattern is found within `in_stream` the search for
        `target_regex` stops early (before the end of the stream).  The line
        containing `stop_regex` is NOT searched for `target_regex`.  If `None`,
        searching continues to the end of `in_stream`.
        

    Yields
    ------
    A tuple of the line index and the match object

        Each time `target_regex` is found within `in_stream`, a tuple is
        yielded that contains (1) the index of the line on which it was found
        and (2) the regular expression match object.
    """
    search_has_started = False
    if not start_regex:
        search_has_started = True
    for line_index, line in enumerate(in_stream):
        if stop_regex and stop_regex.match(line):
            break
        if start_regex and (not search_has_started):
            if start_regex.match(line):
                search_has_started = True
            continue
        for match_object in target_regex.finditer(line):
            yield line_index, match_object
