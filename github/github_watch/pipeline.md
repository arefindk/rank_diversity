Pipeline for project:

First do the bigquery. But remember to transfer them to a destination table and check the option to allow large resutls. example for project_watch_nofork:
```
SELECT
  repository_name, repository_watchers, repository_language, 
  repository_organization, actor_attributes_login, created_at, repository_owner
	FROM [githubarchive:github.timeline]
WHERE type="WatchEvent" AND repository_fork = "false"
```
Then transfer them to the bucket from the gitnet table. Use the JSON, with GZIPPED. For multiple file use a destination like this:
```
gs://mishuk_gitnet/project_watch_nofork/project_watch_nofork*.gzip
```
Then download them using gsutil. When there are a lot of files use -m to parallelizing the download. An example gsutil  command:
```
gsutil -m cp gs://mishuk_gitnet/project_watch_nofork/* .
```
Then extract all the gzip and change the extracted filenames to json using the following command:
```
find . -type f -exec mv '{}' '{}'.json \; 
```
Now use a sh script to take them inside mongodb. An example can be found here:

http://blog.syedarefinulhaque.com/my-mongodb-scratchpad/

Then convert all text date field to ISODate using similar scripts to the following example:
```
db.gt_watch_nofork.find().forEach(function(doc) { 
doc.created_at = new Date(doc.created_at.replace(/-/g, '/'));  
db.gt_watch_nofork.save(doc);  
})
```
Also convert all the string “repository_watchers” to integers.
```
db.gt_watch_nofork.find({repository_watchers:{$type:"string"}}).forEach(function(doc) { 
doc.repository_watchers = parseInt(doc.repository_watchers);  db.gt_watch_nofork.save(doc);  
})
```