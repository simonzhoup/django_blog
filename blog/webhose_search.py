import json
import urllib.parse
import urllib.request


def read_webgose_key():
    webhose_api_key = None
    try:
        with open('search.key','r') as f:
            webhose_api_key = f.readline().strip()
    except:
        raise IOError('search.key file Not found.')
    return webhose_api_key

def run_query(search_terms,size=10):
    webhose_api_key = read_webgose_key()

    if not webhose_api_key:
        raise KeyError('search key not found.')
    root_url = 'http://webhose.io/search'
    query_string = urllib.parse.quote(search_terms)
    search_url = ('{root_url}?token={key}&format=json&q={query}'
                    '&sort=relevancy&size={size}').format(
                    root_url=root_url,
                    key=webhose_api_key,
                    query=query_string,
                    size=size)
    results = []

    try:
        response = urllib.request.urlopen(search_url).read().decode('utf-8')
        json_response= json.loads(response)

        for post in json_response['posts']:
            results.append({'title':post['title'],
                            'link':post['url'],
                            'summary':post['text'][:200]})
    except:
        print('Error when querying the Webhose API.')

    return results

if __name__ == "__main__":
    theams = input('>>>')
    size = int(input('???'))
    jieguo = run_query(theams,size)
    for i in jieguo:
        print('标题:'+i['title']+'\n'+'内容:'+i['summary'])