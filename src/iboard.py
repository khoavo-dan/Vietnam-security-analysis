import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from io import BytesIO
import concurrent.futures
import aiohttp
import asyncio
import nest_asyncio
from datetime import datetime

async def fetch(session, url):
    headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
  }
    async with session.get(url,headers=headers) as response:
        return await response.json()


async def main(ticker_list, url):
    urls = [url.format(ticker) for ticker in ticker_list]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        market_data = await asyncio.gather(*tasks)

    market_df = pd.DataFrame(market_data)
    print(market_df)
    return market_df


nest_asyncio.apply()

# To display all tickers and their financial ratio from TCBS API as an iboard
def load_iboard(tickers):
    iboard = asyncio.run(main( tickers, 'https://apipubaws.tcbs.com.vn/stock-insight/v1/stock/second-tc-price?tickers={}'))
    data = []
    for i in np.array(iboard['data']):
        try:
            data.append(i[0])
        except:
            pass
    data = pd.DataFrame(data)
    return data


def dividend(tickers):
    data = asyncio.run(main(tickers,'https://apipubaws.tcbs.com.vn/tcanalysis/v1/company/{}/dividend-payment-histories?page=0&size=20'))
    # df = []
    # for i in np.array(df['data']):
    #     try:
    #         df.append(i[0])
    #     except:
    #         pass
    # df = pd.DataFrame(df)
    return data
