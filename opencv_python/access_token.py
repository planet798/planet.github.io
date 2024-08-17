import requests

def main():
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=jY3enrAfnPl1vdYP0XxdWIpm&client_secret=WI8nM3IB4kg9oU69nutzgaK0paajXXlS"

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == '__main__':
    main()