import base64
import sys
import argparse
import xtea
import utils
import diffiehellmann
import os.path
import random


def send(user, password, recipient, message_sent):
    print("sending... ")
    print("text: " + str(message_sent))

    if not os.path.exists(user.split("@")[0]):
        os.makedirs(user.split("@")[0])

    if not os.path.exists(recipient.split("@")[0]):
        os.makedirs(recipient.split("@")[0])

    # if message_sent.startswith("DH"):
    #    print("WARNING: DH is not set up yet")
    #    key = password
    # else:
    key = diffie_hellmann_key(user, recipient, password)

    if not key:
        private_key_location = user.split("@")[0] + "/dh_private.txt"
        A = diffiehellmann.get_public_key(int(utils.getStringFromText(private_key_location)))

        message_sent = "DH:" + user + ":" + str(A)
        print("text changed to: " + str(message_sent))

    # message_sent = xtea_crypt(key, message_sent, True)
    # print("xtea: " + str(message_sent))

    base64_ecnoded_msg = base64.encodestring(message_sent)
    print ("encrypted: " + str(base64_ecnoded_msg))

    # utils.write_string_to_file( recipient + "/mail" + base64_ecnoded_msg[:5] + ".txt", base64_ecnoded_msg)
    utils.write_string_to_file(recipient.split("@")[0] + "/mail.txt", base64_ecnoded_msg)


def receive(user, password):
    print ("receiving... ")
    text = utils.getStringFromText(user.split("@")[0] + "/mail.txt")
    print("read: " + str(text))

    text = base64.decodestring(text)
    print("debase64d: " + str(text))

    # decrypted = xtea_crypt(password, base64_decoded_msg, False)
    # print("decrypted: " + str(decrypted))

    if text.startswith("DH:"):
        splitted = text.split(":")
        account = splitted[1]
        key = splitted[2]
        print("found dh public key " + key + " for account " + account + " in new email. Reply to send own public key")
        if save_dh(user, account, key):
            send(user, password, account, "random text")


def xtea_crypt(password, text, enc):
    passhash = utils.generate_key(password)
    iv = passhash[len(passhash) - 8:]
    password = passhash[48:]
    return xtea.crypt(password, text, iv, enc=enc)


def save_dh(my_account, other_account, key):
    location = my_account.split("@")[0] + "/" + other_account.split("@")[0] + "_public.txt"
    if os.path.isfile(location):
        dh = read_dh(my_account, other_account)
        print "public key for account " + other_account + " already known: " + str(dh)
        return False
    print "saving dh K in file " + location
    utils.write_string_to_file(location, key)
    return True


def read_dh(my_account, other_account):
    location = my_account.split("@")[0] + "/" + other_account.split("@")[0] + "_public.txt"
    if os.path.isfile(location):
        return int(utils.getStringFromText(location))
    else:
        print "no key found for account " + other_account
        return None


def diffie_hellmann_key(account1, account2, password):
    private_key_location = account1.split("@")[0] + "/dh_private.txt"
    k_location = account1.split("@")[0] + "/dh_k.txt"

    # setup
    if not os.path.isfile(private_key_location):
        private_key = random.randint(0, 1000)
        utils.write_string_to_file(private_key_location, str(private_key))
        print("messaging is not set up. Please check mails in account " + account2 + " and reply with own public key")
        return False

    if os.path.isfile(k_location):
        K = int(utils.getStringFromText(k_location))
    else:
        a = int(utils.getStringFromText(private_key_location))
        B = int(read_dh(account1, account2))
        K = diffiehellmann.get_k(a, B)
        print "calculating K = " + str(K) + " from " + str(a) + " and " + str(B)
        utils.write_string_to_file(k_location, str(K))
    return K


MODE_SEND = 'MODE_SEND'
MODE_RECEIVE = 'MODE_RECEIVE'

# https://docs.python.org/2/howto/argparse.html
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--send', help='send an encrypted email', action='store_const', const=MODE_SEND)
parser.add_argument('-r', '--receive', help='receive encrypted email', action='store_const', const=MODE_RECEIVE)
parser.add_argument('-k', '--key', help='user xtea password', required=True)
parser.add_argument('-u', '--user', help='user email address', required=True)
parser.add_argument('-m', '--message', help='receiver and message', nargs=2)

# parser.parse_args('c --foo a b'.split())
args = parser.parse_args()
s = args.send == MODE_SEND
r = args.receive == MODE_RECEIVE

k = args.key
user = args.user

if s:
    m_recipient = args.message[0]
    m_message = args.message[1]
    send(user, k, m_recipient, m_message)
elif r:
    receive(user, k)
