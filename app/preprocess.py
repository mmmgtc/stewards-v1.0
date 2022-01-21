import os
import requests
import pandas as pd
import json
import time

def request_init_data(address):

    graph_tally = "https://api.thegraph.com/subgraphs/name/withtally/protocol-gitcoin-bravo-v2"
    CRLF = "\\r\\n"

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
        voting_power = float(res["data"]["account"]["percentageOfTotalVotingPower"])
        voting_participation = float(res["data"]["account"]["frequencyOfParticipationTotal"])*100
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


def gitcoin_posts(username):
    for i in range(3):
        try:
            s = requests.get(
                f"https://gov.gitcoin.co/u/{username}.json",
                headers={
                "Api-key": os.environ.get("DISCOURSE_API_KEY"),
                "Api-Username": os.environ.get("DISCOURSE_API_USERNAME"),
                },
            )
            return int(s.json()["user"]["post_count"])
        except Exception as e:
            time.sleep(3)
            continue
    return 0


def get_F_value(df):
    df['F_value'] = 1.75 * df['forum_post_count'] / df['weeks_steward']
    df['F_value'] = df['F_value'].apply(lambda x: 1.5 if x>1.5 else x)
    return df

def transform_ten(x, max_value, min_value):
    return int(((x-min_value)/(max_value-min_value))*10)

def preprocess():
    # to do
    # if no updates load the latest version immediately
    stewards_data = pd.read_csv("app/assets/csv/stewards.csv")

    stewards_data['workstream_name'] = stewards_data.workstream_short.apply(workstream_cleaning)

    stewards_data["forum_post_count"] = stewards_data.username.apply(gitcoin_posts)

    stewards_data["votingweight"], stewards_data["voteparticipation"] = zip(*stewards_data.address.map(request_init_data))

    stewards_data['days_steward'] = (pd.to_datetime("now")-stewards_data['steward_since'].apply(pd.to_datetime)).dt.days
    
    stewards_data = get_F_value(stewards_data)

    stewards_data["Health_Score"] = stewards_data['health'].apply(lambda x: transform_ten(x, stewards_data['F_value'].max(), stewards_data['F_value'].min()))

    #format to 2 decimals
    stewards_data.votingweight = stewards_data.votingweight.apply(lambda x: format(x, ".2f"))
    stewards_data.voteparticipation = stewards_data.voteparticipation.apply(lambda x: format(x, ".2f"))
    
    return stewards_data
