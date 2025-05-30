import urllib.request
import urllib.error
import urllib.parse # Added for urljoin

from bs4 import BeautifulSoup
import os

already_visited = set()
yet_to_visit = []

# The domain name, without the trailing '/', eg:
# '[http|https]://the-domain-to-index.[com|....]'
domain = ''
# Initialize yet_to_visit after domain is defined if it's used as the first item.
# or ensure domain is set before the main loop starts if it's populated from elsewhere.
# For now, let's assume domain will be set before crawling starts.
# yet_to_visit.append(domain) # This will add an empty string if domain is not set.

keep_it_moving = True
debug = True

dir_name = 'pages_to_index/'


def get_anchor_tag(doc):
    soup = BeautifulSoup(doc, 'html.parser')
    links = []
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        if href is not None: # Only add if href exists
            links.append(href) # Store as string, no encoding here.
    return links


def get_proper_link(cur_link, anchor_link):
    global domain

    # Check if anchor_link is an absolute URL
    if anchor_link.startswith("http://") or anchor_link.startswith("https://"):
        return anchor_link
    # Check if anchor_link is an absolute path
    elif anchor_link.startswith("/"):
        # Join with the base domain
        return urllib.parse.urljoin(domain, anchor_link)
    # Handle relative paths
    else:
        # Join with the current link (which acts as the base URL)
        return urllib.parse.urljoin(cur_link, anchor_link)


if __name__ == '__main__':

    if not os.path.exists(dir_name):
        # Directory does not exists, to store the web page. Create one.
        os.makedirs(dir_name)

        if debug:
            print('%s does not exists, Creating one' % dir_name)

    print('main')
    while keep_it_moving:
        # print('Looping')
        if not yet_to_visit: # Check if list is empty before popping
            print('Yet to visit is empty. Stopping.')
            keep_it_moving = False
            break
        cur = yet_to_visit.pop(0)

        if (domain in cur) and (cur not in already_visited): # Ensure domain is part of cur
            print('Hitting', cur)
            try:
                request = urllib.request.Request(cur)
                response = urllib.request.urlopen(request)

                # read web page.
                data_got = response.read() # This will be bytes
            except urllib.error.HTTPError as e:
                print('Cannot connect %s. HTTPError: %s' % (cur, e.code))
                continue
            except urllib.error.URLError as e:
                print('Cannot connect %s. URLError: %s' % (cur, e.reason))
                continue


            fname = cur.replace(':', '+').replace('/', '-')

            # write to file.
            # Since data_got is bytes, open file in binary write mode.
            try:
                with open(dir_name + fname, 'wb') as f:
                    f.write(data_got)
            except IOError as e:
                print("Error writing file %s: %s" % (fname, e))
                continue


            # BeautifulSoup can handle bytes, it will try to decode it.
            # Or decode explicitly: data_got.decode('utf-8', errors='replace')
            temp_links = get_anchor_tag(data_got)

            next_links = []

            for link in temp_links:
                # Ensure link is not None before processing
                if link:
                    proper_link = get_proper_link(cur, link)
                    if proper_link: # Ensure get_proper_link didn't return None
                       next_links.append(proper_link)


            print('New links are', next_links)

            for link in next_links:
                if link not in already_visited and link not in yet_to_visit: # Avoid duplicates in yet_to_visit
                    yet_to_visit.append(link)

            # yet_to_visit.extend(next_links) # This could add duplicates if not checked
            already_visited.add(cur)

            if len(yet_to_visit) == 0:
                keep_it_moving = False
                print('Done crawling.')
