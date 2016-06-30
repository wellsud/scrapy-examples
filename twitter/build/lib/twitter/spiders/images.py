# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 22:46:14 2016

@author: Wellington
"""

# -*- coding: utf-8 -*-
import scrapy
import json
#from scrapy.http import Request
from twitter.items import TwitterItem
from time import sleep



class ImagesSpider(scrapy.Spider):
    term='flamengo'
    name = "images"
    #allowed_domains = ["https://twitter.com","https://twitter.com/i/","https://twitter.com/i/search/" ]
    start_urls = (
        'https://twitter.com/i/search/timeline?f=images&vertical=default&q='+term,
    )
    
    #min position refers to oldest tweet ID in the page. 
    min_position=''
    #max position refers to newest tweet ID in the page.  
    max_position=''
    returned_items=0
    max_result=100
    
    def parse(self, response):
        
        #Response is a json file and the html code is in items_html key
        json_response = json.loads(response.text)
        print "chaves json: ", json_response.keys()
        #sleep(8)
        html_text = json_response['items_html']
        
        #Here I extract all tweets from this page    
        Images = scrapy.selector.Selector(text=html_text).css('.grid-tweet')
        print "tweets: ", Images
        
        item= TwitterItem()
        
        #self.min_position=tweets[-1].xpath('@*')[1].extract()
        
        #if self.max_position=='':
       #     self.max_position=tweets[0].xpath('@*')[1].extract()

        for tweet in Images:
            #Parsing Userame
            item['username']=tweet.css('span.username > b').xpath('text()').extract()[0]
            
            #Parsing Time
            item['timestamp']=tweet.css("span._timestamp").xpath('text()').extract()[0]
            
            #parsing Text:
            item['text']=tweet.css('p.tweet-text').xpath('text()').extract()
            #print item['text']
                        
            #parsing Retweets
            retweet_span=tweet.css('span.ProfileTweet-action--retweet > span.ProfileTweet-actionCount')
            item['retweets'] = retweet_span.xpath('@*').extract()[-1]
        
            #parsing favorites
            favorite_span = tweet.css('span.ProfileTweet-action--favorite > span.ProfileTweet-actionCount')
            item['favorites'] = favorite_span.xpath('@*').extract()[-1]
            
            print item
            self.returned_items= self.returned_items+1
        
       # new_request='https://twitter.com/i/search/timeline?f=images&q='+self.term+'&max_position=TWEET-'+self.min_position+'-'+self.max_position
        #while(self.returned_items < 101):
         #   sleep(3.5)            
          #  yield scrapy.Request(url=new_request, callback=self.parse)
        
            #tweet_data['Favorites']=favorite_count[0].attrib['data-tweet-stat-count']