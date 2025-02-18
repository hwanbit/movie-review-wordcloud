""" * File: review.py
    * Author: Miseon Lee
    * Date: 2024-12-03
    * Description: 이 파일은 네이버 영화 리뷰 데이터의 영화별 워드클라우드를 생성합니다."""

from konlpy.tag import Okt
import collections
import matplotlib.pyplot as plt
from wordcloud import wordcloud, WordCloud
import pandas as pd

# Dataframe 형태로 데이터 파일 읽어오기
df = pd.read_csv('./Data/movie_aisw.csv')

# 데이터 탐색
print(df)
df.info()
print(df.isnull().sum()) # 결측치 재확인

# 영화 개수 및 제목 확인
unique_movies = df['movie'].nunique()
print(f'영화 개수 : {unique_movies}')
unique_movies_list = df['movie'].unique()
print(f'영화 제목 : {unique_movies_list}')

# 영화별 평점과 리뷰 수 확인
average_scores = df.groupby('movie')['score'].mean().round(2)
print(f'영화별 평균 평점 : {average_scores}')
sentence_counts = df.groupby('movie')['sentence'].count()
print(f'영화별 리뷰 개수 : {sentence_counts}')

# [올빼미] 영화 리뷰 필터링 및 전처리
owl_df = df[df['movie'] == '올빼미']
owl_df['sentence'] = owl_df['sentence'].str.replace("[^ㄱ-ㅎ가-힣 ]", "", regex=True)
print(owl_df)

# 형태소 분석 및 상위 50개 단어 추출
okt = Okt()
temp_list = []
for sentence in owl_df['sentence']:
    s_list = okt.pos(sentence)
    for word, tag in s_list:
        if tag in ['Noun', 'Adjective']:
            temp_list.append((word))
counts = collections.Counter(temp_list)
tag = counts.most_common(50)
print(tag)

# 불용어 제거
stopword=['영화', '진짜', '최고', '정말', '입니다', '만',
          '올해', '것', '꼭', '볼', '더', '보고', '류준',
          '중', '수', '간만', '때', '정도', '중간', '안',
          '감', '그냥', '이', '좀', '그', '하나', '있는', '거']
list = []
for sentence in owl_df['sentence']:
    s_list = okt.pos(sentence)
    for word, tag in s_list:
        if word not in stopword:
            if tag in ['Noun', 'Adjective']:
                list.append(word)
counts=collections.Counter(list)
tag=counts.most_common(50)
print(tag)

# 워드클라우드 생성
font_path='C:/Windows/Fonts/malgun.ttf'
wc=WordCloud(font_path=font_path, background_color='white', max_font_size=60)
cloud = wc.generate_from_frequencies(dict(tag))
plt.imshow(cloud)
plt.show()

# 영화 리뷰 수가 두번째로 많은 영화의 분석 및 워드클라우드 생성 [블랙 팬서: 와칸다 포에버]
black_df = df[df['movie'] == '블랙 팬서: 와칸다 포에버']
print(black_df)

black_df['sentence'] = black_df['sentence'].str.replace("[^ㄱ-ㅎ가-힣 ]", "", regex=True)
print(black_df)

okt = Okt()
temp_list = []
for sentence in black_df['sentence']:
    s_list = okt.pos(sentence)
    for word, tag in s_list:
        if tag in ['Noun', 'Adjective']:
            temp_list.append((word))
counts = collections.Counter(temp_list)
tag = counts.most_common(50)
print(tag)

font_path = 'C:/Windows/Fonts/malgun.ttf'
wc = WordCloud(font_path=font_path, background_color='white', max_font_size=60)
cloud=wc.generate_from_frequencies(dict(tag))
plt.imshow(cloud)
plt.show()

stopword=['영화', '것', '진짜', '그냥', '볼', '더',
          '수', '정말', '이제', '좀', '안', '왜', '정도',
          '듯', '점', '편', '보고', '입니다', '부분', '분', '내']
list = []
for sentence in black_df['sentence']:
    s_list = okt.pos(sentence)
    for word, tag in s_list:
        if word not in stopword:
            if tag in ['Noun', 'Adjective']:
                list.append(word)
counts=collections.Counter(list)
tag=counts.most_common(50)
print(tag)

font_path='C:/Windows/Fonts/malgun.ttf'
wc=WordCloud(font_path=font_path, background_color='white', max_font_size=60)
cloud = wc.generate_from_frequencies(dict(tag))
plt.imshow(cloud)
plt.show()