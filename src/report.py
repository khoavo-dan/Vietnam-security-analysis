import requests
import pandas as pd
from io import BytesIO
from src import translator as trans
from src import local_storing
# from bs4 import BeautifulSoup
import random
import uuid
import concurrent.futures
import time

# Define the tickers and reports and the frequency
reports = ['balancesheet', 'incomestatement', 'cashflow']
def get_random_headers():
    ssi_headers = {
        'Accept': 'application/json',
        # Added comma after Accept-Language value
        'Accept-Language': 'en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'https://iboard.ssi.com.vn',
        'Referer': 'https://iboard.ssi.com.vn/',
        'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'sec-ch-ua-platform': 'Windows',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'User-Agent': '',  # Placeholder for User-Agent value
        'X-Fiin-User-ID': 'ID',
        'X-Fiin-Key': 'KEY',
        'X-Fiin-Seed': 'SEED',
    }

    user_agent_list = [
        # Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.1234.56 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.1234.56 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.1234.56 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.1234.56 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.1234.56 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.1234.56 Safari/537.36',
        # Firefox
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0',
        # Safari
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        # Edge
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.1234.56 Safari/537.36 Edg/98.0.1234.56',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.1234.56 Safari/537.36 Edg/97.0.1234.56',
        # Opera
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.1234.56 Safari/537.36 OPR/98.0.1234.56',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.1234.56 Safari/537.36 OPR/97.0.1234.56',
        # Others
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.1234.56 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.1234.56 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.1234.56 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.1234.56 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.1234.56 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.1234.56 Safari/537.36',
    ]

    user_agent = random.choice(user_agent_list)
    ssi_headers['User-Agent'] = user_agent

    supported_cache_directives = ['no-cache', 'max-age=0', 'private']
    cache_directive = random.choice(supported_cache_directives)
    ssi_headers['Cache-Control'] = cache_directive

    session_cookie = str(uuid.uuid4())
    ssi_headers['Cookie'] = f'session={session_cookie}'

    return ssi_headers


def url_prepare(tickers, reports, frequency):
    urls = ['https://fiin-fundamental.ssi.com.vn/FinancialStatement/Download{}?language=vi&OrganCode={}&Skip=0&Frequency={}'.format(report, ticker, frequency)
            for ticker in tickers for report in reports]
    keys = [f'{ticker}_{report}' for ticker in tickers for report in reports]
    return urls, keys


def fetch_financial_statement(url, key):
    """To download the financial statement from SSI API

    Args:
        url (_str_): formatted API url with ticker, report type and frequency
        key (_str_): the name of report for example Q_SSI_incomestatement

    Returns:
        _dataframe_: financial statement with table format
    """
    try:
        response = requests.get(url, headers=get_random_headers())
        df = pd.read_excel(BytesIO(response.content),
                           skiprows=7, engine='openpyxl').dropna()
        # print(f'Successfully downloaded: {key}')
        return df
    except Exception as e:
        print(f'Error occurred while downloading {key}: {e}')
    # time.sleep(7)

# OPTION 1
def fetch_batch(tickers, reports, frequency, save_file=False):
    """Download multiple financial statements from SSI, number and types of report of each ticker are listed in reports

    Args:
        tickers (_type_): Company stock exchange symbol
        reports (_type_): list of report type can include income statement, balance sheet, cash flow
        frequency (_type_): yearly or quarterly
        batch_size (int, optional): just a prevent of heat up the laptop Defaults to 10.

    Returns:
        _dict_: dictionary of financial statement with Q_ticker_reporttype as keys.
    """
    current_results = {}
    urls, keys = url_prepare(tickers, reports, frequency)
    total_tasks = len(urls)  # Total number of tasks to complete


    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures_map = {executor.submit(
            fetch_financial_statement, url, key): key for url, key in zip(urls, keys)}


        for future in concurrent.futures.as_completed(futures_map):
            key = futures_map[future]
            result = future.result()
            if result is not None:
                try:
                    current_results[key] = result
                except Exception as e:
                    print(f'Error occurred while storing: {e}')

    trans.translate_report_data(report_data=current_results)

    if save_file==True:
        local_storing.save_file(frequency, current_results)

    return current_results
