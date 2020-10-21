## Development Guide
For a more detailed guide, check out check out [Github's guide](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

#### Saving Credentials
Check out https://dirask.com/posts/Git-save-password-under-windows-gp52xj. The first method is preferred.

#### Latest Commits
Make sure you have the latest commits
- `git fetch origin`
- `git rebase origin/master`

or the one liner (equivalent to the above)
- `git pull --rebase origin master`

Make sure your dependencies are updated
- `pip install -r requirements.txt`

#### Making Changes
You should always be on your own branch when making any changes.

Write some code, and once you're happy
- Commit your changes: `git add, git commit` ([Atlassian guide](https://www.atlassian.com/git/tutorials/saving-changes/git-commit))
- Push your changes to your local branch: `git push origin HEAD` (HEAD points to your own branch)
- Go to the Github repo and make a pull request. If you've just pushed to your own branch, you should see it under "recently pushed" on the master branch
- Wait for it to be merged

#### Conflicts
See: https://www.atlassian.com/git/tutorials/using-branches/merge-conflicts

Because everyone adds commands to a central file (`cli.py`), it's inevitable you'll run into merge (rebase) conflicts.
`error: Pulling is not possible because you have unmerged files.`

You'll first need to figure out which files have pending merges. It's usually just `cli.py`.
`git ls-files -u`

Open the pending files. If you're lucky, it's already settled automatically (Your code and someone else's code is both present). If not, you'll see something like this.
```
<<<<<<< HEAD
this is some content to mess with
content to append
=======
totally different content to merge later
>>>>>>> new_branch_to_merge_later
```

What you'll need to do is get rid of these symbols ">>> ==== <<<" and the following text. You'll want to manually edit this file so that it reflects both your changes and someone else's. Once you're done, add the file and commit with an appropriate message.
`git add <yourfile>`  
`git commit -m "Resolve rebase conflicts`

Then, you can continue on with your rebase.
`git rebase --continue`
