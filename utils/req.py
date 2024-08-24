import requests
from dotenv import load_dotenv
import os

load_dotenv()

def use_post(
        body: dict = {},
        headers: dict =  {
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
        'Content-Type': 'application/json',
    },
        protocol: str = 'http',
        host: str|bool = None,
        port: int|bool = None,
        route: str = '',
        ):
    # Define the URL
    host = os.getenv('MYSQL_HOST') if host is None else host
    port = os.getenv('MYSQL_PORT') if port is None else port
    url = f'{protocol}://{host}:{port}/{route}'

    # Make the POST request
    response = requests.post(url, headers=headers, json=body)

    # Check the status code
    if response.status_code == 200:
        # Successful request
        response_data = response.json()
        print('Response Data:', response_data)
    else:
        # Request failed
        print(f'Status Code: {response.status_code}')
        print('Response Text:', response.text)

def use_put(
        body: dict = {},
        headers: dict =  {
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
        'Content-Type': 'application/json',
    },
        protocol: str = 'http',
        host: str|bool = None,
        port: int|bool = None,
        route: str = '',
        ):
    # Define the URL
    host = os.getenv('MYSQL_HOST') if host is None else host
    port = os.getenv('MYSQL_PORT') if port is None else port
    url = f'{protocol}://{host}:{port}/{route}'

    # Make the POST request
    response = requests.put(url, headers=headers, json=body)

    # Check the status code
    if response.status_code == 200:
        # Successful request
        response_data = response.json()
        print('Response Data:', response_data)
    else:
        # Request failed
        print(f'Status Code: {response.status_code}')
        print('Response Text:', response.text)

def use_delete(
        body: dict = {},
        headers: dict =  {
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
        'Content-Type': 'application/json',
    },
        protocol: str = 'http',
        host: str|bool = None,
        port: int|bool = None,
        route: str = '',
        ):
    # Define the URL
    host = os.getenv('MYSQL_HOST') if host is None else host
    port = os.getenv('MYSQL_PORT') if port is None else port
    url = f'{protocol}://{host}:{port}/{route}'

    # Make the POST request
    response = requests.delete(url, headers=headers, json=body)

    # Check the status code
    if response.status_code == 200:
        # Successful request
        response_data = response.json()
        print('Response Data:', response_data)
    else:
        # Request failed
        print(f'Status Code: {response.status_code}')
        print('Response Text:', response.text)

def use_get(
        params: dict = {},
        headers: dict =  {
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
        'Content-Type': 'application/json',
        
    },
        protocol: str = 'http',
        host: str|bool = None,
        port: int|bool = None,
        route: str = '',
        ):
    
    # Define the URL
    host = os.getenv('MYSQL_HOST') if host is None else host
    port = os.getenv('MYSQL_PORT') if port is None else port
    url = f'{protocol}://{host}:{port}/{route}'

    # Make the GET request
    response = requests.get(url, headers=headers, params=params)

    # Check the status code
    if response.status_code == 200:
        # Successful request
        data = response.json()  # Parse JSON response
        print('Response Data:', data)
    else:
        # Request failed
        print(f'Error: {response.status_code}')
        print('Response Text:', response.text)

use_delete(body={
    "id": 18
},
port=5000,
route='users')