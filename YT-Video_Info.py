import time

from selenium import webdriver


website_url = 'https://www.youtube.com/watch?v=UOsRrxMKJYk&ab_channel=FrankAndrade'

driver = webdriver.Chrome(executable_path='chromedriver.exe')

driver.get(website_url)

time.sleep(1)

info = {}

#xpath => //tag[@unique_attribute]
show_more_button = driver.find_element_by_xpath('//yt-formatted-string[@slot="more-button"]')
show_more_button.click()

title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string')
info['title'] = title.text


channel_name = driver.find_element_by_xpath('//a[@dir="auto"]')

info['Channel_name'] = channel_name.text

sub_count = driver.find_element_by_id('owner-sub-count')

info['sub_count'] = sub_count.text

views_count = driver.find_element_by_class_name('view-count')

info['views_count'] = views_count.text

video_description = driver.find_element_by_xpath('//ytd-expander[@style="--ytd-expander-collapsed-height:60px;"]')

info['video_description'] = video_description.text

likes_count = driver.find_element_by_xpath('//yt-formatted-string[@class="style-scope ytd-toggle-button-renderer style-text"][1]')

info['likes_count'] = likes_count.text

# print(info)

driver.quit()
