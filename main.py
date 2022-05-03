import csv
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from config import SITE_UTL

# таймеры нужны чтобы браузер успевал прогружать страницу
def sleep():
    time.sleep(random.randrange(1, 2))


if __name__ == '__main__':

    # set options
    options = Options()
    # не открывает браузер с этой настройокй
    options.headless = True

    # start driver
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(10)
    print('началы работы парсера')

    # === STARTS PARSER ===

    # корневая папка сайта с которого парсим
    driver.get(SITE_UTL)
    print(f'переход на страницу {SITE_UTL}')
    sleep()
    # таймеры нужны чтобы браузер успевал прогружать страницу


    # находим исполнителей на странице
    authors = driver.find_elements(By.CLASS_NAME, 'author')

    # получаем ссылки на исполнителей
    author_links = []
    for author in authors:
        author_links.append(str(author.get_attribute("href")))

    print(f'на сайте {len(author_links)} исполнителей ( {author_links} )')

    for author in author_links:
        # переходим на страницу исполнителя
        driver.get(author)
        sleep()

        # находим исполнителя на странице
        author_name = driver.find_element(By.CLASS_NAME, 'title').text

        print(f'_переход на страницу исполнителя ( {author_name} )')

        # находим список песен на странице
        songs = driver.find_elements(By.CLASS_NAME, 'song')
        song_links = []
        for song in songs:
            song_links.append(str(song.get_attribute("href")))

        print(f'_у исполнителя {author_name} {len(song_links)} песен')

        for song in song_links:
            # переходим на страницу песни
            driver.get(song)
            sleep()

            # получаем название
            title = driver.find_element(By.CLASS_NAME, 'title').text
            # получаем название
            text = driver.find_element(By.CLASS_NAME, 'song-text').text

            print(f'__переход на страницу песни "{title}" исполнителя {author_name}')

            # записываем в цсв файл
            with open(f'result.csv', 'a', newline='') as csvfile:
                spamwriter = csv.writer(
                    csvfile,
                    delimiter=',',
                    quotechar='"',
                    quoting=csv.QUOTE_MINIMAL
                )
                spamwriter.writerow([author_name, title, text])
            print(f'__песня "{title}" записана в файл result.csv')

    # exit driver
    driver.quit()

