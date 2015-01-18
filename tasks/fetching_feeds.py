#!/usr/bin/env python
from app.models import db, Feed, FeedEntries
from pprint import pprint as pp
import feedparser
import sys

def run():
    cnt = 0 # added entry counter
    feeds = Feed.query.filter('is_skip is not true').all()
    cached_titles = []
    for feed in feeds:
        url = feed.url
        d = feedparser.parse(url, etag=feed.etag, modified=feed.last_modified)
        if 'status' in d:
            feed.status = d.status
            print d.status, feed.url
            if d.status == 200:
                new_etag =  getattr(d, 'etag', '')
                lm =  getattr(feed, 'updated', None)

                # remember new etag and last modified from feed
                feed.status = d.status
                feed.etag = new_etag
                feed.last_modified = getattr(d.feed, 'updated', None)
                # print 'modified at :', feed.last_modified
                
                db.session.add(feed)

                etag_supported = bool(feed.etag)

                for entry in d.entries:
                   item_id = getattr(entry, 'id', '')
                   
                   if item_id and not etag_supported:
                       # check unique item
                       uitem = FeedEntries.query.filter_by(item_id=item_id).first()
                       if uitem: continue
                    
                   dup_entry = FeedEntries.query.filter_by(title=entry.title).first()
                   if dup_entry: continue

                   link = getattr(entry, 'link', None)
                   title = getattr(entry, 'title', None)
                   if not title or not link: continue
                   # create feed entries
                   fe = FeedEntries(item_id=item_id,
                                    feed_id=feed.id,
                                    title=entry.title,
                                    link=link,
                                    summary=entry.summary,
                                    published=entry.published,
                                    updated=entry.updated) 

                   if entry.title not in cached_titles:
                       cached_titles.append(entry.title)
                       print "--> [add]", entry.title
                       db.session.add(fe)
                       cnt += 1
                # check entry id for cached item
                # since fetched feed server may not implement etag or if-modified-since

            # update at least status
            db.session.add(feed);

    # print db.session.dirty
    db.session.commit();
    print "================================================ "
    print "total added", cnt
