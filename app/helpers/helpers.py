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