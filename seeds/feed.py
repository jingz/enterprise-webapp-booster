#!/usr/bin/env python
from env import app_main, db, m
with app_main.app_context():
    # feed_urls = (
    #  'http://www.dailynews.co.th/rss/news_agriculture.xml',
    #  'http://www.posttoday.com/rss/src/politics.xml',
    #  'http://www.posttoday.com/rss/src/lifestyle.xml',
    #  'http://www.posttoday.com/rss/src/social.xml',
    #  'http://www.posttoday.com/rss/src/analyse.xml',
    #  'http://www.posttoday.com/rss/src/breakingnews.xml',
    #  'http://www.posttoday.com/rss/src/crime.xml',
    #  'http://www.posttoday.com/rss/src/district.xml',
    #  'http://www.posttoday.com/rss/src/sport.xml',
    #  'http://www.posttoday.com/rss/src/world.xml',
    #  'http://www.posttoday.com/rss/src/moneyguide.xml',
    #  'http://www.posttoday.com/rss/src/business.xml',
    #  'http://www.posttoday.com/rss/src/homecondo.xml',
    #  'http://www.posttoday.com/rss/src/eattravel.xml',
    #  'http://www.posttoday.com/rss/src/digitallife.xml',
    #  'http://www.posttoday.com/rss/src/mindsoul.xml',
    #  'http://www.posttoday.com/rss/src/motor.xml',
    #  'http://www.posttoday.com/rss/src/entertainment.xml',
    #  'http://www.posttoday.com/rss/src/blogs.xml',
    #  'http://www.posttoday.com/rss/src/learning.xml')

    feed_urls = (
            'http://www.dailynews.co.th/rss/news_royal.xml',
            'http://www.dailynews.co.th/rss/popular.xml',
            'http://www.dailynews.co.th/rss/news_politics.xml',
            'http://www.dailynews.co.th/rss/news_crime.xml',
            'http://www.dailynews.co.th/rss/news_world.xml',
            'http://www.dailynews.co.th/rss/news_sport.xml',
            'http://www.dailynews.co.th/rss/news_technology.xml',
            'http://www.dailynews.co.th/rss/news_entertainment.xml',
            'http://www.dailynews.co.th/rss/news_business.xml',
            'http://www.dailynews.co.th/rss/news_society.xml',
            'http://www.dailynews.co.th/rss/news_education.xml',

            'http://www.khaosod.co.th/rss/urgent_news.xml',
            'http://www.khaosod.co.th/rss/wikipedia_news.xml',
            'http://www.khaosod.co.th/rss/entertainment_news.xml',
            'http://www.khaosod.co.th/rss/sport_news.xml',
            'http://www.khaosod.co.th/rss/every-direction_news.xml',
            'http://www.khaosod.co.th/rss/column_online_news.xml',
            'http://www.khaosod.co.th/rss/monitor_news.xml',
            'http://www.khaosod.co.th/rss/firstpage_news.xml',
            'http://www.khaosod.co.th/rss/articles_news.xml',
            'http://www.khaosod.co.th/rss/sports_news.xml',
            'http://www.khaosod.co.th/rss/entertain_news.xml',
            'http://www.khaosod.co.th/rss/politics_news.xml',
            'http://www.khaosod.co.th/rss/foreign_news.xml',
            'http://www.khaosod.co.th/rss/economy_news.xml',
            'http://www.khaosod.co.th/rss/marketing_news.xml',
            'http://www.khaosod.co.th/rss/youth_news.xml',
            'http://www.khaosod.co.th/rss/women_news.xml',
            'http://www.khaosod.co.th/rss/education_news.xml',
            'http://www.khaosod.co.th/rss/ratjapat_news.xml',
            'http://www.khaosod.co.th/rss/amulet_news.xml',
            'http://www.khaosod.co.th/rss/regional_news.xml',
            'http://www.khaosod.co.th/rss/misc_news.xml',
            'http://www.khaosod.co.th/rss/bkk_news.xml',
            'http://www.khaosod.co.th/rss/hunsa_news.xml',
            'http://www.khaosod.co.th/rss/motor_news.xml',
            'http://www.khaosod.co.th/rss/social_news.xml',
            'http://www.khaosod.co.th/rss/shotnews_news.xml',
            'http://www.khaosod.co.th/rss/technology_news.xml',
            'http://www.khaosod.co.th/rss/horoscope_news.xml',

            'http://www.bangkokbiznews.com/home/services/rss/home.xml',
            'http://www.bangkokbiznews.com/home/services/rss/politics.xml',
            'http://www.bangkokbiznews.com/home/services/rss/business.xml',
            'http://www.bangkokbiznews.com/home/services/rss/finance.xml',
            'http://www.bangkokbiznews.com/home/services/rss/property.xml',
            'http://www.bangkokbiznews.com/home/services/rss/auto-mobile.xml',
            'http://www.bangkokbiznews.com/home/services/rss/it.xml',
            'http://www.bangkokbiznews.com/home/services/rss/life-style.xml',
            'http://www.bangkokbiznews.com/home/services/rss/video.xml',
            'http://www.bangkokbiznews.com/home/services/rss/audio.xml',

            'http://www.manager.co.th/RSS/Home/Breakingnews.xml',
            'http://www.manager.co.th/RSS/Interview/Interview.xml',
            'http://www.manager.co.th/RSS/Politics/Politics.xml',
            'http://www.manager.co.th/RSS/Crime/Crime.xml',
            'http://www.manager.co.th/RSS/QOL/QOL.xml',
            'http://www.manager.co.th/RSS/Local/Local.xml',
            'http://www.manager.co.th/RSS/Around/Around.xml',
            'http://www.manager.co.th/RSS/IndoChina/IndoChina.xml',
            'http://www.manager.co.th/RSS/China/China.xml',
            'http://www.manager.co.th/RSS/Business/Business.xml',
            'http://www.manager.co.th/RSS/iBizChannel/iBizChannel.xm',
            'http://www.manager.co.th/RSS/StockMarket/StockMarket.xml',
            'http://www.manager.co.th/RSS/MutualFund/MutualFund.xml',
            'http://www.manager.co.th/RSS/SMEs/SMEs.xml',
            'http://www.manager.co.th/RSS/Motoring/Motoring.xml',
            'http://www.manager.co.th/RSS/Cyberbiz/Cyberbiz.xml',
            'http://www.manager.co.th/RSS/CBizReview/CBizReview.xml',
            'http://www.manager.co.th/RSS/Telecom/Telecom.xml',
            'http://www.manager.co.th/RSS/Science/Science.xml',
            'http://www.manager.co.th/RSS/Game/Game.xml',
            'http://www.manager.co.th/RSS/Sport/Sport.xml',
            'http://www.manager.co.th/RSS/Entertainment/Entertainment.xml',
            'http://www.manager.co.th/RSS/Campus/Campus.xml',
            'http://www.manager.co.th/RSS/Celeb/Celeb.xml',
            'http://www.manager.co.th/RSS/Family/Family.xml',
            'http://www.manager.co.th/RSS/Lady/Lady.xml',
            'http://www.manager.co.th/RSS/Travel/Travel.xml',
            'http://www.manager.co.th/RSS/Pjkkuan/Pjkkuan.x',

             'http://www.prachachat.net/rss/article_news.xml',
             'http://www.prachachat.net/rss/breakingnews.xml',
             'http://www.prachachat.net/rss/worldnews.xml',
             'http://www.prachachat.net/rss/stock_finance.xml',
             'http://www.prachachat.net/rss/property.xml',
             'http://www.prachachat.net/rss/marketing.xml',
             'http://www.prachachat.net/rss/motoring.xml',
             'http://www.prachachat.net/rss/it.xml',
             'http://www.prachachat.net/rss/column.xml',
             'http://www.prachachat.net/rss/dlife.xml',
             'http://www.prachachat.net/rss/csr.xml',
             'http://www.prachachat.net/rss/politic.xml',
             'http://www.prachachat.net/rss/localeconomy.xml',
             'http://www.prachachat.net/rss/travel.xml',
             'http://www.prachachat.net/rss/aec.xml',
             'http://www.prachachat.net/rss/square.xml',
             'http://www.prachachat.net/rss/economy.xml',
             'http://www.prachachat.net/rss/gallery.xml',

            'http://www.siamturakij.com/main/news_list.php?cid=1',
            'http://www.siamturakij.com/main/news_list.php?cid=2',
            'http://www.siamturakij.com/main/news_list.php?cid=3',
            'http://www.siamturakij.com/main/news_list.php?cid=4',
            'http://www.siamturakij.com/main/news_list.php?cid=8',
            'http://www.siamturakij.com/main/news_list.php?cid=6',
            'http://www.siamturakij.com/main/news_list.php?cid=9',
            'http://www.siamturakij.com/main/news_list.php?cid=10',
            'http://www.siamturakij.com/main/news_list.php?cid=13',
            'http://www.siamturakij.com/main/news_list.php?cid=12',
            'http://www.siamturakij.com/main/news_list.php?cid=25',
            'http://www.siamturakij.com/main/news_list.php?cid=26',
            'http://www.siamturakij.com/main/news_list.php?cid=27',
            'http://www.siamturakij.com/main/news_list.php?cid=28',
            'http://www.siamturakij.com/main/news_list.php?cid=14',
            'http://www.siamturakij.com/main/news_list.php?cid=15',
            'http://www.siamturakij.com/main/news_list.php?cid=16',
            'http://www.siamturakij.com/main/news_list.php?cid=29',
            'http://www.siamturakij.com/main/news_list.php?cid=30',
            'http://www.siamturakij.com/main/news_list.php?cid=31',
            )
    
    feed_urls = (
            'http://www.komchadluek.net/rss/news_widget.xml',
            'http://www.komchadluek.net/rss/politic.xml',
            'http://www.komchadluek.net/rss/entertainment.xml',
            'http://www.komchadluek.net/rss/crime.xml',
            'http://www.komchadluek.net/rss/sport.xml',
            'http://www.komchadluek.net/rss/lifestyle.xml',
            'http://www.komchadluek.net/rss/drink-eat-travel.xml',
            'http://www.komchadluek.net/rss/agriculture.xml',
            'http://www.komchadluek.net/rss/foreign.xml',
            'http://www.komchadluek.net/rss/amulet.xml',
            'http://www.komchadluek.net/rss/horoscope.xml',
            'http://www.komchadluek.net/rss/local.xml',
            'http://www.komchadluek.net/rss/unclecham.xml',
            'http://www.komchadluek.net/rss/economic.xml',
            'http://www.komchadluek.net/rss/homecar.xml',
            'http://www.komchadluek.net/rss/scienceit.xml',
            'http://www.komchadluek.net/rss/artculture.xml',
            'http://www.komchadluek.net/rss/education.xml',
           )
    for url in feed_urls:
        u = m.Feed(url=url, name=url, etag='', status=None)
        db.session.add(u)
    db.session.commit()
