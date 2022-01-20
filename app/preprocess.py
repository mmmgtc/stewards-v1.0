import os
import requests
import pandas as pd
import json

graph_tally = "https://api.thegraph.com/subgraphs/name/withtally/protocol-gitcoin-bravo-v2"

CRLF = "\\r\\n"

def request_init_data(address):
    
    payload = (
        '{"query":"query ($voterAddress: String!) {'
        + CRLF
        + "  account(id: $voterAddress) {"
        + CRLF
        + "    id"
        + CRLF
        + "    ballotsCastCount"
        + CRLF
        + "    percentageOfTotalVotingPower"
        + CRLF
        + "    frequencyOfParticipationTotal"
        + CRLF
        + "  }"
        + CRLF
        + '}","variables":{"voterAddress":"'
        + address
        + '"}}'
    )

    response = requests.request("POST", graph_tally, data=payload)

    res = json.loads(response.text)

    if res["data"]["account"] == None:
        return 0.00, 0.00

    else:
        voting_power = round(float(res["data"]["account"]["percentageOfTotalVotingPower"]), 2)
        voting_participation = round(float(res["data"]["account"]["frequencyOfParticipationTotal"])*100, 2)
        return voting_power, voting_participation


def workstream_cleaning(i):
    if str(i) == "MMM":
        return "Merch, Memes, Marketing"
    elif str(i) == "PGF":
        return "Public Goods Funding"
    elif str(i) == "MC":
        return "Moonshot Collective"
    elif str(i) == "DG":
        return "Decentralize Gitcoin"
    elif str(i)=="FDD":
        return "Fraud Detection & Defense"
    else:
        return "-"


def gitcoin_score(username):
    s = requests.get(
        f"https://gov.gitcoin.co/u/{username}.json",
        headers={
            "Api-key": os.environ.get("DISCOURSE_API_KEY"),
            "Api-Username": os.environ.get("DISCOURSE_API_USERNAME"),
        },
    )
    return int(s.json()["user"]["post_count"])


def preprocess():
    #if: save file and load the last version
    stewards_data = pd.read_csv("app/assets/csv/stewards.csv")

    stewards_data.workstream_short = stewards_data.workstream_short.apply(workstream_cleaning)

    stewards_data["votingweight"], stewards_data["voteparticipation"] = zip(*stewards_data.address.map(request_init_data))

    return stewards_data
