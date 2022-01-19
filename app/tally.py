import requests

def tally(address):
    while True:
        try:
            r = requests.get(f"https://gtcselenium.herokuapp.com/?a={address}")
            return float(r.json()["Total_participation_rate"].strip("%"))

        except Exception as e:
            print(e)
            continue