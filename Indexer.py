import glob
import webbrowser
from tkinter import Tk, Entry, Button # Changed Tkinter to tkinter
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
    # Convert to lowercase first, then substitute non-alphanumeric (keeps underscore) and split
    # If underscore should also be removed, use [^\w_] as part of the non-alphanumeric set,
    # or a more specific regex for "words".
    # For now, assuming words can contain underscores as per \w.
    # The prompt implies "hello" from "Hello", so lowercasing is key.
    words = re.sub(r"[^\w\s]", '', document.lower()) # Remove punctuation, keep spaces for splitting
    word_list = words.split() # Split by whitespace

    return Counter(word_list)


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
    print('Done') # Changed to print()


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
            print(word, ' not found in index') # Changed to print()
            continue

        # for each url in the url_hit_list, increase its hit count by one.
        for item in url_hit_list:
            try:
                rank_list[item[0]] += 1
            except KeyError:
                rank_list[item[0]] = 1

    print('rank list') # Changed to print()

    # Sort the rank list by its count.
    sort_list = sorted(rank_list.items(), key=lambda x: x[1])

    total_result = len(sort_list)

    print('%d matches found' % total_result) # Changed to print()

    if total_result == 0:
        print('No result found at all.') # Changed to print()

    res_to_show = 20

    if total_result < res_to_show:
        res_to_show = total_result

    sort_list = sort_list[::-1]

    print('Top results') # Changed to print()
    for i in range(res_to_show):
        print(sort_list[i]) # Changed to print()

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

    for key, value in small_table.items(): # Changed iteritems to items
        try:
            big_table[key].append(value)
        except KeyError:
            big_table[key] = []
            big_table[key].append(value)


def create_small_table(word_counter, url):
    s_table = {}

    for k, v in word_counter.items(): # Changed iteritems to items
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

    print('Done indexing') # Changed to print()
    print('Indexed', len(file_list), 'files.') # Changed to print()

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
