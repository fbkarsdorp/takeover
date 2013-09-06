#!usr/bin/env python

import mechanize
import cookielib
import os
import re
import random
import sys
import time
from ConfigParser import SafeConfigParser

from lxml import html
from lxml.html.clean import clean_html
from lxml import etree

# regular expresssions:
semicolon = re.compile(r'\;')
p_htmltag = re.compile(r'(\<\/*p\>)+')
SUP_htmltag = re.compile(r'(\<\/*SUP\>)+')
page_span = re.compile(r'<span\s*class="page">\([0-9]+\s*of\s*[0-9]+\)</span><br\s*/>')
tags_around_actual_text = re.compile(r'[\s\S]+\<\!\-\-\/\.post\-rail\-\-\>\s+<p>([\s\S]+)\<\/div\>\<\!\-\-\/\.entry\-contents\-\-\>[\s\S]+')

def clean_page(page, lookupkey):
    page = page_span.sub(" ", p_htmltag.sub(" ", SUP_htmltag.sub(" ", tags_around_actual_text.sub(r"\1", page))))
    try:
        tree = html.fromstring(page)
        tree = clean_html(tree)
    except etree.XMLSyntaxError:
        print "We had an XMLSyntaxError in:", lookupkey
        return page
    return tree.text_content()

def _make_url(url_prefix, url_suffix):
    def make_url(lookupkey, counter=1):
        print '%s%s-%s%s' % (url_prefix, lookupkey, counter, url_suffix
        return '%s%s-%s%s' % (url_prefix, lookupkey, counter, url_suffix)
    return make_url    

def next_page(lookupkey, counter, page):
    return '%s-%s,00.html" title="%s" class="page">%s' % (
        lookupkey, counter, counter, counter) in page

def make_browser(root_url, username, password):
    browser = mechanize.Browser()
    browser.set_cookiejar(cookielib.LWPCookieJar())

    browser.set_handle_equiv(True)
    browser.set_handle_gzip(True)
    browser.set_handle_redirect(True)
    browser.set_handle_referer(True)
    browser.set_handle_robots(False)

    browser.set_handle_refresh(mechanize.HTTPRefreshProcessor(), max_time=1)
    browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    browser.open(root_url)
    browser.select_form(nr=1)
    
    browser.set_all_readonly(False)
    browser.form['turl'] = root_url
    browser.form['rurl'] = root_url
    browser.form['username'] = username
    browser.form['password'] = password
    browser.submit()
    return browser

def fetch_page(lookupkey, browser, counter=1):
    url = make_url(lookupkey, counter)
    response = browser.open(url).read()
    return [response] + (fetch_page(lookupkey, browser, counter+1) if next_page(lookupkey, counter+1, response) else [])

if __name__ == "__main__":
    config = SafeConfigParser()
    config.read(sys.argv[1])
    url_prefix = config.get('urls', 'login-url-prefix')
    url_suffix = config.get('urls', 'url-suffix')
    make_url = _make_url(url_prefix, url_suffix)
    decade = config.get('options', 'decade')    
    print "Scraping started..."
    # load the lookupkeys for the decade-file specified
    with open("../lookupkeys/" + decade + ".csv") as inf:
        lines = inf.readlines()
    print "Attempting to extract "+str(len(lines))+" texts from decade..."
    # mkdirs, if nessecary
    if not os.path.isdir("../texts"):
        os.mkdir("../texts")
    if not os.path.isdir("../texts/" + decade):
        os.mkdir("../texts/" + decade)
    # make only one browser instance
    browser = make_browser(config.get('urls', 'root-url'), 
                           config.get('credentials', 'username'), 
                           config.get('credentials', 'password'))
    # iterate over texts in the decade
    for i in range(1,len(lines)):
        line = lines[i].strip()
        # check the cells
        data_items = semicolon.split(line)
        if len(data_items) != 7:
            continue
        # extract loopupkey
        lookupkey = str(data_items[0])
        text = ' '.join(clean_page(page, lookupkey) for page in fetch_page(lookupkey, browser))
        with open("../texts/" + decade + "/" + lookupkey + ".txt", 'w') as out:
            out.write(text.encode("utf8"))
        time.sleep(random.randint(1,int(config.getint('options', 'maximum-wait-interval'))))
    print "Scraping terminated..."

