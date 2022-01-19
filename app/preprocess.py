import os
import requests
import pandas as pd
import json
import math

graph_tally = "https://api.thegraph.com/subgraphs/name/withtally/protocol-gitcoin-bravo-v2"

headers = {"Content-Type": "application/json"}

CRLF = "\\r\\n"

def request_init_data(address):

    url = f"https://api.boardroom.info/v1/voters/{address}"

    response_boardroom_voters = requests.get(url).json()

    if list(response_boardroom_voters.keys())[0] == "message":

        payload = (
            '{"query":"query ($voterAddress: String!) {'
            + CRLF
            + "  histories {"
            + CRLF
            + "    totalSupply"
            + CRLF
            + "  },"
            + CRLF
            + "  account(id: $voterAddress) {"
            + CRLF
            + "    id"
            + CRLF
            + "    votes"
            + CRLF
            + "    tokenBalance"
            + CRLF
            + "    ballotsCastCount"
            + CRLF
            + "    proposalsProposedCount"
            + CRLF
            + "    percentageOfTotalVotingPower"
            + CRLF
            + "    frequencyOfParticipationTotal"
            + CRLF
            + "    delegationsCurrentlyReceivedCount"
            + CRLF
            + "    frequencyOfParticipationAsActiveVoter"
            + CRLF
            + "  }"
            + CRLF
            + "  delegators: accounts(orderBy: tokenBalance, orderDirection: desc, where: {delegatingTo: $voterAddress}){"
            + CRLF
            + "    id"
            + CRLF
            + "    votes"
            + CRLF
            + "    tokenBalance"
            + CRLF
            + "    ballotsCastCount"
            + CRLF
            + "    proposalsProposedCount"
            + CRLF
            + "    percentageOfTotalVotingPower"
            + CRLF
            + "    frequencyOfParticipationTotal"
            + CRLF
            + "    delegationsCurrentlyReceivedCount"
            + CRLF
            + "    frequencyOfParticipationAsActiveVoter"
            + CRLF
            + "  }"
            + CRLF
            + '}","variables":{"voterAddress":"'
            + address
            + '"}}'
        )

        response = requests.request("POST", graph_tally, headers=headers, data=payload)

        res = json.loads(response.text)

        if res["data"]["account"] == None:
            return "NA"

        else:
            power = "{:.2f}".format(
                float(res["data"]["account"]["percentageOfTotalVotingPower"])
            )
            return power

    else:
        power = "{:.2f}".format(
            (float(response_boardroom_voters["data"]["protocols"][0]["lastCastPower"]) / 100000000)
            * 100
        )
        return power

def request_second_data(address, totalVotes):

    url = f"https://api.boardroom.info/v1/voters/{address}"
    
    r = requests.get(url)
    try:
        userVotesCast = r.json()["data"]["protocols"][0]["totalVotesCast"]
    except Exception as e:
        userVotesCast = 0
        print(e)
    return math.ceil((userVotesCast / totalVotes) * 100)

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
    stewards_data = pd.read_csv("stewards.csv")
    stewards_data.workstream_short = stewards_data.workstream_short.apply(workstream_cleaning)
    stewards_data["votingweight"] = stewards_data.address.apply(lambda x: request_init_data(x))

    #stewards_data["f_value"] = stewards_data["username"].apply(gitcoin_score)

    w = requests.get("https://api.boardroom.info/v1/protocols/gitcoin")

    totalVotes = w.json()["data"]["totalProposals"]

    stewards_data["voteparticipation"] = stewards_data.address.apply(lambda x: request_second_data(x, totalVotes))

    return stewards_data
