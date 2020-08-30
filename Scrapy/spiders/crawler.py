# -*- coding: utf-8 -*-
import scrapy
import urllib.request as urllib2
import csv
import json

#teste125458@gmail.com
#125458

class CrawlerSpider(scrapy.Spider):
    name = 'crawler'
    start_urls = ['https://openlibrary.org/account/login?']

    def parse(self, response):

        formdata = {
            'username': 'teste125458@gmail.com',
            'password': '125458'
            }
        yield scrapy.FormRequest(
            url = 'https://openlibrary.org/account/login?',
            formdata = formdata,
            callback=self.parse_login
        )

    def parse_login(self, response):

        subject_url = 'https://openlibrary.org/subjects'
        yield scrapy.Request(
            url = subject_url,
            callback=self.parse_subject
        )
    
    def parse_subject(self, response):

        for url in response.xpath('//a[contains(@href, "/subjects/")]/@href').getall():
            print("CATEGORY URL: ", url)
            yield scrapy.Request(
                url = response.urljoin(url),
                callback=self.parse_category
            )

    def parse_category(self, response):
        if response.status == 200:
            title = response.xpath("//h1[contains(@class, 'inline')]/text()").extract_first()
            urljs = response.xpath("//div[contains(@class, 'carousel-section')]/div/div/@data-config").extract_first().split('"')[5] #by subject 
            limit = response.xpath("//div[contains(@class, 'carousel-section')]/div/div/@data-config").extract_first().split('"')[8].replace(",","").replace(":","").strip()
            for page in range(0, 100):
                api_url = "https://openlibrary.org%s" % urljs + "?limit=%s" % limit + "&offset=%s" % page * 12
                meta = {
                    'title': title,
                }
                req = scrapy.Request(
                    url = api_url,
                    callback = self.parse_json,
                )
                yield req
        else:
            pass

    def parse_json(self,response):
        jsonresponse = json.loads(response.body_as_unicode())
        subject = jsonresponse['name']
        works = jsonresponse['works']
        for work in works:
            item = {}
            item['title'] = work['title']
            item['main_subject'] = subject
            item['cover_edition_key'] = work['cover_edition_key'] if 'cover_edition_key' in work else ''
            item['cover_id'] = work['cover_id'] if 'cover_id' in work else ''
            item['edition_count'] = work['edition_count'] if 'edition_count' in work else ''
            item['lending_identifier'] = work['lending_identifier'] if 'lending_identifier' in work else ''
            item['lendinglibrary'] = work['lendinglibrary'] if 'lendinglibrary' in work else ''
            item['lending_edition'] = work['lending_edition'] if 'lending_edition' in work else ''
            item['first_publish_year'] = work['first_publish_year'] if 'first_publish_year' in work else ''
            item['checked_out'] = work['checked_out'] if 'checked_out' in work else ''
            item['public_scan'] = work['public_scan'] if 'public_scan' in work else ''
            item['printdisabled'] = work['printdisabled'] if 'printdisabled' in work else ''
            item['has_fulltext'] = work['has_fulltext'] if 'has_fulltext' in work else ''
            item['authors'] = '\n'.join([author['name'] for author in work['authors']]) if 'authors' in work else ''
            item['availability'] = work['availability']['status'] if 'availability' in work else ''
            item['subject'] = '\n'.join(work['subject']) if 'subject' in work else ''
            item['ia'] = work['ia'] if 'ia' in work else ''
            item['ia_collection'] = '\n'.join(work['ia_collection']) if 'ia_collection' in work else ''
            item['url'] = "https://openlibrary.org/{}".format(work['key']) if 'url' in work else ''
            yield item
