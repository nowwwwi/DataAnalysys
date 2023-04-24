import re
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_travel_time(route_data: BeautifulSoup) -> int:
    t = route_data.find('li', attrs={'class': 'time'}).text

    match = re.search(r'(\d+)時間(\d+)分', t)

    if match:
        hours, minutes = int(match.group(1)), int(match.group(2))
        return hours * 60 + minutes

    match = re.search(r'(\d+)分', t)

    if match:
        return int(match.group(1))

    raise ValueError('Invalid time format')


def get_distance(route_data: BeautifulSoup) -> float:
    dist = route_data.find('li', attrs={'class': 'distance'}).text
    return float(dist.replace('km', ''))


def get_pass_stations(route_data: BeautifulSoup) -> int:
    stations = 0

    for span in route_data.find_all('span', {'class': 'btnStopNum'}):
        s = span.get_text().split('<!-- -->')[0]
        stations += int(s.replace('駅', ''))

    return stations


def get_transport_info(destination: str):
    url = 'https://transit.yahoo.co.jp/search/result?from=東京&to=' \
          + destination \
          + '&fromgid=&togid=&flatlon=&tlatlon=&via=&viacode=&y=2023&m=04&d=18&hh=10&m1=0&m2=0&type=1&ticket=ic&expkind=1&userpass=1&ws=3&s=0&al=1&shin=1&ex=1&hb=1&lb=1&sr=1'
    site = requests.get(url)
    data = BeautifulSoup(site.text, 'html.parser')

    route_data = data.find(id='route01')
    detail = route_data.find('div', attrs={'class': 'routeDetail'}).text

    pass_stations = 0

    for span in route_data.find_all('span', {'class': 'btnStopNum'}):
        num_str = span.get_text().split('<!-- -->')[0].replace('駅', '')
        pass_stations += int(num_str)

    return {
        'distance': get_distance(route_data),
        'travel_time': get_travel_time(route_data),
        'is_express': "特急" in detail,
        'is_superexpress': "新幹線" in detail,
        'is_bus': any(x in detail for x in ['bus', 'highWaybus']),
        'is_airplane': "air" in detail,
        'transfer_times': int(re.findall(r'\d+', route_data.find('li', attrs={'class': 'transfer'}).text)[0]),
        'pass_stations': pass_stations
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
            'is_airplane': None,
            'transfer_times': None,
            'pass_stations': None
        }


def get_and_save_dataframe():
    df = pd.read_csv('data/FEI_CITY_230418134143.csv', header=6)
    destination_list = list(df['地域'])
    transport_info_list = []

    for item in tqdm(destination_list):
        transport_info_list.append(process_destination(item))
        time.sleep(0.0001)

    transport_info_df = pd.DataFrame(transport_info_list)
    df = pd.concat([df, transport_info_df], axis=1)

    df.to_csv('data/temp_data.csv')

    return df


def clean_and_save_dataframe(df: pd.DataFrame):
    df = df.drop(df.columns[[0, 1, 2, 3, 4, 5, 6, 7]], axis=1).dropna(how='any')

    df = df.astype({
        'is_express': bool,
        'is_superexpress': bool,
        'is_bus': bool,
        'is_airplane': bool,
        'transfer_times': int,
        'pass_stations': int
    })

    df.to_csv('data/cleansed_data.csv')

    return df


def preprocess():
    temp_df = get_and_save_dataframe()
    cleansed_df = clean_and_save_dataframe(temp_df)

    return cleansed_df
