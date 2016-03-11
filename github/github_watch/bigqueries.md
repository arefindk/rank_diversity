**Query to get all watch events**
```
SELECT
  repository_name, repository_owner, created_at, payload_action, repository_language, actor_attributes_login
	FROM [githubarchive:github.timeline]
WHERE type="WatchEvent"
```