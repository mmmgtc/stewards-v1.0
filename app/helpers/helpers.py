import requests

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

url = 'https://hub.snapshot.org/graphql?'

def get_last_proposals():
    
    query_proposal_closed = """query Votes {
  votes (
    first: 10000000
    where: {
      voter_in: ["0x4c0a466df0628fe8699051b3ac6506653191cc21", "0x34aa3f359a9d614239015126635ce7732c18fdf3", "0x5e349eca2dc61aBCd9dD99Ce94d04136151a09Ee", "0x2b888954421b424c5d3d9ce9bb67c9bd47537d12", "0x839395e20bbb182fa440d08f850e6c7a8f6f0780", "0x54becc7560a7be76d72ed76a1f5fee6c5a2a7ab6", "0x66b1de0f14a0ce971f7f248415063d44caf19398", "0x80d63799b1e08a80f73fb7a83264b5c31600bf3a", "0xa2bf1b0a7e079767b4701b5a1d9d5700eb42d1d1", "0x31482858561725b74b5ec2a739e447bc74cdf7b9", "0x10d6d2e343281d388291a3e02f3293aaeda67178", "0x5ba02f4ff6af1d9d2af8774d10fd32eb57d4e2e6", "0x68898b237823448475bd50ea0bb6e4a20b71ff63", "0x016C8780e5ccB32E5CAA342a926794cE64d9C364", "0x4bc519f0b7b348fae780afb2dd4aa76841ba8e9e", "0x86d3ee9ff0983bc33b93cc8983371a500f873446", "0xf503017d7baf7fbc0fff7492b751025c6a78179b", "0xd9ffaf2e880df0cc7b7104e9e789d281a81824cf", "0xa30ab83e693ad49f3f651085dad11d049c818923", "0x8b405dbf2f30844b608b08dad20447a6955a6c6e", "0x88cca876eebb2a541ed87584f189319c3441aca6", "0x6375885ce997543cc7e057fe9af3e255d52fb4f4", "0x934b510d4c9103e6a87aef13b816fb080286d649", "0x8d07d225a769b7af3a923481e1fdf49180e6a265", "0x73186b2a81952c2340c4eb2e74e89869e1183df0", "0xc3fab4228ce462653dbf0bb3e4f3fdd81697fec4", "0x6bf1eba9740441d0a8822eda4e116a74f850d81b", "0x809FA673fe2ab515FaA168259cB14E2BeDeBF68e", "0xc7e6bbf6dbe78b40640385e73dc1958f4428fb3e", "0xd23aff9ad562c445bcab03321cbfe63bf4b0bcf2", "0x5a384227b65fa093dec03ec34e111db80a040615", "0x554c5aF96E9e3c05AEC01ce18221d0DD25975aB4", "0x2d407ddb06311396fe14d4b49da5f0471447d45c", "0xe4b420f15d6d878dcd0df7120ac0fc1509ee9cab", "0x02Eb89D2ff910989024e19673f8302a695bBD979", "0xed625c9ABa1245Fa8e22eb1f1825881517A9DCE7", "0x16d2ad8cc04888b537bb7b631715335a901b57ca", "0xdC0046B52e2E38AEe2271B6171ebb65cCD337518", "0x05a1ff0a32bc24265bcb39499d0c5d9a6cb2011c", "0xf07A2439296e07Bc4320AF924E655a01fb69D89C", "0x45735683E432A5701959fc4D2e0FAB19dc7D1d58", "0xf4c7E772f24c10E3Ce60CE549059a021F60c911E", "0xb53b0255895c4f9e3a185e484e5b674bccfbc076", "0x03B79C0C1487a68AeabD9AA4ce779DaD77855F52", "0xcf88fa6ee6d111b04be9b06ef6fad6bd6691b88c", "0x58f123BD4261EA25955B362Be57D89F4B6E7110a", "0x9ac9c636404C8d46D9eb966d7179983Ba5a3941A", "0x3b067af83f540cb827825a6ee5480441a4237e77", "0x4f0a1940De411285ad0455a7F40C81B5E0BC8492", "0x45735683E432A5701959fc4D2e0FAB19dc7D1d58", "0x224e69025A2f705C8f31EFB6694398f8Fd09ac5C", "0xEe0579b4C36fd52EC0A2B542fb801F136838B7f1", "0x521aacb43d89e1b8ffd64d9ef76b0a1074dedaf8", "0x7E052Ef7B4bB7E5A45F331128AFadB1E589deaF1", "0x4a5B536A613E69F43a52f6Aa7A7F3765428329ad", "0xC714a62A4BF7ff475C8dc3E589e1388342A38BB8", "0x59AE7f21D18b2F5fDC7a99c4fd6dD9E67Cec0Bc9", "0x809C9f8dd8CA93A41c3adca4972Fa234C28F7714", "0x3ec44a823e07555b5f889d8d954eec736eb5865b", "0x0585B28Fd862d3bF033bE20b178BDF01262b8424"]
    }
    orderBy: "end",
    orderDirection: asc
  ) {
    voter,
    proposal {
      id
    }
  }
}"""
    r = requests.post(url, json={'query': query_proposal_closed})
    return  r.json()['data']['votes']

def get_proposals():
    query_proposal_closed = """query Proposals {
    proposals (
        first: 10000,
        where: {
                space_in:"gitcoindao.eth",
                state: "closed"
                },
        orderBy: "created",
        orderDirection: desc
                ) {
                id
                end
                }
    } """   
    r = requests.post(url, json={'query': query_proposal_closed})
    return  r.json()['data']['proposals']