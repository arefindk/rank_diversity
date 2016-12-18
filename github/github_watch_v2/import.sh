FILES=/Users/arefindk/development/datasets/github_rank_watch/*  
for f in $FILES  
do  
  echo "Importing file $f..."
  mongoimport --db github_watch --collection gt_watch_no_fork --file $f
  echo "Done $f"
done  