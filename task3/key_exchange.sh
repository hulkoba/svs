#!/bin/bash

echo
echo "======================================================="
echo "Alice sends Bob the message \"Live long and prosper\""
echo
python2 native_dh.py -s -k pass -u "alice@mail.org" -m "bob@mail.org" "Live long and prosper"

echo
echo "======================================================="
echo "Bob checking his mails"
echo
python2 native_dh.py -r -k pass -u "bob@mail.org"

echo
echo "======================================================="
echo "Alice checking her mails"
echo
python2 native_dh.py -r -k pass -u "alice@mail.org"

echo
echo "======================================================="
echo "Alice sends Bob the message \"Live long and prosper\""
echo
python2 native_dh.py -s -k pass -u "alice@mail.org" -m bob@mail.org "Live long and prosper"