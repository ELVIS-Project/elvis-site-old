import json

pks = [51, 52, 53, 54, 55, 56, 57, 58]

d1 =  {"model": "elvis.attachment", "pk":0, "fields": { "old_id": 50, "attachment":"movement1.xml", "description":"First movement" } }
d2 =  {"model": "elvis.attachment", "pk":0, "fields": { "old_id": 50, "attachment":"movement2.xml", "description":"Second movement" } }
d3 =  {"model": "elvis.attachment", "pk":0, "fields": { "old_id": 50, "attachment":"movement3.xml", "description":"Third movement" } }
d4 =  {"model": "elvis.attachment", "pk":0, "fields": { "old_id": 50, "attachment":"movement4.xml", "description":"Fourth movement" } }

for pk in pks:
	d1["pk"] = pk
	d2["pk"] = int(str(pk)+"001")
	d3["pk"] = int(str(pk)+"002")
	d4["pk"] = int(str(pk)+"003")
	print d1
	print d2
	print d3
	print d4