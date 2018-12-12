import json
import requests
import random

def walmart(glassesType):

    if glassesType == 'D-Frame':
        glassesType = 'Wayfarer'

    print(glassesType)
    
    key = 'a5z9epyzg4vdcazhfuhkmqvz'
    assert key

    api_url = 'http://api.walmartlabs.com/v1/search?'

    params = {
        'apiKey': key,
        'query':glassesType,
        'categoryId': '976760',
        'start': 1,
        'numItems': 1,
        'format': 'json'
    }

    response = requests.get(api_url, params=params)
    data = response.json()
    if data['totalResults'] == 0:
        print('no results')
        return

    totalResults = data['totalResults']
    print(totalResults)

    params['start'] = random.randint(1, totalResults)

    response2 = requests.get(api_url, params=params)
    data2 = response2.json()
    if data2['totalResults'] == 0:
        print('no results')
        return

    name = data2['items'][0]['name']
    medImage = data2['items'][0]['mediumImage']
    prodURL = data2['items'][0]['productUrl']

    ret = {
        'type': glassesType,
        'name': name,
        'img_link': medImage,
        'prodURL': prodURL,
    }
    return ret
    # print('Product Name: ' + name)
    # print('Image Link: ' + medImage)
    # print('Product URL: ' + prodURL)
    
