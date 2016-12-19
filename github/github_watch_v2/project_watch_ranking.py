from pymongo import MongoClient
import pprint as pp
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

client = MongoClient("mongodb://localhost:27017/")
db = client.github_watch
gt_watch = db.gt_watch_no_fork

lowDate = dt.datetime(2012,04,01)
highDate = dt.datetime(2014,12,31)

doc = gt_watch.find_one()
pp.pprint(doc)

pipeline_watch = [{"$match":{"created_at":{"$gt":lowDate,"$lt":highDate},"repository_name":{"$exists":True}}},\
			{"$group":{"_id":{"project":"$repository_name","year":{"$year":"$created_at"},"month":{"$month":"$created_at"},"date":{"$dayOfYear":"$created_at"}},"cnt":{"$sum":1}}},\
			{"$sort":{"cnt":-1}},\
			{"$sort":{"_id.date":1}},\
			{"$sort":{"_id.year":1}}]#,\
			# {"$limit":5000}]

results = gt_watch.aggregate(pipeline_watch, allowDiskUse=True)

running_day = 0
last_day = 0
max_number_of_ranks = 0
rank_dict = defaultdict(list)
current_rank_list = list()
rank_list = list()
current_pipeline_key = 'project'

results = gt_watch.aggregate(pipeline_watch, allowDiskUse=True)

for result in results:
	## First find out the current day of the year, then for a single day of the year get all the 
	#projects with their count of watch event. Create a tuple of (watchcount, projectname). 
	#Then sort the tuple by the count and for all the projects in the sorted list add the in a 
	#dictionary that has the rank as the keys and list of project names for each rank as the 
	#values, e.g. {1: ['project a', 'project b'], 2:['project c, project b']}
	year_current_document = result["_id"]["year"]
	day_current_document = result["_id"]["date"]
	month_current_document = result["_id"]["month"]
	project_current_document = result["_id"]["project"]
	count_project_current_document = result['cnt']
	print year_current_document, month_current_document,day_current_document, project_current_document, count_project_current_document
	current_watchcount_project_tuple = (count_project_current_document, project_current_document)
	if day_current_document != last_day:
		last_day = day_current_document
		running_day += 1
		#print "running_day", running_day
		current_rank_list = sorted(current_rank_list, reverse = True)
		#print current_rank_list
		for rank_enumerated in enumerate(current_rank_list):
			#print rank_enumerated
			rank_dict[rank_enumerated[0]].append(rank_enumerated[1][1])
		current_rank_list = list()
		current_rank_list.append(current_watchcount_project_tuple)
	else:
		current_rank_list.append(current_watchcount_project_tuple)
print rank_dict
rank_change_distribution = {}
for k,v in rank_dict.items():
	prob = len(set(v)) / float(len(v))
	rank_change_distribution[k] = prob
print rank_change_distribution
# rankChangeDistribution = np.array(rankChangeDistribution)
# # rankChangeDistribution = rankChangeDistribution / float(len(rankList)) # I am dividing the number changes for each rank by the total number of time periods here.

plt.plot(rank_change_distribution.keys(), rank_change_distribution.values(), 'r--')
#plt.xscale('log')
plt.savefig("enron_rank.pdf")
plt.show()

