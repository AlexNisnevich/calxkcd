# Instructions
# ------------
# - Install python3, pyskein, and requests
# - Run this script with python3
#
# In latest Ubuntu / Debian / Mint:
# 	sudo apt-get install python3-dev python3-pip
# 	sudo python3-pip install requests
# 	sudo python3-pip install pyskein
# 	python3 calxkcd.py

from skein import skein256, skein512, skein1024
import requests
import random
import itertools

target = '5b4da95f5fa08280fc9879df44f418c8f9f12ba424b7757de02bbdfbae0d4c4fdf9317c80cc5fe04c6429073466cf29706b8c25999ddd2f6540d4475cc977b87f4757be023f19b8f4035d7722886b78869826de916a79cf9c94cc79cd4347d24b567aa3e2390a573a373a48a5e676640c79cc70197e1c5e7f902fb53ca1858b6'

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

def get_random_string():
	slen = random.randint(2, 200)
	return ''.join(random.choice(alphabet) for _ in range(slen)).encode('ascii')

def hamming_dist(hex_str1, hex_str2):
	def hex_to_bytes(hex_str):
		size = len(hex_str) * 4
		return ( bin(int(hex_str, 16))[2:] ).zfill(size)

	bytes1 = hex_to_bytes(hex_str1)
	bytes2 = hex_to_bytes(hex_str2)
	return sum(map(str.__ne__, bytes1, bytes2))

best_dist = 1024
while True:
	string = get_random_string()

	h = skein1024(string)
	dist = hamming_dist(h.hexdigest(), target)
	if dist < best_dist:
		best_dist = dist
		print(string, dist)

		# send to xkcd and print response (for sanity check)
		r = requests.post("http://almamater.xkcd.com/?edu=berkeley.edu", data={'hashable': string})
		print(r.content)
