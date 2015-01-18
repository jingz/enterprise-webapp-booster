#!venv/bin/python
import sys
import feedparser

url = sys.argv[1]
print 'fetching ...', url
d = feedparser.parse(url)
print d

for i, entry in enumerate(d['entries']):
    print i, entry['updated'], entry['title']
