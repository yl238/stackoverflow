import os
import re
import xml.etree.ElementTree as ET
import json
from pathlib import Path
from bs4 import BeautifulSoup

def sanitise_xml(s):
    """
    Use BeautifulSoup to extract all text within HTML/XML tags, except those in <code> blocks.
    Remove the line breaks, replace unicode character for space
    
    Parameters
    ----------
    s - UTF-8 string
    
    Returns
    -------
    Cleaned up string    
    """
    soup = BeautifulSoup(s, 'lxml')
    for tag in soup.find_all('code'):
        tag.replace_with('')
        
    return soup.get_text().replace('\n', '').replace('\xa0', ' ')


def preprocess_text(data):
    """
    Clean the text body of the question/answers by removing HTML tags and <code> blocks,
    and split the Tags into a list.
    
    Parameter
    ---------
    data - dictionary, data extracted from an XML line using ElementTree
    
    Returns
    -------
    Processed dictionary
    """
    if 'Body' in data:
        data['Body'] = sanitise_xml(data['Body'])
    
    if 'Tags' in data:
        data['Tags'] = re.findall('\<([^>]+)', data['Tags'])
        
    return data


def insert_posts(filename):
    """
    Preprocess posts in the file and insert into MongoDB database
    """
    new_posts = []
    with open(filename) as f:
        for line in f:
            data = preprocess_text(ET.fromstring(line.strip()).attrib)
            new_posts.append(data)
    posts.insert_many(new_posts)
    

if __name__ == "__main__":
    import time
    from pymongo import MongoClient
    client = MongoClient()
    db = client.stackoverflow
    posts = db.posts

    PATH = Path('../data/posts')
    init_time = time.time()
    for file in PATH.iterdir():
        print(file)
        time0 = time.time()
        insert_posts(file)
        print("Time taken to insert = {} seconds".format(time.time()-time0))
        print("Time taken so far = {} seconds".format(time.time() - init_time))