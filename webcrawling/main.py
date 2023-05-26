from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time


# 웹 크롤링 하기
def webcrawling(url, one_page=False):

    # 데이터 형식 정의
    df = pd.DataFrame(
        columns=[
            'title',  # 제목
            'lyric',  # 가사
        ]
    )

    driver = webdriver.Chrome()

    # 웹 크롤링 시작
    songs_per_page = 50
    song_cnt = 0
    page_cnt = 0
    while True:

        if one_page:
            driver.get(url)
        else:
            driver.get(url+str(songs_per_page*page_cnt+1))
            time.sleep(1)

        # 해당 페이지 안에 있는 음악 목록 확인
        songs = driver.find_elements(By.CLASS_NAME, 'type03')[1:]
        if len(songs) == 0:
            break

        # 각 음악 설명을 보기 위해 순회하면서 클릭
        for song_idx in range(songs_per_page):
            songs = driver.find_elements(By.CLASS_NAME, 'type03')[1:]

            if song_idx >= len(songs):
                break
            song = songs[song_idx]
            print('\rwebcrawling: ' + str(song_cnt), end='')
            song_cnt += 1
            song.click()

            # 정보 추출
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # 1. 제목
            song_title = soup.find('div', class_='song_name').text.replace('\n', '').replace('\t', '')[2:]

            # 2. 가사
            if soup.find('div', class_='lyric_none'):
                continue

            song_lyric = soup.find('div', class_='lyric')
            for br in song_lyric.find_all('br'):
                br.replace_with('/')
            song_lyric = song_lyric.text.replace('\n', '').replace('\t', '')

            # 정보 추가
            df.loc[len(df)] = [song_title, song_lyric]


            # 뒤로 가기
            driver.back()
            time.sleep(0.5)

        # 페이지 이동
        if one_page:
            break
        page_cnt += 1

    return df


# songs_url = "https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq=521849384#params%5BplylstSeq%5D=521849384&po=pageObj&startIndex="
# total_data = webcrawling(url=songs_url, one_page=False)
# total_data.to_csv('21.csv', encoding='utf-8')

file1 = pd.read_csv('1.csv', encoding='utf-8')
file2 = pd.read_csv('2.csv', encoding='utf-8')
file3 = pd.read_csv('3.csv', encoding='utf-8')
file4 = pd.read_csv('4.csv', encoding='utf-8')
file5 = pd.read_csv('5.csv', encoding='utf-8')
file6 = pd.read_csv('6.csv', encoding='utf-8')
file7 = pd.read_csv('7.csv', encoding='utf-8')
file8 = pd.read_csv('8.csv', encoding='utf-8')
file9 = pd.read_csv('9.csv', encoding='utf-8')
file10 = pd.read_csv('10.csv', encoding='utf-8')
file11 = pd.read_csv('11.csv', encoding='utf-8')
file12 = pd.read_csv('12.csv', encoding='utf-8')
file13 = pd.read_csv('13.csv', encoding='utf-8')
file14 = pd.read_csv('14.csv', encoding='utf-8')
file15 = pd.read_csv('15.csv', encoding='utf-8')
file16 = pd.read_csv('16.csv', encoding='utf-8')
file17 = pd.read_csv('17.csv', encoding='utf-8')
file18 = pd.read_csv('18.csv', encoding='utf-8')
file19 = pd.read_csv('19.csv', encoding='utf-8')
file20 = pd.read_csv('20.csv', encoding='utf-8')
file21 = pd.read_csv('21.csv', encoding='utf-8')


total_data = pd.concat([file1, file2, file3, file4, file5, file6, file7, file8, file9, file10, file11, file12, file13, file14, file15, file16, file17, file18, file19, file20, file21])
total_data.to_csv('song_data_new.csv', encoding="utf-8-sig")