# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json
from twitter.items import TwitterItem
import lxml

class LiveSpider(scrapy.Spider):
   
    name = "live"
    
    #Initiator allows to use paramters in command line call
    def __init__(self, term , total_results=20, *args,**kwargs ):
        
        super(LiveSpider, self).__init__(*args, **kwargs)                
        
        term = term.replace(" ","")       
        
        self.term=term
        
        self.total_results=int(total_results)
        
        self.start_urls = (
        'https://twitter.com/i/search/timeline?f=tweets&src=typd&q='+term,
        )
        self.result_counter=0
       
        
    # Receive the oldest and the newest tweet ID, respectvily for pagination
    min_position=''
    
    max_position=''
    
        
    def parse(self, response):
        
        #The response is a json file
        jsonresponse=json.loads(response.text)
                
        
        #HTML page code is in "items_html" key        
        html_text = jsonresponse['items_html']
        
        item = TwitterItem()        
        
        tweets = scrapy.selector.Selector(text=html_text).css('li.stream-item')
        
        tweets_ID = scrapy.selector.Selector(text=html_text).css('div.original-tweet')
        
        if self.max_position == '':
            
            self.max_position = tweets_ID[0].xpath('@*').extract()[1]
        
        self.min_position = tweets_ID[-1].xpath('@*').extract()[1]

        
        for tweet in tweets:
            
            if self.result_counter < self.total_results:            
                

                #Parsing Name
                
                UserName = '@' + tweet.css('span.username > b').xpath('text()').extract()[0]
                
                item['username'] = UserName
                

                #Parsing Time

                date_time = tweet.css("span._timestamp").xpath('text()').extract()[0]

                item['timestamp']= date_time
                

                #parsing Text:

                Text = tweet.css('p.tweet-text').extract()[0]

                Text = lxml.html.document_fromstring(Text)                

                Text = Text.text_content()


                #replace function prevent breaklines in csv output                

                item['text']= Text.replace('\n','').replace('\r','')
                

                #parsing Retweets

                retweet_span = tweet.css('span.ProfileTweet-action--retweet > span.ProfileTweet-actionCount')

                retweet_count = retweet_span.xpath('@*').extract()[-1]

                item['retweets'] = retweet_count


            
                #parsing favorites

                favorite_span = tweet.css('span.ProfileTweet-action--favorite > span.ProfileTweet-actionCount')

                favorite_count = favorite_span.xpath('@*').extract()[-1]

                item['favorites'] =  favorite_count
                
                self.result_counter = self.result_counter +1                      
                
                yield item
            
            else:

                self.logger.info("Scraping process concluded. Total Results: %d. \n Exiting " % self.total_results)
                
                raise StopIteration
                           
                
            
        if jsonresponse['has_more_items']:
            
            self.logger.info("Total of results at moment:" , self.result_counter)
            
            yield Request("https://twitter.com/i/search/timeline?f=tweets&q="+self.term+"&max_position=TWEET-"+ self.min_position +"-"+ self.max_position, self.parse)
        
        else:
            
            self.log('Has no more pages to crawl. Closing in some seconds...')