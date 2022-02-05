import time

from selenium import webdriver

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def get_channel_info():
    website_url = 'https://www.youtube.com/channel/UC6tpyBt63bIKnnwfN78T0Pw'

    driver = webdriver.Chrome()

    driver.get(website_url)

    #_________Storing all Infomations_________
    info = {}

    # __________Confirming cookies settings_________
    if(driver.current_url.startswith('https://consent.youtube.com/')):
        agree_button = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div/div/button')
        agree_button.click()


    # __________Channel Name_____________
    channel_name = driver.find_element_by_class_name('style-scope ytd-channel-name').text

    info['channel_name'] = channel_name

    #__________Subsrcber Count____________
    subscriber_count = driver.find_element_by_id('subscriber-count')

    info['subscriber_count'] = subscriber_count.text

    #_________All Video List_____________
    videos = driver.find_elements_by_class_name('style-scope ytd-grid-video-renderer')

    video_list = []

    for video in videos:
        title = video.find_element_by_xpath('.//*[@id="video-title"]').text
        views = video.find_element_by_xpath('.//*[@id="metadata-line"]/span[1]').text
        when = video.find_element_by_xpath('.//*[@id="metadata-line"]/span[2]').text
        video_obj = {'title': title, 'views': views, 'when': when}
        if title != '':
            video_list.append(video_obj)

    info['video_list'] = video_list


    driver.maximize_window()
    time.sleep(2)

    # ____________Routing to About page____________
    about_button = driver.find_element_by_xpath('//*[@id="tabsContent"]/tp-yt-paper-tab[6]')
    about_button.click()

    time.sleep(5)

    #_____________Description of the channel__________
    descriptions = driver.find_elements_by_xpath('//*[@id="description"]')

    description = ''

    for des in descriptions:
        description = description + des.text

    info['description'] = description

    joining_date = driver.find_element_by_xpath('//*[@id="right-column"]/yt-formatted-string[2]')

    info['joining_date'] = joining_date.text

    total_views = driver.find_element_by_xpath('//*[@id="right-column"]/yt-formatted-string[3]')

    info['total_views'] = total_views.text

    #____________Social Media Links______________
    links = driver.find_elements_by_xpath('//*[@id="link-list-container"]/a')

    creaters_links_list = {}
    for link in links:
        creaters_links_list[link.text] = link.get_attribute('href')

    info['creaters_links_list'] = creaters_links_list


    time.sleep(1)

    print(info)

    driver.quit()


    return jsonify(info)


if __name__ == '__main__':
    app.run()