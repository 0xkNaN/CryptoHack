#!/usr/bin/env python3

from telnetlib import Telnet
import json
import base64
import codecs

HOST = "socket.cryptohack.org"
PORT = 13377

cnx = Telnet(HOST, PORT)
    
def decode_res(rType, rEnc):
    decoded = ""
    if rType == "base64":
        decoded = base64.b64decode(rEnc).decode("utf-8")
    elif rType == "hex":
        decoded = bytes.fromhex(rEnc).decode("utf-8")
    elif rType == "rot13":
        decoded = codecs.decode(rEnc, 'rot_13')
    elif rType == "bigint":
        decoded = bytes.fromhex(rEnc[2:]).decode("utf-8")
    elif rType == "utf-8":
        dec = [chr(x) for x in rEnc]
        decoded = ''.join(dec)
    #
    return {"decoded": decoded}

def send_req(hsh):
    print(hsh)
    request = json.dumps(hsh).encode()
    cnx.write(request)

def read_res():
    bres = cnx.read_until(b"\n")
    res = json.loads(bres)
    print(res)
    return res

def do_the_challenge():
    res = read_res()
    try:
        rType = res["type"]
        rEnc = res["encoded"]
        decoded = decode_res(rType, rEnc)
        req = send_req(decoded)
        do_the_challenge()
    except:
        print("End of story")


do_the_challenge()
