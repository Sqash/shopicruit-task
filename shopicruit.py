import sys
import urllib.request
import json

_defaultURL = "http://shopicruit.myshopify.com/products.json"

if(len(sys.argv) != 2):
    URL = _defaultURL
else:
    print("Url given: {}".format(sys.argv[1]))
    URL = sys.argv[1]

try:
    res = urllib.request.urlopen(URL)
    data = json.loads(res.readall().decode('utf-8'))
    print("Received data... Parsing for wallets and lamps")
except BaseException as e:
    print("Error occured while getting data: {}".format(str(e)))
    exit(1)

products = data["products"]
numProducts = 0
numBought = 0
taxableCost = 0
nonTaxCost = 0

for item in products:
    if (item["product_type"] == "Wallet") or (item["product_type"] == "Lamp"):
        numProducts += 1
        for v in item["variants"]:
            numBought += 1
            if v["taxable"]:
                taxableCost += float(v["price"])
            else:
                nonTaxCost += float(v["price"])
                print("non-taxable item!")

taxRate = 1.13
cost = taxableCost*taxRate + nonTaxCost

print("Buying {} variants of {} core products, you'd spend ${:.2f} including 13% tax".format(numBought, numProducts, cost, int((taxRate - 1)*100)))
