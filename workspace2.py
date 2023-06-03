import streamlit as st
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

maketType = {
    "KOSPI": "0",
    "KOSDAQ": "1"
}

# 웹 스크래핑 함수
def scrape_data(market_type, page):
    code = maketType[market_type]
    req = requests.get(f"https://finance.naver.com/sise/sise_market_sum.naver?sosok={code}&page={page}")
    html = req.text
    soup = bs(html, "html.parser")

    stock_contents = soup.select(f"#contentarea > div.box_type_l > table.type_2 > tbody > tr")
    data = []
    for stock_content in stock_contents:
        try:
            stock_rank = stock_content.select_one("td.no").text
            stock_name = stock_content.select_one("td:nth-child(2)").text
            stock_price = stock_content.select_one("td:nth-child(3)").text
            stock_Cap = stock_content.select_one("td:nth-child(7)").text
            stock_PER = stock_content.select_one("td:nth-child(11)").text
            stock_PBR = stock_content.select_one("td:nth-child(12)").text

            data.append({
                "Rank": stock_rank,
                "Name": stock_name,
                "Price": stock_price,
                "Market Cap": stock_Cap,
                "PER": stock_PER,
                "PBR": stock_PBR
            })

        except AttributeError:
            continue

    return data

# Streamlit 애플리케이션 구성
def main():
    st.title("주식 정보")
    selected_market = st.selectbox("시장 선택", list(maketType.keys()))
    selected_page = st.selectbox("페이지 선택", list(range(1, 51)), index=0)
    data = scrape_data(selected_market, selected_page)

    # 데이터 출력
    df = pd.DataFrame(data)
    st.dataframe(df.style.set_table_styles([{"selector": "th", "props": [("border", "1px solid black")]},
                                            {"selector": "td", "props": [("border", "1px solid black")]}]))

if __name__ == '__main__':
    main()
