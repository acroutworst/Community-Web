from django.shortcuts import render
import feedparser


def feed_view(request):

    feed = feedparser.parse('https://www.uwb.edu/news?rss=blogs')
    entries = feed.entries
    num_entries = 5
    context = {
        'feed': feed,
        'entries': entries,
        'num_entries': num_entries,
    }
    return render(request, 'rss_feed/view.html', feed)
