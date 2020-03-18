from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk
import time
# import related to flask
from flask import Flask, render_template, send_file , jsonify,request
import requests

# #For Local Testing
application = Flask(__name__, static_url_path='')


# nltk.download('punkt')
from googletrans import Translator
translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.bn'
      #'translate.google.co.kr',
    ])

import requests 
import lxml.html 


LANGUAGE = "english"
SENTENCES_COUNT = 10


def get_update():

    try: 
        from googlesearch import search 
    except ImportError:  
        print("No module named 'google' found") 
      
    # to search 
    query = "covid-19 google scholar" #google scholer,  Czech Republic

    update ={}
      
    for url in search(query, tld="co.in", num=10, stop=2, pause=2): 
        
        print(url)        
        web_response = requests.get(url) 
  
        # building 
        element_tree = lxml.html.fromstring(web_response.text) 
          
        tree_title_element = element_tree.xpath('//title')[0] 
          
        #print("Tag title : ", tree_title_element.tag) 
        print("\nText title :", tree_title_element.text_content()) 

        print("\n")
        
        #print("\nhtml title :", lxml.html.tostring(tree_title_element)) 
        #print("\ntitle tag:", tree_title_element.tag) 
        #print("\nParent's tag title:", tree_title_element.getparent().tag) 



        
        #url = "https://academic.oup.com/clinchem/advance-article/doi/10.1093/clinchem/hvaa029/5719336"
        parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
        # or for plain text files
        # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)

        summarizer = Summarizer(stemmer)
        # print(summarizer._text)
        summarizer.stop_words = get_stop_words(LANGUAGE)


        sentence_list = []

        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            #print(dir(sentence))
            # print(sentence._text)
            sentence_list.append(sentence._text)
        sentences = (" ".join(sentence_list))
        update[tree_title_element.text_content()] = sentences
        # print("\n")    
        # for i in range(0,len(sentence_list),1):    
        #   time.sleep(2)
        #   translations = translator.translate([sentence_list[i]], dest='bn')    
        #   for translation in translations:
        #     print(translation.text)
        #   #print(translation.origin, ' -> ', translation.text)

        # print("\n")

        # translations = []
        # for sentence in sentence_list:
        #   translations.append(translator.translate(,dest='bn'))
        
        # print(translations)
    return update
@application.route('/')
def index():
    update = get_update()
    return render_template("index.html",update=update)

if __name__ == "__main__":

    application.run(debug=True)