from tinydb import TinyDB, Query
import jellyfish
import re


def finder(data):

	data = re.match(r"\[@AniPlus\](.*)\[.*\]\.mkv", data.split("/")[-1])
	target = "Senpai ga Uzai Kouhai"
	diff = jellyfish.jaro_distance(target, data.group(1))



	if diff > 0.75:
		return True
	

q = Query()
db = TinyDB("database/db.json")
search = db.search(q.href.test(finder))


for i in search:
	data = i['href'].split("/")[-1]
	data = data.replace("%20", " ")
	print(data)

# for k in db:

# 	data = k['href'].split("/")[-1]
# 	data = data.replace("%20", " ")


# 	print(data)


print("Length:", len(search))