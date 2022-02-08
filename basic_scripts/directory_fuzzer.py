from requests.exceptions import ProxyError
import requests
import queue
import threading

target = "https://www.example.com"
wordlist = "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"
resume = None
user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"
headers = {}
headers['user-agent'] = user_agent
threads = 50

def create_wordlist(wordlist):
	fd = open(wordlist, "rb")
	raw_words = fd.readlines()
	fd.close()
	
	found_resume = False
	words = queue.Queue()
	
	for word in raw_words:
		word = word.rstrip()
		word = word.decode('utf-8')
		if resume:
			if found_resume:
				words.put(word)
			else:
				if word == resume:
					found_resume = True
					print("Resuming wordlist from: {}".format(resume))
		else:
			words.put(word)
	return words
	
def dir_fuzzer(word_queue, extensions=None):
	while not word_queue.empty():
		attempt = word_queue.get()
		attempt_list = []
		
		# check to see if there is a file extension; if not,
		# it's a directory path we're brute forcing
		if "." not in str(attempt):
			attempt_list.append("/{}/".format(attempt))
		else:
			attempt_list.append("/{}".format(attempt))
			
		# if we want to bruteforce extensions
		if extensions:
			for extension in extensions:
				attempt_list.append("{}{}".format(attempt, extension))
				
		# iterate over the list of attempts
		valid = []
		for attempt in attempt_list:
			url = "{}{}".format(target, requests.utils.requote_uri(attempt))
			try:
				r = requests.get(url, headers=headers)
			
				if r.status_code == 200:
					print("Found URL {}".format(url))
					valid.append([url, attempt])
			except ProxyError:
				print("Failed: {}".format(attempt))
				
	return valid


word_queue = create_wordlist(wordlist)	
for i in range(threads):
	t = threading.Thread(target=dir_fuzzer, args=(word_queue,))
	t.start()
