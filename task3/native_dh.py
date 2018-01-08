import base64
import sys
import argparse
import xtea
import utils
import diffiehellmann
import os.path
import random
import datetime
import time


def send(user, recipient, message_sent):
    """
    sending mail
    :param user: sender email address
    :param password: with password
    :param recipient: recipient email address
    :param message_sent: content
    :return: None
    """
    print("sending... ")
    print("text: " + str(message_sent))

    user_short = short_from_mail(user)
    recipient_short = short_from_mail(recipient)

    if not os.path.exists(user_short):
        os.makedirs(user_short)

    if not os.path.exists(recipient_short):
        os.makedirs(recipient_short)

    # try to calculate K with Diffie Hellmann
    key = diffie_hellmann_key(user, recipient)

    # key could not be generated --> we don't have enough data to generate K
    if not key:
        # private key location
        private_key_location = user_short + "/" + user_short + "_private.txt"
        # generate public key
        A = diffiehellmann.get_public_key(int(utils.getStringFromText(private_key_location)))

        # if Diffie-Hellmann is not initialized: we send our public key instead of the original message
        message_sent = "DH:" + user + ":" + str(A)
        print("text changed to: " + str(message_sent))
    else:
        # if we can calculate K, Diffie-Hellmann is initialized --> we can encrypt with XTEA
        message_sent = xtea_crypt(str(key), message_sent, True)
        print("xtea: " + str(message_sent))

    # Base64
    base64_ecnoded_msg = base64.encodestring(message_sent)
    print ("encrypted: " + str(base64_ecnoded_msg))

    # add timestamp to each mail
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%y-%m-%d_%H:%M:%S')
    utils.write_string_to_file(recipient_short + "/mail_" + user + "_" + timestamp + ".txt", base64_ecnoded_msg)


def short_from_mail(mail):
    return mail.split("@")[0]


def receive(user):
    """
    receive all E-Mails
    :param user: user email address
    :param password: password
    :return:
    """
    # all new mails (no "read"-prefix)
    prefixed = [filename for filename in os.listdir(short_from_mail(user)) if filename.startswith("mail")]

    print "receiving... \nfound " + str(len(prefixed)) + " new mails"

    for mail in prefixed:
        # read mail content
        text = utils.getStringFromText(short_from_mail(user) + "/" + mail)
        print("read: " + str(text))

        # sender account
        account2 = mail.split("_")[1]

        text = base64.decodestring(text)
        print("received message: " + str(text))

        # rename to mark as read
        os.rename(short_from_mail(user) + "/" + mail, short_from_mail(user) + "/read_" + mail)

        # if mail belogs to Diffie-Hellman exchange
        if text.startswith("DH:"):
            splitted = text.split(":")
            account = splitted[1]
            key = splitted[2]
            print "found new public key " + key + " for account " + account
            if save_dh(user, account, key):
                print "Replying own public key..."
                send(user, account, "DH OK")
        else:
            key = diffie_hellmann_key(user, account2)
            decrypted = xtea_crypt(str(key), text, False)
            print("decrypted: " + str(decrypted))


def xtea_crypt(password, text, enc):
    passhash = utils.generate_key(password)
    iv = passhash[len(passhash) - 8:]
    password = passhash[48:]
    return xtea.crypt(password, text, iv, enc=enc)


def save_dh(my_account, other_account, key):
    location = short_from_mail(my_account) + "/" + short_from_mail(other_account) + "_public.txt"
    if os.path.isfile(location):
        dh = read_dh(my_account, other_account)
        print "public key for account " + other_account + " already known: " + str(dh)
        return False
    print "saving dh K in file " + location
    utils.write_string_to_file(location, key)
    return True


def read_dh(my_account, other_account):
    location = short_from_mail(my_account) + "/" + short_from_mail(other_account) + "_public.txt"
    if os.path.isfile(location):
        return int(utils.getStringFromText(location))

    return None


def diffie_hellmann_key(account1, account2):
    account1_short = short_from_mail(account1)
    private_key_location = account1_short + "/" + account1_short + "_private.txt"
    k_location = account1_short + "/" + account1_short + "_" + short_from_mail(account2) + "_sharedkey.txt"

    B = read_dh(account1, account2)

    # setup
    if not os.path.isfile(private_key_location):
        private_key = random.randint(0, 1000)
        utils.write_string_to_file(private_key_location, str(private_key))
        print("secure messaging is not set up. Please check mails in account " + account2 + " and reply with own public key")

        if B:
            B = int(B)
            write_dh_k(private_key, B, k_location)
            return False

    if not B:
        return False
    elif os.path.isfile(k_location):
        return int(utils.getStringFromText(k_location))
    else:
        a = int(utils.getStringFromText(private_key_location))
        B = int(B)
        return write_dh_k(a, B, k_location)


def write_dh_k(a, B, location):
    K = diffiehellmann.get_k(a, B)
    print "calculating K = " + str(K) + " from " + str(a) + " and " + str(B)
    utils.write_string_to_file(location, str(K))
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
    send(user, m_recipient, m_message)
elif r:
    receive(user)
