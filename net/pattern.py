#!/bin/python3

#> Imports
import re
#</Imports

#> Header >/
link_pattern = re.compile(
    # examples will use https://raw.githubusercontent.com:443/Tiger-Tom/ShaeLib/main/net/__init__.py?query=test#anchor
    # the full match for each section will be in [] following its explanation
    # the specific group for each section will be in {}, if it differs from the full match
    r'(?P<protocol>\w+):\/\/'                 # protocol (http[s], etc) and protocol-sep (://) [https://] {https}
    r'(?P<location>'                          # begin "location" block-group [raw.githubusercontent.com:443]
        r'(?:(?P<subdomains>[\w\d\-\.]+)\.)?' # subdomain(s) joined by '.' [raw.] {raw}
        r'(?P<domain>[\w\d\-]+)'              # domain [githubusercontent]
        r'\.(?P<topdomain>[\w\d\-]+)'         # top-level domain [.com] {com}
        r'(?::(?P<port>\d+))?)'               # port [:443] {443} and end "location" block-group
    r'(?P<path>\/'                            # begin "path" block-group [/Tiger-Tom/ShaeLib/main/net/__init__.py]
        r'(?P<directory>[\w\d\-/]*\/)?'       # the directory component of the path [/Tiger-Tom/ShaeLib/main/net/
        r'(?:(?P<file>'                       # begin "file" block-group [__init__.py]
            r'(?P<name>[\w\d\-\.]*?[\w\d\-])' # the name component of the file [__init__]
            r'(?:\.(?P<suff>[\w\d\-]+))?)?'   # the suffix component of the file [.py] {py}
    r'(?=[^\w\d\-\/]|$)))?'                   # right boundary of paths and end "file" block-group and end "path" block-group
    r'(?:\?(?P<query>[\w\d\-&=]+))?'          # the query-string component [?query=test] {query=test}
    r'(?:#(?P<anchor>[\w\d\-]+))?'            # the anchor/hash-string component [#anchor] {anchor}
, re.MULTILINE)

link_search_pattern = re.compile(
    fr'(?:^|[^\w])('                          # left boundary of the link (BOL or non-protocol char)
    fr'{link_pattern.pattern}'                # embed link_pattern
    r')(?:[^\w\d\-/]|$)'                      # right boundary of the link (EOL or non-link char)
, re.MULTILINE)
