import os
import requests
import pandas as pd
import json
import time

from app.helpers.helpers import get_last_proposals, get_proposals

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
        voting_power = float(res["data"]["account"]["percentageOfTotalVotingPower"])*100
        voting_participation = float(res["data"]["account"]["frequencyOfParticipationTotal"])
    return voting_power, voting_participation

def gitcoin_posts(username):
    for i in range(10):
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
            time.sleep(5)
            continue
    return 0


def get_F_value(df):
    df['F_value'] = 1.75 * df['forum_post_count'] / df['weeks_steward']
    df['F_value'] = df['F_value'].apply(lambda x: 1.5 if x>1.5 else x)
    return df

def get_snapshot(df):
    
    values_snapshot = dict()
    number_of_votes = get_last_proposals()

    for x in range(len(number_of_votes)):
        if number_of_votes[x]['voter'].lower() in values_snapshot:
            values_snapshot[number_of_votes[x]['voter'].lower()] += 1
        else:
            values_snapshot[number_of_votes[x]['voter'].lower()]  = 1
    
    df['snapshot_votes'] = df.address.apply(lambda x: x.lower()).map(values_snapshot) /100 / 40 
    df['snapshot_votes'] = df['snapshot_votes'].fillna(0)
    return df

def transform_ten(x, max_value, min_value):
    return int(((x-min_value)/(max_value-min_value))*5+5)

def preprocess():
    cols = ['name', 'image', 'username', 'handle_gitcoin', 'statement_post_id',
        'steward_since', 'address', 'w_value', 'Tally_participation_rate', 'f_value',
        'forum_post_count', 'workstream_name', 'votingweight','voteparticipation', 
        'weeks_steward', 'F_value', 'snapshot_votes', 'V_value', 'Health_Score']
    stewards_data = pd.read_csv("app/assets/csv/stewards.csv", usecols=cols)

    proposals_data = get_proposals()

    stewards_data["Health_Score"] = stewards_data['Health_Score'].apply(lambda x: transform_ten(x, stewards_data['Health_Score'].max(), stewards_data['Health_Score'].min())).astype(int)
    
    if len(proposals_data)==40:
        stewards_data.votingweight = stewards_data.votingweight.apply(lambda x: format(x, ".2f"))
        stewards_data.voteparticipation = stewards_data.voteparticipation.apply(lambda x: format(x, ".2f"))
        return stewards_data
    
    else:

        stewards_data["forum_post_count"] = stewards_data.username.apply(gitcoin_posts)

        stewards_data["votingweight"], stewards_data["voteparticipation"] = zip(*stewards_data.address.map(request_init_data))

        stewards_data['weeks_steward'] = round( ( pd.to_datetime("now")-stewards_data['steward_since'].apply(pd.to_datetime)).dt.days / 7 )
        
        stewards_data = get_F_value(stewards_data)
        stewards_data = get_snapshot(stewards_data)

        stewards_data["V_value"] = (2.2*stewards_data["snapshot_votes"]+1.5*(stewards_data['voteparticipation']))/2
        stewards_data["Health_Score"] = stewards_data['F_value'] * stewards_data['V_value'] + stewards_data['w_value']
        stewards_data["Health_Score"] = stewards_data['Health_Score'].apply(lambda x: transform_ten(x, stewards_data['Health_Score'].max(), stewards_data['Health_Score'].min())).astype(int)
        #format to 2 decimals
        stewards_data.votingweight = stewards_data.votingweight.apply(lambda x: format(x, ".2f"))
        stewards_data.voteparticipation = stewards_data.voteparticipation.apply(lambda x: format(x*100, ".2f"))
        stewards_data.to_csv("app/assets/csv/stewards.csv",  index=False)
        return stewards_data
