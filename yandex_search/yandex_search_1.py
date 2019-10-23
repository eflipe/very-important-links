import json
import requests
import sys

import yandex_search.__init__ as yandex_search

API_USER = 'infelipe'
API_KEY = '03.760306854:e586732429bc5de4f356e1633e231be0'


# def run_query(query):
#     y = YaSearch(API_USER, API_KEY)
#     results = y.search(query, page=1)
#     serp = []
#     for result in results.items:
#         serp.append(result)
#     return serp
def run_query(query):
    yandex = yandex_search.Yandex(api_user=API_USER, api_key=API_KEY)
    search_results = yandex.search(query).items
    results = []
    for result in search_results:
        results.append({
            'title': result['title'],
            'link': result['url'],
            'summary': result['snippet']})
    return results


def main():
    print("Yandex search")
    query_str = input("Enter a query to search for: ")
    results = run_query(query_str)

    print(results)


if __name__ == '__main__':
    main()



#
#
# def read_yandex_key():
#     yandex_api_key = None
#
#     try:
#         with open('yandex.key', 'r') as f:
#             yandex_api_key = f.readline().strip()
#     except:
#         try:
#             with open('../yandex.key', 'r') as f:
#                 yandex_api_key = f.readline().strip()
#         except:
#             raise IOError('yandex.key file not found!')
#
#     if not yandex_api_key:
#         raise KeyError('Bing key not found.')
#
#     return yandex_api_key
#
#
# def run_query(search_terms):
#     yandex_key = read_yandex_key()
#     search_url = 'https://yandex.com/search/xml'
#     headers = {'Ocp-Apim-Subscription-Key': yandex_key}
#     params = {'query': search_terms, 'textDecorations': True, 'textFormat': 'HTML'}
#
#     response = requests.get(search_url, headers=headers, params=params)
#     response.raise_for_status()
#     search_results = response.json()
#
#     results = []
#     for result in search_results['webPages']['value']:
#         results.append({
#             'title': result['name'],
#             'link': result['url'],
#             'summary': result['snippet'],
#         })
#
#     return results
#
