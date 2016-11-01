from django.shortcuts import render
import feedparser


def feed_view(request):

    feed = feedparser.parse('https://www.uwb.edu/news?rss=blogs')
    entries = feed['entries']
    context = {
        'feed': feed,
        'entries': entries,
    }
    return render(request, 'rss_feed/view.html', feed)
