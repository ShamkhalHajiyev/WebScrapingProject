import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import csv
import requests

categ = ""
file = open('Crawler.csv', 'w', encoding="utf-16", newline='')
csv_writer = csv.writer(file, delimiter="\t", quotechar='"', quoting=csv.QUOTE_ALL)
fields = ['title','main_subject','cover_edition_key','cover_id','edition_count','lending_identifier','lendinglibrary','lending_edition','first_publish_year','checked_out','public_scan','printdisabled','has_fulltext','authors','availability','subject','ia','ia_collection','url']
csv_writer.writerow(fields)

driver1 = webdriver.Chrome('./chromedriver')
driver1.get('https://openlibrary.org/account/login?')
time.sleep(3)
username_input = driver1.find_element_by_id("username")
username_input.send_keys("teste125458@gmail.com")
password_input = driver1.find_element_by_id("password")
password_input.send_keys("125458")
button_login = driver1.find_element_by_class_name("login-submit")
button_login.click()
driver1.get('https://openlibrary.org/subjects')
time.sleep(2)
links = driver1.find_elements_by_xpath("//a[contains(@href, '/subjects/')]")
for link in links:
    driver1.get(link.get_attribute("href"))
    time.sleep(8)
    categ = driver1.find_element_by_xpath("//h1[contains(@class, 'inline')]").get_attribute("innerHTML").strip()
    urljs = driver1.find_element_by_xpath("//div[contains(@class, 'carousel-section')]/div/div").get_attribute("data-config").split('"')[5]
    limit = driver1.find_element_by_xpath("//div[contains(@class, 'carousel-section')]/div/div").get_attribute("data-config").split('"')[8].replace(",","").replace(":","").strip()
    print(categ)
    print(urljs)
    print(limit)
    a = 0
    while True:
        full_url_js = "https://openlibrary.org%s" % urljs + "?limit=%s"%(limit)+ "&offset=%s" % a * 12
        response1 = requests.get(full_url_js)
        jsonresponse1 = json.loads(response1.text)
        for work in jsonresponse1['works']:
            title = work['title']
            main_subject = jsonresponse1['name']
            cover_edition_key = work['cover_edition_key'] if 'cover_edition_key' in work else ''
            cover_id = work['cover_id'] if 'cover_id' in work else ''
            edition_count = work['edition_count'] if 'edition_count' in work else ''
            lending_identifier = work['lending_identifier'] if 'lending_identifier' in work else ''
            lendinglibrary = work['lendinglibrary'] if 'lendinglibrary' in work else ''
            lending_edition = work['lending_edition'] if 'lending_edition' in work else ''
            first_publish_year = work['first_publish_year'] if 'first_publish_year' in work else ''
            checked_out = work['checked_out'] if 'checked_out' in work else ''
            public_scan = work['public_scan'] if 'public_scan' in work else ''
            printdisabled = work['printdisabled'] if 'printdisabled' in work else ''
            has_fulltext = work['has_fulltext'] if 'has_fulltext' in work else ''
            authors = '\n'.join([author['name'] for author in work['authors']]) if 'authors' in work else ''
            availability = work['availability']['status'] if 'availability' in work else ''
            subject = '\n'.join(work['subject']) if 'subject' in work else ''
            ia = work['ia'] if 'ia' in work else ''
            ia_collection = '\n'.join(work['ia_collection']) if 'ia_collection' in work else ''
            url = "https://openlibrary.org/{}".format(work['key']) if 'url' in work else ''
            csv_writer.writerow([title, main_subject, cover_edition_key, cover_id, edition_count, lending_identifier, lendinglibrary, lending_edition, first_publish_year, checked_out, public_scan, printdisabled, has_fulltext, authors, availability, subject, ia, ia_collection, url])

        a += 1
        file.flush()

driver1.close()
file.close()