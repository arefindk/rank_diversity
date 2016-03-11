**Converting all string date fields into ISO-date fields**
```
db.gt_watch.find().forEach(function(doc) { doc.created_at = new Date(Date.parse(doc.created_at.toString())); db.gt_watch.save(doc); })
```