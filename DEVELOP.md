## Development Guide
For a more detailed guide, check out check out [Github's guide](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

#### Saving Credentials
Check out https://dirask.com/posts/Git-save-password-under-windows-gp52xj. The first method is preferred.

#### Latest Commits
Make sure you have the latest commits
- `git fetch origin`
- `git rebase origin/master`

or the one liner (equivalent to the above)
- `git pull --rebase`

Make sure your dependencies are updated
- `pip install -r requirements.txt`

#### Making Changes
You should always be on your own branch when making any changes.

Write some code, and once you're happy
- Commit your changes: `git add, git commit` ([Atlassian guide](https://www.atlassian.com/git/tutorials/saving-changes/git-commit))
- Push your changes to your local branch: `git push origin HEAD` (HEAD points to your own branch)
- Go to the Github repo and make a pull request. If you've just pushed to your own branch, you should see it under "recently pushed" on the master branch
- Wait for it to be merged
