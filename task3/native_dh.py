import base64
import sys
import argparse

def send(password, recipient, message_sent):
    print ("sending")



def receive(password):
    print ("receiving")


MODE_SEND = 'MODE_SEND'
MODE_RECEIVE = 'MODE_RECEIVE'

# https://docs.python.org/2/howto/argparse.html
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--send', help='send an encrypted email', action='store_const', const=MODE_SEND)
parser.add_argument('-r', '--receive', help='receive encrypted email', action='store_const', const=MODE_RECEIVE)
parser.add_argument('-k', '--key', help='xtea password', required=True)
parser.add_argument('-m', '--message', help='email and message', nargs=2)

# parser.parse_args('c --foo a b'.split())
args = parser.parse_args()
s = args.send == MODE_SEND
r = args.receive == MODE_RECEIVE
k = args.key
m_recipient = args.message[0]
m_message = args.message[1]

if send:
    send(k, m_recipient, m_message)
elif receive:
    receive(k)



'''
mail_a_to_b_string = read_file_to_string(mail_a_to_b)

mail_a_to_b_encoded = base64.b64encode(mail_a_to_b_string)

print(mail_a_to_b_encoded)

mail_a_to_b_bin = getBytesFromText(mail_a_to_b_encoded)

mail_a_to_b_binarynum = ''.join(mail_a_to_b_bin)

print(mail_a_to_b_binarynum)

p = 0
g = 0

a = get_a(mail_a_to_b_binarynum)
'''
