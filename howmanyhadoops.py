import os
import urllib
import random
import string

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):

    def get(self):
    	template = JINJA_ENVIRONMENT.get_template('index.html')
    	self.response.write(template.render())


class HowMany(webapp2.RequestHandler):

    def choice(self, words):
       #assumes words is non-empty
       random.seed
       index = random.randint(0,len(words)-1)
       return words[index]
       
    #   Stolen from: 
    #   shaney.py              by Greg McFarlane
    #                          some editing by Joe Strout
    #
    #   search for "Mark V.  Shaney" on the WWW for more info!
    # http://www.yisongyue.com/shaney/
    def run( self, text ):
        words = string.split(text)
        
        end_sentence = []
        dict = {}
        prev1 = ''
        prev2 = ''
        for word in words:
          if prev1 != '' and prev2 != '':
            key = (prev2, prev1)
            if dict.has_key(key):
              dict[key].append(word)
            else:
              dict[key] = [word]
              if (prev1[-1:] == '.' or prev1[-1:] == '?' or prev1[-1:] == '!'):
                end_sentence.append(key)
          prev2 = prev1
          prev1 = word
        
        if end_sentence == []:
          print 'Sorry, there are no sentences in the text.'
          return
        
        key = ()
        count = 1
        
        line = []

        while 1:
          if dict.has_key(key):
            word = self.choice(dict[key])
            print word, 
            line.append( word )
            key = (key[1], word)
            if key in end_sentence:
              print
              count = count - 1
              key = self.choice(end_sentence)
              if count <= 0:
                break
          else:
            key = self.choice(end_sentence)
        
        return ' '.join( line )

    def post(self):
    	content = self.request.get('content')

        path = os.path.join(os.path.split(__file__)[0], 'static/cloudera-blog.txt')
        text = open(path).readlines()[0]

        advice = self.run( text )

        logging.info("PROJECT DESCRIPTION: %s", content)
        logging.info("ADVICE: %s", advice)

    	template_values = {
    	    'content': content,
            'advice': advice
    	}

    	template = JINJA_ENVIRONMENT.get_template('result.html')
    	self.response.write(template.render(template_values))


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', HowMany),
], debug=True)