#!usr/local/env python
import sys
import feedparser

fname = ("./%s" % sys.argv[1])
d = feedparser.parse(fname)

for i, entry in enumerate(d['entries']):
    print i, entry['updated'], entry['title']
