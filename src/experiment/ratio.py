import aiohttp
import asyncio
import nest_asyncio
from src.report import get_random_headers

async def fetch(session, url):
    """
    Asynchronously fetches data from a specified URL using the provided session and headers.
    Parameters:
        session (aiohttp.ClientSession): The session object used for making the HTTP request.
        url (str, optional): The URL to fetch data from. Defaults to the value of `url`.
    Returns:
        dict: The JSON response obtained from the URL.
    """
    async with session.get(url, headers=get_random_headers()) as response:
        return await response.json()

async def main(ticker_list, url_template):
    urls = [url_template.format(ticker) for ticker in ticker_list]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    # Map the results back to their respective tickers
    data = {ticker: result for ticker, result in zip(ticker_list, results)}
    return data

nest_asyncio.apply()

url = 'https://apipubaws.tcbs.com.vn/stock-insight/v1/stock/second-tc-price?tickers={}'
def get_data_from_api(tickers, url=url):
    data = asyncio.run(main(tickers, url))
    return data