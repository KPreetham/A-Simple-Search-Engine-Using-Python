import glob
import webbrowser
from Tkinter import Tk, Entry, Button
from collections import Counter

# Get all the crawled files.
import re

file_list = glob.glob('pages_to_index/*')

# Holds word, {count, url}
big_table = {}

glob_text = None
debug = True


def parse_document(document):
    """
    Parse the document, return the small table.
    :param document:
    :return:
    """
    words = re.sub("[^\w]", ' ', document).split()

    return Counter(words)


def generate_html_files(url_list):
    f = open('result.html', 'w')

    f.write("<html>")
    f.write("<title>Search Result</title>\n")
    f.write("<body>\n")

    f.write("<h1>The Web Spider Search Engine</h1>")
    f.write(
        "<img src='webspider.jpg' width='100' height = '100' align='middle' />")

    f.write("<br/> <br/>")
    for item in url_list:
        link = item[0]
        link = link.replace('final\\', '').replace('+', ':').replace('-', '/')

        f.write("<a href='%s'>%s</a>\n" % (link, link))
        f.write("<br/>")

    f.write("</body>\n")
    f.write("</html>")
    f.close()

    webbrowser.open_new_tab('result.html')
    print 'Done'


def perform_custom_search(search_query):
    global debug

    # Get each word.
    search_words = search_query.split()

    rank_list = {}

    for word in search_words:
        # Get all the sites which has these words.
        try:
            url_hit_list = big_table[word]
        except KeyError:
            print word, ' not found in index'
            continue

        # for each url in the url_hit_list, increase its hit count by one.
        for item in url_hit_list:
            try:
                rank_list[item[0]] += 1
            except KeyError:
                rank_list[item[0]] = 1

    print 'rank list'

    # Sort the rank list by its count.
    sort_list = sorted(rank_list.items(), key=lambda x: x[1])

    total_result = len(sort_list)

    print '%d matches found' % total_result

    if total_result == 0:
        print 'No result found at all.'

    res_to_show = 20

    if total_result < res_to_show:
        res_to_show = total_result

    sort_list = sort_list[::-1]

    print 'Top results'
    for i in range(res_to_show):
        print sort_list[i]

    # Show only res_to_show results. Limited result.
    generate_html_files(sort_list[:res_to_show])


def start_search():
    global glob_text
    perform_custom_search(glob_text.get())


def add_to_big_table(small_table):
    """
    Add small table to big table.
    :param small_table: A dictionary
    :return: None
    """
    global big_table

    for key, value in small_table.iteritems():
        try:
            big_table[key].append(value)
        except KeyError:
            big_table[key] = []
            big_table[key].append(value)


def create_small_table(word_counter, url):
    s_table = {}

    for k, v in word_counter.iteritems():
        s_table[k] = [url, v]

    return s_table


if __name__ == '__main__':
    for inp_file in file_list:
        with open(inp_file) as f:
            document = f.read()

        # Get the table which contains words, count
        w_counter = parse_document(document)

        # Create a table [word, [url, count]]
        small_table = create_small_table(w_counter, inp_file)

        add_to_big_table(small_table)

    print 'Done indexing'
    print 'Indexed', len(file_list), 'files.'

    # UI comes here

    root = Tk()
    root.maxsize(640, 480)
    root.minsize(640, 480)

    e = Entry(root, width=100)
    e.pack()

    glob_text = e

    b = Button(root, text="Search", command=start_search)
    b.pack()

    root.mainloop()
