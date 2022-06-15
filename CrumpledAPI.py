from flask import Flask, render_template, request, redirect
import string
import secrets
import random
from urllib import response
from nanolib import generate_account_id
import requests
from secrets import token_bytes
from coincurve import PublicKey
from sha3 import keccak_256
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()


app = Flask(__name__)

@app.route('/') # default homepage 
def home():
    return 'Avalible Calls :'

#test 
@app.route('/test') 
def testroute():
    #do python stuff
    #return results / data / whatever
    return 'Result'



#  __                      _ _         
# / _\ ___  ___ _   _ _ __(_) |_ _   _ 
# \ \ / _ \/ __| | | | '__| | __| | | |
# _\ \  __/ (__| |_| | |  | | |_| |_| |
# \__/\___|\___|\__,_|_|  |_|\__|\__, |
#                                |___/ 


#Generate Strong Passwords
@app.route('/genpass', methods=['GET', 'POST'])
def genpass():
    symbols = ['@', '!', '?'] # Can add more
    password = ""
    for _ in range(4):
        password += secrets.choice(string.ascii_lowercase)
        password += secrets.choice(string.ascii_uppercase)
        password += secrets.choice(string.digits)
        password += secrets.choice(symbols)
    return password




#---------------------------------------------------------------------------------------------------

#    ___                 _        
#   / __\ __ _   _ _ __ | |_ ___  
#  / / | '__| | | | '_ \| __/ _ \ 
# / /__| |  | |_| | |_) | || (_) |
# \____/_|   \__, | .__/ \__\___/ 
#            |___/|_|             



#get crypto price from coingeko
                        #ethereum #usd 
@app.route('/crytprice/<crypto>/<local>', methods=['GET', 'POST'])
def getCryptPrice(crypto, local):
    currentPrice= cg.get_price(ids=crypto, vs_currencies=local)
    return (currentPrice)


#generate Nano Seed and related address
@app.route('/nanoseed', methods=['GET', 'POST'])
def genNanoSeed():
    full_wallet_seed = hex(random.SystemRandom().getrandbits(256))
    wallet_seed = full_wallet_seed[2:].upper()
    account_id = generate_account_id(wallet_seed, 0)
    address=account_id.replace('xrb','nano')
    return("Seed : "+wallet_seed+ "\n"+ "Address : "+address)


#generate ETH key and address
@app.route('/ethkey', methods=['GET', 'POST'])
def genEthKey():
    private_key = keccak_256(token_bytes(32)).digest()
    public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
    addr = keccak_256(public_key).digest()[-20:]
    return("Key : "+private_key.hex()+"\n"+ "Address : 0x"+addr.hex())

#---------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app.run(host='0.0.0.0')
    app.run(debug=True)
