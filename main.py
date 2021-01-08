"""Testing stuff out"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.parse
from http.client import InvalidURL
from urllib.error import HTTPError
import os

def convert_url_to_raw(url):
    try:
        print(url)
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode('utf-8')
        return html
    except:
        return "Failed"
    # except (UnicodeDecodeError, HTTPError, InvalidURL, UnboundLocalError) as e:
    #     return("Failed")


# def find_urls(raw, root_url, curr_url):
#     # try:
#     soup = BeautifulSoup(raw, 'html.parser')
#
#     list_of_urls = []
#
#     for element in soup.find_all("a"):
#         try:
#             if "?" not in element["href"] and "#" not in element["href"] and element['href'] != '/' \
#                     and 'http' not in element['href']:
#                 if element['href'][0] == '/':
#                     list_of_urls.append(root_url + element["href"][1:])
#                 elif element['href'][:2] == '..':
#                     print()  # Cannot get the recursive roots yet, but it will be fixed eventually.
#                 else:
#                     list_of_urls.append(curr_url + element["href"])
#         except:
#             print("something wrong with "+ curr_url)
#             return None
#     return list_of_urls


def better_find_urls(raw, root_url, curr_url):
    try:
        soup = BeautifulSoup(raw, 'html.parser')
        list_of_urls = []
        for element in soup.find_all("a"):
            link_destination = element["href"]
            # print(link_destination)
            if len(link_destination) <= 1 or '?' in link_destination or '#' in link_destination:
                continue
            if "http" in link_destination:
                continue
            if link_destination[:3] == "../":
                index2 = curr_url.rfind("/")
                index1 = curr_url[:-1].rfind("/")
                abs_link = curr_url[:index1] + link_destination[2:]
            elif link_destination[0] == "/":
                abs_link = root_url + link_destination[1:]
            else:
                abs_link = curr_url + link_destination
            list_of_urls.append(abs_link)
        return list_of_urls
    except:
        print("failed")
        return []
    finally:
        print("")

# def record_raw_data(url, raw):
#     # print(url)
#     url = url[len("https://www.teach.cs.toronto.edu/"):]
#     if "." in url:
#         # Save file
#         print("Attempt to save file")
#         try:
#             path = os.path.join('.', url)
#             f = open(path, 'a')
#             f.write(raw)
#             f.close()
#         except:
#             print("Unable to save")
#     else:
#         print("create directory based on last value in url.")
#         print("making directories for " + url)
#         path = os.path.join('.', url)
#         if not os.path.exists(path):
#             os.makedirs(path)
#
#     print(url)


def save_all_urls(set_of_urls):
    for url in set_of_urls:
        file_url = url[8:]
        check_local_url_path(file_url)
        if "." in file_url.split("/")[-1] and file_url.split("/")[-1] != "reveal.js":
            save_file(url, file_url)

def save_file(url, local_path):
    urllib.request.urlretrieve(url, local_path)
    # f = open(local_path, 'wb')
    # f.write()
def check_local_url_path(url):
    folders = url.split("/")
    if "." in folders[-1]:
        if folders[-1] == "reveal.js":
            # Exception, do not remove
            print("Special")
        else:
            # Is a file, do not include
            folders.remove(folders[-1])
    beginning_path = "."
    for folder in folders:
        beginning_path = os.path.join(beginning_path, folder)
        if not os.path.exists(beginning_path):
            os.makedirs(beginning_path)

if __name__ == "__main__":
    all_urls = set()
    processed_urls = set()
    root_url = "https://www.teach.cs.toronto.edu/"
    base_url = "https://www.teach.cs.toronto.edu/~csc110y/"
    all_urls.add(base_url)
    curr_url = base_url
    while len(all_urls) != len(processed_urls):
        curr_url = next(iter(all_urls - processed_urls))
        raw = convert_url_to_raw(curr_url)
        if raw != "Failed":
            list_of_urls = better_find_urls(raw, root_url, curr_url)
            processed_urls.add(curr_url)
            if list_of_urls is not None:
                all_urls.update(list_of_urls)
        else:
            all_urls.remove(curr_url)
    print(all_urls)

    save_all_urls(all_urls)
