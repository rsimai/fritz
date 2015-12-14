#!/usr/bin/python
#
#
# login to Fritzbox and get a SID
# rsimai suse.de


import urllib
import re
import md5

login_url = 'http://fritz.box/login_sid.lua'
pw = 'PASSWORT'

response = urllib.urlopen(login_url).read()                                     # read XML including challenge string
challenge_string = re.search('<Challenge>(\w+)</Challenge>', response).group(1) # extract the challenge string
challenge_pw = challenge_string + "-" + pw                                      # assemle for hashing
challenge_pw_utf16le = challenge_pw.encode('utf-16le')                          # encode into utf16le
md5 = md5.new(challenge_pw_utf16le).hexdigest()                                 # hash it
challenge_response = challenge_string + '-' + md5                               # assemble as challenge response
auth_url = login_url + '?user=&response=' + challenge_response                  # plus the URL
response = urllib.urlopen(auth_url).read()                                      # submit
sid = re.search('<SID>(\w+)</SID>', response).group(1)                          # extract the session ID

if sid == '0000000000000000':                                                   # true if auth didn't work out
    print "Login failed, no SID received"
    exit(1)

print "sid received:", sid                                                      # the SID to be used in further GET


