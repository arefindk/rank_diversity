FILES=/Users/arefindk/datasets/github_watch/*
for f in $FILES
do
  echo "Importing file $f..."
  mongoimport --db github_watch --collection gt_watch --file $f
  echo "Done $f"
done