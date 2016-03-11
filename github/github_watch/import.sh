FILES=/Users/arefindk/datasets/github_rank/project_watch_nofork/*
for f in $FILES
do
  echo "Importing file $f..."
  mongoimport --db github_watch --collection gt_watch_nofork --file $f
  echo "Done $f"
done