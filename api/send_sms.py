import urllib.parse  # Import the correct module for urlencode
import requests

def send_message(message, number):
    # Define your API endpoint
    url = 'https://api.semaphore.co/api/v4/messages'
    
    # Define your parameters
    params = {
        'apikey': 'efc56d88b16c0228b2c147eceaf6ba67',
        'number': number,
        'message': message,
        'sendername': 'Dave'
    }
    
    # Encode parameters
    query_string = urllib.parse.urlencode(params)
    
    # Construct the full URL with parameters
    full_url = f"{url}?{query_string}"
    
    # Send the HTTP GET request (or use POST if required by the API)
    response = requests.post(full_url)
    
    # Print the response (or handle it as needed)
    print(response.text)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python semaphore.py <message> <number>")
        sys.exit(1)
    
    message = sys.argv[1]
    number = sys.argv[2]
    print("Sending Message..")
    send_message(message, number)
