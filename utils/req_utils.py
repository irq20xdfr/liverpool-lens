import re
import json
import requests
from bs4 import BeautifulSoup
from utils.logging_utils import log_error

URL = "https://www.liverpool.com.mx/"

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'

def get_initial_cookies_and_headers():
    res = requests.get(URL, headers={'User-Agent': USER_AGENT})
    return res.cookies, res.headers

def get_json_search_results(description):
    json_res = {}
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
        }
        url = f'https://www.liverpool.com.mx/tienda?s={description}'
        print(f'URL: {url}')
        response = requests.get(
            url,
            headers=headers,
        )

        soup = BeautifulSoup(response.text, 'html.parser')

        # print(f'HTML: {response.text}')

        script_tag = soup.find('script', id="__NEXT_DATA__", type="application/json")

        if script_tag:
            # print(f'Script tag: {script_tag.string}')
            json_res = json.loads(script_tag.string)
    except Exception as e:
        log_error(f"Error getting search results: {e}")

    return json_res

def get_shop_results(description):
    search_results = get_json_search_results(description.replace(" ", "+"))

    records = search_results['query']['data']['mainContent']['records']
    images = []
    for r in records:
        all_meta = r['allMeta']
        variant = all_meta['variants'][0]
        sku_id = variant['skuId']
        small_image = variant['smallImage']
        title = all_meta['title']
        images.append({
            'title': title,
            'price': f"${float(variant['prices']['listPrice']):,.2f}",
            'image': small_image,
            'link': f"https://www.liverpool.com.mx/tienda/pdp/{title.replace(' ', '-')}/{sku_id}",
        })

    return images

def get_search_results(description):
    html = ""
    try:
        cookies, headers = get_initial_cookies_and_headers()
        print(cookies)
        print(headers)
        headers['User-Agent'] = USER_AGENT

        search_url = f'{URL}/tienda?s={description}'
        print(search_url)
        response = requests.get(
            search_url,
            cookies=cookies,
            headers=headers,
        )
        html = response.text
        print(html)
    except Exception as e:
        log_error(f"Error getting search results: {e}")
    return html


def parse_search_results(html):
    images = []

    pattern = r'https?://[^\s"\']+/sm[^\s"\']+'
    sm_urls = re.findall(pattern, html)

    print(f"Found {len(sm_urls)} URLs containing '/sm':")
    for url in sm_urls:
        url = url.split('#')[0] if '#' in url else url
        url = url.replace('|', '')
        if url.endswith('.jpg.jpg'):
            url = url[:-4]
        images.append(url)

    return images