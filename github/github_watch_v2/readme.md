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