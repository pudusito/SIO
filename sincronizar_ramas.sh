for branch in $(git branch -r | grep -vE 'HEAD|master|main'); do
  git branch --track "${branch#origin/}" "$branch" 2>/dev/null
done