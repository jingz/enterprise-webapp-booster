#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pythai
from app.models import db, Feed, FeedEntries

def run():
    feeds = FeedEntries.today()
    for f in feeds:
        print f.title
