# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json
from twitter.items import TwitterItem
from time import sleep
import lxml
import sys


class BasicSpider(scrapy.Spider):
   
    name = "basic"
    
    #Here assign the term of search
    term="mistureba"    
    
    # Here, you must to define the number of results    
    total_results=100   
    
    result_counter=0
    
    start_urls = (
        'https://twitter.com/i/search/timeline?f=tweets&src=typd&q='+term,
    )
    
    # Receive the oldest and the newest tweet ID, respectvily for pagination
    min_position=''
    max_position=''
    
        
    def parse(self, response):
        
        #The response is a json file
        jsonresponse=json.loads(response.text)
                
        
        #HTML code is in "items_html" key        
        html_text= jsonresponse['items_html']
                
        item= TwitterItem()        
        
        tweets=scrapy.selector.Selector(text=html_text).css('li.stream-item')
        
        tweets_ID=scrapy.selector.Selector(text=html_text).css('div.original-tweet')
        
        if self.max_position == '':
            self.max_position = tweets_ID[0].xpath('@*').extract()[1]
        
        self.min_position = tweets_ID[-1].xpath('@*').extract()[1]

        
        for tweet in tweets:
            
            if self.result_counter < self.total_results:            
                
                #Parsing Name
                UserName = '@' + tweet.css('span.username > b').xpath('text()').extract()[0]
                item['username'] = UserName
                
                #Parsing Time
                date_time=tweet.css("span._timestamp").xpath('text()').extract()[0]
                item['timestamp']= date_time
                
                #parsing Text:
                Text = tweet.css('p.tweet-text').extract()[0]
                Text = lxml.html.document_fromstring(Text)                
                Text=Text.text_content()
                item['text']= Text
                
                        
                #parsing Retweets
                retweet_span=tweet.css('span.ProfileTweet-action--retweet > span.ProfileTweet-actionCount')
                retweet_count = retweet_span.xpath('@*').extract()[-1]
                item['retweets'] = retweet_count
            
                #parsing favorites
                favorite_span = tweet.css('span.ProfileTweet-action--favorite > span.ProfileTweet-actionCount')
                favorite_count = favorite_span.xpath('@*').extract()[-1]
                item['favorites'] =  favorite_count
                
                print('\n')
                
                self.result_counter = self.result_counter +1                      
                
                yield item
            
            else:
                print "Scraping concluded. Total Results: %d. \n Exiting " % self.total_results
                sleep(5)                
                sys.exit('exiting..')              
                
            
        if jsonresponse['has_more_items']:
            print "Total of results at moment:" , self.result_counter
            print 'Trying new request in 5 seconds'
            sleep(5)
            yield Request("https://twitter.com/i/search/timeline?f=tweets&q="+self.term+"&max_position=TWEET-"+ self.min_position +"-"+ self.max_position, self.parse)
        
        else:
            print 'Has no more pages to crawl. Closing in 5 seconds...'
            sleep(5)
            sys.exit('Has no more pages to crawl')
            