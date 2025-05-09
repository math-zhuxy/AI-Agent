import chardet
import requests
import bs4
import typing
import lxml_html_clean
import set
def get_bing_search_result(query: str) -> typing.List[typing.Dict[str, str]]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537'
        '.36 (KHTML, like Gecko) Chrome/82.0.4051.0 Safari/537.36 Edg/82.0.425.0',
        'Cookie': set.bing_cookie
    }
    if set.bing_cookie == "":
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537'
        '.36 (KHTML, like Gecko) Chrome/82.0.4051.0 Safari/537.36 Edg/82.0.425.0'
        }
    baseUrl=f'https://cn.bing.com/search?q={query}'
    response = requests.get(baseUrl, headers=headers)
    if response.status_code != 200:
        print("There is a network problem")
        return "网络有问题"
    
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    ol_b_results = soup.find(id= 'b_results')
    final_result = []
    if not ol_b_results:
        print("empty search result")
        return final_result
    info_list = ol_b_results.find_all('li')
    for info in info_list:
        ref = info.find('a')
        content = info.find('p')
        ref_url = ""
        content_text = ""
        if ref:
            ref_url = ref.get('href')
        if content:
            content_text = content.get_text()
        final_result.append(
            {
                "ref": ref_url,
                "content": content_text
            }
        )
    final_result = [item for item in final_result if item['ref'] != "" and item['content'] != ""]
    if len(final_result) == 0:
        print("bing search function error")
    print(f"search info num: {len(final_result)}")
    return final_result

def get_web_search_result(url: str) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537'
        '.36 (KHTML, like Gecko) Chrome/82.0.4051.0 Safari/537.36 Edg/82.0.425.0'
    }
    if not url.startswith("https://"):
        url = "https://"+url
    response = requests.get(url, headers=headers)
    detected = chardet.detect(response.content)
    encoding = detected['encoding']
    response.encoding = encoding
    html_content = response.text
    
    cleaner = lxml_html_clean.Cleaner()
    cleaner.javascript = True  
    cleaner.style = True       
    cleaned_html = cleaner.clean_html(html_content)
    
    soup = bs4.BeautifulSoup(cleaned_html, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    text = ' '.join(text.split())
    return text
