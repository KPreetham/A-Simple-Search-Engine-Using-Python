import urllib2

from sets import Set
from bs4 import BeautifulSoup
import os

already_visited = Set()
yet_to_visit = []

domain = ''     # The domain name, without the trailing '/', eg: '[http|https]://the-domain-to-index.[com|....]'
yet_to_visit.append(domain)

keep_it_moving = True
debug = True

dir_name = 'pages_to_index/'


def get_anchor_tag(doc):
    soup = BeautifulSoup(doc, 'html.parser')

    try:
        n_link = [a_tag.get('href').encode('utf-8') for a_tag in soup.find_all('a')]
    except AttributeError:
        return []

    return n_link


def get_proper_link(cur_link, anchor_link):
    if anchor_link.startswith("http"):
        return anchor_link
    elif anchor_link.startswith("/"):
        return "http://textfiles.com" + anchor_link
    else:
        if cur_link.endswith(".html"):
            # replace mode
            items = cur_link.split('/')
            items[-1] = anchor_link
            items = '/'.join(items)
            return items
        else:
            return cur_link + '/' + anchor_link


if __name__ == '__main__':

    if not os.path.exists(dir_name):
        # Directory does not exists, to store the web page. Create one.
        os.makedirs(dir_name)

        if debug:
            print '%s does not exists, Creating one' % dir_name

    print 'main'
    while keep_it_moving:
        # print 'Looping'
        cur = yet_to_visit.pop(0)

        if (domain in cur) and (cur not in already_visited):
            print 'Hitting', cur
            try:
                request = urllib2.Request(cur)
                response = urllib2.urlopen(request)

                # read web page.
                data_got = response.read()
            except urllib2.HTTPError:
                print 'Cannot connect', cur
                continue

            fname = cur.replace(':', '+').replace('/', '-')

            # write to file.
            f = open(dir_name + fname, 'w')
            f.write(data_got)
            f.close()

            temp_links = get_anchor_tag(data_got)

            next_links = []

            for link in temp_links:
                next_links.append(get_proper_link(cur, link))

            print 'New links are', next_links

            for link in next_links:
                if link not in already_visited:
                    yet_to_visit.append(link)

            # yet_to_visit.extend(next_links)
            already_visited.add(cur)

            if len(yet_to_visit) == 0:
                keep_it_moving = False
                print 'Done crawling.'
