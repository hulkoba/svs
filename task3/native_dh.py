from utils import *
from rsa import *
import base64
import sys

mail_a_to_b = "./mails/mail_alice_to_bob.txt"
mail2 = "./mails/mail_bob_to_alice.txt"
alice = "alice"
bob = "bob"

def menu(is_logged_in=False, username=None, password=None):
    if not is_logged_in:
        username = raw_input("Welcome to pyMail! Please log in to send and receive E-Mails! \nUsername: ").lower()
        assert (username in [alice, bob], "username should be " + alice + " or  " + bob)
        password = raw_input("Please enter your password: ")

    other_user = bob if username is alice else alice

    choice = input("\nWhat do you want to do? \n"
                   "1 --> Log out \n2 --> Send Mail to " + other_user + "\n3 --> check for new mail \n>")

    if choice is 1:
        username = None
        menu(False)
    if choice is 2:
        menu(True, username, password)
    if choice is 3:
        menu(True, username, password)


menu()
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
