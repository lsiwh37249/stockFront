import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# S&P 500 기업 티커 목록 추출
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
sp500 = pd.read_html(url)[0]
tickers = sp500['Symbol'].tolist()

# 최근 1일간 거래량 데이터 수집
data = yf.download(tickers, period="1d", group_by='ticker')

# 거래량 기준 상위 10개 종목 추출
volume_data = []
for ticker in tickers:
    try:
        vol = data[ticker]['Volume'].iloc[-1]
        volume_data.append((ticker, vol))
    except:
        continue

sorted_vol = sorted(volume_data, key=lambda x: x[1], reverse=True)[:10]

# 종목명 매핑 및 결과 출력
result = []
for ticker, vol in sorted_vol:
    info = yf.Ticker(ticker).info
    name = info.get('longName', ticker)
    result.append((name, ticker))

print("거래량 상위 10개 종목:")
for idx, (name, ticker) in enumerate(result, 1):
    print(f"{idx}. {name} ({ticker})")


# 사이드바 설정
st.sidebar.header('설정')
ticker = st.sidebar.text_input('종목 코드 (예: AAPL)', 'AAPL')
start_date = st.sidebar.date_input('시작일')
end_date = st.sidebar.date_input('종료일')

# 데이터 로드
@st.cache_data
def load_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

df = load_data(ticker, start_date, end_date)

# 캔들스틱 차트 생성
fig = go.Figure(data=[go.Candlestick(
    x=df.index,
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    name='Candlestick'
)])

# 레이아웃 설정
fig.update_layout(
    title=f'{ticker} 주가 차트',
    xaxis_title='날짜',
    yaxis_title='가격(USD)',
    xaxis_rangeslider_visible=False
)

# 차트 출력
st.plotly_chart(fig, use_container_width=True)
