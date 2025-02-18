# Movie Review Wordcloud

This project generates word clouds from Naver movie reviews to visualize frequently mentioned words for movies.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Project Structure](#project-structure)

## Overview
The script analyzes Korean movie reviews, extracts meaningful words, and creates word clouds for easy visualization of word frequency.

## Features
- Reads Naver movie review data from a CSV file.
- Handles missing data and performs text cleaning with regular expressions.
- Uses the Okt (Open Korean Text) tokenizer for morphological analysis.
- Removes stopwords to refine the word list.
- Generates and displays word clouds for the movies "The Night Owl" and "Black Panther: Wakanda Forever".

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/movie-review-wordcloud.git
   ```
2. Install dependencies.

3. Make sure you have a Korean font installed and update the font path in `review.py`:
   ```python
   font_path = 'C:/Windows/Fonts/malgun.ttf'  # Update for your OS
   ```

## Usage
1. Place your movie review CSV file at `./Data/movie_aisw.csv`.
2. Run the script:
   ```bash
   python review.py
   ```
3. The word clouds will be displayed.

## Dependencies
- Python 3.8
- konlpy
- matplotlib
- wordcloud
- pandas
- collections

## Project Structure
```
.
├── Data
│   └── movie_aisw.csv
├── review.py
└── README.md
```

---

## 데이터 전처리 방법 및 워드클라우드 생성

여러 영화의 리뷰와 평점 데이터를 탐색하고, 데이터 정제 과정을 거쳐 영화에 대한 리뷰 워드클라우드를 생성하는 것이 목표입니다.

### 1. 파일 읽어오기
Pandas의 read_csv를 통해서 csv 파일을 읽어와 Dataframe 형태로 만듭니다. <br/>
Dataframe 형태는 Numpy 구조를 기반으로 하여 연산 작업에서 빠른 속도를 보이기 때문에 데이터 분석에 자주 사용되는 형태입니다.
```
df = pd.read_csv('./Data/movie_aisw.csv')
```

### 2. 데이터 확인하기
맨 앞의 데이터 5개와 마지막 데이터 5개를 콘솔창에 출력하여 데이터 구조를 간단히 확인하고 데이터에 어떤 식으로 접근하면 좋을지 파악합니다.
```python
print(df)
```
데이터 전처리 전에 데이터의 타입 확인이 우선이므로 데이터의 열과 행 개수를 확인하며, 열의 이름과 결측치 여부, 데이터의 타입을 확인합니다.
```python
df.info()
```
df.info()를 통해서도 결측치 개수를 확인할 수 있지만 아래 코드로도 확인 가능합니다.
```python
print(df.isnull().sum())
```

### 3. 영화 개수 확인하기
데이터의 movie 열에 몇 개의 다른 영화가 있는지 알 수 없으므로 아래 코드로 movie 열의 고유값 개수를 확인합니다.
```python
df.nunique()
```
영화의 개수를 확인했으므로, 영화의 제목을 확인합니다. 아래 코드로 movie 열의 고유값들을 확인할 수 있습니다.
```python
df.unique()
```

### 4. 영화별 평점과 리뷰 수 확인하기
영화별 평균 평점을 확인하기 위해 movie 열의 동일한 영화 제목끼리 묶은 뒤 score 열의 평균을 계산합니다. (소수점 3번째 자리에서 반올림)
```python
df.groupby('movie')['score'].mean().round(2)
```
영화별 리뷰 수를 확인하기 위해 movie 열의 동일한 영화 제목끼리 묶은 뒤 sentence 열의 비어있지 않은 값을 셉니다.
```python
df.groupby('movie')['sentence'].count()
```

### 5. [올빼미] 영화 리뷰 필터링 및 전처리
올빼미의 리뷰 내용인 sentence 열의 값에서 한글(초성~종성)과 공백을 제외한 모든 문자를 제거합니다.<br/>
[^ㄱ-ㅎ가-힣 ]은 한글 문자(초성부터 종성까지)와 공백( )을 제외한 모든 문자를 의미합니다.<br/>
이 코드를 통해 한글 모음, 영어, 숫자, 특수문자, 이모티콘 등을 제거하여 의미 있는 단어만 남깁니다.
```python
owl_df = df[df['movie'] == '올빼미']
owl_df['sentence'] = owl_df['sentence'].str.replace("[^ㄱ-ㅎ가-힣 ]", "", regex=True)
```
### 6. 형태소 분석 및 상위 50개 단어 추출
Okt(Open Korean Text) 한국어 텍스트 분석 라이브러리를 사용하여 owl_df['sentence']에 저장된 텍스트 데이터를 한 문장씩 순회하며 s_list에 형태소와 품사로 분리합니다.<br/>
분석된 형태소와 품사를 순회하며 품사가 명사 또는 형용사인 경우에 temp_list에 추가합니다.<br/>
collections.Counter를 사용해 temp_list에 저장된 명사와 형용사의 빈도수를 계산하여, 빈도수가 높은 상위 50개의 단어를 출력합니다.<br/>
```python
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
```
### 7. 불용어 제거
상위 50개의 단어를 확인하며 영화 평가를 바로 알 수 없는 단어들을 삭제합니다.<br/>
삭제할 단어들을 stopword 리스트에 저장한 뒤, stopword 리스트에 포함되지 않은 단어들만 명사와 형용사로 나누어 list에 추가합니다.
```python
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
```

### 8. 워드클라우드 생성
워드클라우드를 생성할 때, 한글은 폰트를 설정해주어야 알맞게 생성되므로 font_path를 통해 글씨체를 설정해준 뒤 워드클라우드를 생성합니다.
```python
font_path='C:/Windows/Fonts/malgun.ttf'
wc=WordCloud(font_path=font_path, background_color='white', max_font_size=60)
cloud = wc.generate_from_frequencies(dict(tag))
plt.imshow(cloud)
plt.show()
```
---
## 워드클라우드 결과물
### ✔️ 올빼미 워드클라우드
<img src="https://github.com/hwanbit/movie-review-wordcloud/blob/main/Result/The_Night_Owl_WordCloud.jpg" height="400"/>

### ✔️ 블랙팬서 워드클라우드
<img src="https://github.com/hwanbit/movie-review-wordcloud/blob/main/Result/Black_Panther_WordCloud.jpg" height="400"/>
