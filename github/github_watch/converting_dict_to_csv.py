import json
import csv

with open('project_watch_nofork_rank_distribution.json', 'r') as f:
	rank_dist_dict = json.load(f)

with open('github_watch_rank_distribution.csv', 'wo') as f:
	csvwriter = csv.writer(f)
	for key in sorted(map(lambda x: int(x), rank_dist_dict.keys())):
		csvwriter.writerow([ key,float(rank_dist_dict[str(key)])])

f.close()
