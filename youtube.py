import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin

chrome_binary = "chrome-win64/chrome.exe"
options = webdriver.ChromeOptions()
options.binary_location = chrome_binary
driver = webdriver.Chrome(options=options)

# Заменить запрос для парсинга
query = 'Строительные материалы'

def parse_videos(youtube_videos, count=0):
    videos = {}
    for youtube_video in youtube_videos:
        video_title = youtube_video.get_attribute('title')
        video_url = youtube_video.get_attribute('href')
        if video_title and video_url:
            count += 1
            videos[video_url] = video_title
            if count >= 100:
                break;
    return videos, count

try:
    driver.maximize_window()
    driver.get('https://www.youtube.com/')
    print('Открыл ютуб, вставил запрос для парсинга видео')
    search_input = driver.find_element(By.NAME, 'search_query')
    search_input.clear()
    search_input.send_keys(query)
    search_input.send_keys(Keys.ENTER)
    time.sleep(3)

    print('Начал парсить видео')

    delta_y = 500
    while True:
        youtube_videos = driver.find_elements(By.ID, 'video-title')
        videos, count = parse_videos(youtube_videos)
        if count >= 100:
            break;
        scroll_origin = ScrollOrigin.from_element(youtube_videos[-1])
        ActionChains(driver).scroll_from_origin(scroll_origin, 0, delta_y).perform()
        delta_y += 200
        time.sleep(3)

    print('fСпарсил {count} видео')
    print(videos)

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
