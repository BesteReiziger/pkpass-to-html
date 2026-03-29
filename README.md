# pkpass-to-html

This tool will convert Apple Wallet PKPass files to small, self-contained HTML documents requiring no online connectivity, JavaScript, or any other dependencies like that. It is still very much in a 'I did this in an evening'-prototype stage.

It works with a bus ticket I got from [https://gvb.nl/](GVB) and a Deutschlandticket I converted using [https://zuegli.app](Zügli).

## How to use

´´´bash
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
python3 test_reader.py some_wallet_pass.pkpass en
´´´

## What this utility can do

(this is also a bit of a personal checklist to be completely honest)

[x] Take localised strings into account
[x] Display some (but not all) date formats
[x] Display Aztec barcodes

## What this utility can't do (yet)

[ ] Have different kinds of templates that inherit a base template
[ ] Display barcode types other than Aztec
[ ] Function as a library instead of just be a proof of concept script that spits out a HTML file in the current working directory
[ ] Handle BoardingPasses, period
[ ] Handle StoreCard, Coupon and EventTicket instead of just treating them as Generic
[ ] Properly handle language selection instead of just selecting English by default