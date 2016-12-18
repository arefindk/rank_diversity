## Changes in githubarchive bigquery

The previous flattened version of githubarchive timeline in bigquery has been removed and they are using the json format of only required field as either 'payload' or 'other' field.

The significant informations are found in the 'payload' field where the table is before 2012-03 and starting from 2012-04, the significant information will be found in the other field.


## Running the query in bigquery and append all the necessary information to a single table

Here is one of all the queries:

```
SELECT
  created_at,
  repo.name AS repository_name,
  JSON_EXTRACT(other, '$.repository.watchers') AS repository_watchers
FROM
  [githubarchive:month.201204] 
WHERE
  JSON_EXTRACT(other, '$.repository.fork') == "false"
  AND type == "WatchEvent"
```

To allow large results, I created a dataet named watch and add the option to append to table with the table name "watch_no_fork".

I ran these queries manually by changing the month from 201204 to 201612. I could do the changing programmatically by using table-query regex of bigquery, but didn't bother. 

The strange thing is that there is no "WatchEvent" found after 201412. Maybe they have changed the name of the watch even into something else after this time period.

## Transfer the table to the local machine

Transfer the table to the bucket from the gitnet table. Use the JSON, with GZIPPED. For multiple file use a destination like this:

```
gs://mishuk_gitnet/project_watch_nofork/project_watch_nofork*.gzip
```

Now, to get them in your local machine, first install `gsutil`.

Then download them using gsutil. When there are a lot of files use -m to parallelize the download. An example gsutil command:

```
gsutil -m cp gs://mishuk_gitnet/project_watch_nofork/* .
```

Now extract all the gzip and remove the gzipped files:

```
rm *.gzip
```

Change the extracted filenames to json using the following command:

```
find . -type f -exec mv '{}' '{}'.json \; 
```

## Inserting into mongodb:
Use a sh script to take them inside mongodb. An example can be found [here](http://blog.syedarefinulhaque.com/my-mongodb-scratchpad/):

```
FILES=/Users/arefindk/development/datasets/github_rank_watch/*  
for f in $FILES  
do  
  echo "Importing file $f..."
  mongoimport --db github_watch --collection gt_watch_no_fork --file $f
  echo "Done $f"
done
```

