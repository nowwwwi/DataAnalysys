import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_travel_time(route_data: BeautifulSoup):
    time = route_data.find('li', attrs={'class': 'time'}).text.split('（')[1].split('）')[0]
    time_split = time.split('時間')

    if len(time_split) == 1:
        return int(time_split[0].split('分')[0])
    else:
        return int(time_split[0]) * 60 + int(time_split[1].split('分')[0])


def get_distance(route_data: BeautifulSoup):
    dist = route_data.find('li', attrs={'class': 'distance'}).text
    return float(dist.replace('km', ''))


def get_transport_info(destination: str):
    url = 'https://transit.yahoo.co.jp/search/result?from=東京&to=' + destination + '&fromgid=&togid=&flatlon=&tlatlon=&via=&viacode=&y=2023&m=04&d=18&hh=10&m1=0&m2=0&type=1&ticket=ic&expkind=1&userpass=1&ws=3&s=0&al=1&shin=1&ex=1&hb=1&lb=1&sr=1'
    site = requests.get(url)
    data = BeautifulSoup(site.text, 'html.parser')
    route_data = data.find(id='route01')
    detail = route_data.find('div', attrs={'class': 'routeDetail'}).text

    return {
        'distance': get_distance(route_data),
        'travel_time': get_travel_time(route_data),
        'is_express': "特急" in detail,
        'is_superexpress': "新幹線" in detail,
        'is_bus': 'bus' in detail or 'highWaybus' in detail,
        'is_airplane': "air" in detail
    }


def process_destination(destination: str):
    try:
        return get_transport_info(destination.split(' ')[1])
    except:
        return {
            'distance': None,
            'travel_time': None,
            'is_express': None,
            'is_superexpress': None,
            'is_bus': None,
            'is_airplane': None
        }


def get_and_save_dataframe():
    df = pd.read_csv('data/FEI_CITY_230418134143.csv', header=6)
    destination_list = list(df['地域'])
    transport_info_list = []

    for item in tqdm(destination_list):
        transport_info_list.append(process_destination(item))
        time.sleep(0.1)

    transport_info_df = pd.DataFrame(transport_info_list)
    df = pd.concat([df, transport_info_df], axis=1)

    df.to_csv('data/preprocessed_data.csv')

    return df


def drop_unnecessary_columns(df):
    df = df.astype({'is_express': bool, 'is_superexpress': bool, 'is_bus': bool, 'is_airplane': bool})
    df = df.drop(df.columns[[0,1,2,3,4,5,6,7]], axis=1)

    return df