**Converting all string date fields into ISO-date fields**
```
db.gt_watch.find().forEach(function(doc) { 
	doc.created_at = new Date(doc.created_at.replace(/-/g, '/')); 
	db.gt_watch.save(doc); 
})
```
