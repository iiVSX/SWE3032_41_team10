from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time


# 웹 크롤링 하기
def webcrawling(url, label, one_page=False):

    # 데이터 형식 정의
    df = pd.DataFrame(
        columns=[
            'title',  # 제목
            'lyric',  # 가사
            'label'   # 라벨
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
            df.loc[len(df)] = [song_title, song_lyric, label]


            # 뒤로 가기
            driver.back()
            time.sleep(0.5)

        # 페이지 이동
        if one_page:
            break
        page_cnt += 1

    return df


happiness_songs_url = "https://www.melon.com/m6/landing/djplayList.htm?type=djc&plylstSeq=429411613#params%5BplylstSeq%5D=429411613&po=pageObj&startIndex="
happiness_data = webcrawling(url=happiness_songs_url, label='happiness')

sadness_songs_url = "https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq=422168373#params%5BplylstSeq%5D=422168373&po=pageObj&startIndex="
sadness_data = webcrawling(url=sadness_songs_url, label='sadness')

fear_songs_url = "https://www.melon.com/m6/landing/djplayList.htm?type=djc&plylstSeq=422618235#params%5BplylstSeq%5D=422618235&po=pageObj&startIndex="
fear_data = webcrawling(url=fear_songs_url, label='fear')

neutral_songs_url = "https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq=490041450&memberKey=&ref=copyurl&snsGate=Y"
neutral_data = webcrawling(url=neutral_songs_url, label='neutral', one_page=True)

disgust_songs = "https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq=457536603&memberKey=&ref=copyurl&snsGate=Y#params%5BplylstSeq%5D=457536603&po=pageObj&startIndex="
disgust_data = webcrawling(url=disgust_songs, label='disgust')

anger_songs = "https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq=490101618#params%5BplylstSeq%5D=490101618&po=pageObj&startIndex="
anger_data = webcrawling(url=anger_songs, label='anger', one_page=True)

total_data = pd.concat([happiness_data, sadness_data, fear_data, neutral_data, disgust_data, anger_data])
total_data.to_csv('song_data.csv', encoding='utf-8')
