## Unstage an added file in Git
If you added a file by mistake, you can unstage it (but keep local changes) by saying

> git reset HEAD path/to/file

## Adding an SSH key with:

// list the existing ssh-keys
> ssh-add -l 

// add the key
> ssh-add ~/Development/Github/newSSHMac

-------------------

Git aliases
https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases

---------------------

## Merge one branch into another (not master)
1. git commit and push the changes into the `myFeatureBranch` branch

2. Checkout to the branch into which we want to merge the changes from the other branch
> git checkout `development`

3. Merge the feature branch to the development branch
> git merge `myFeatureBranch`

Output: Fast-forward .. 

4. Push changes to the `development` branch:
> git push `origin` `development`

---------------------

## List all origin branches that exist
> git branch -a

----------------------

## Delete a PUSHED commit from the history and from the repo

If we have the following history:

```
commit 2219d1ed6da09c63da3c4855439d499dbf6f4f87 (HEAD -> master)
Author: adimi5 <anelia.dimitrova@nike.com>
Date:   Thu Jan 10 10:27:31 2019 +0100

    testing packages

commit 2abd0166a64847f1fd048b87ccc5dfd97994b7cf
Author: adimitrova <a.dimitrovaa@gmail.com>
Date:   Tue Nov 20 22:29:13 2018 +0100

    packaging, this went terribly wrong but still pushing

commit 6f96fe3275532185f8fb3fd80dce66f262e9d6ff
Author: adimitrova <a.dimitrovaa@gmail.com>
Date:   Fri Oct 5 11:32:44 2018 +0200

    packaging data
```

and want to get rid of the commit `2abd016` or skip the last 2 commits and revert to the third most recent one, then do
> git rebase -i HEAD~2

It will then give an option to remove a commit, like this:

```
pick 2abd016 packaging, this went terribly wrong but still pushing
pick 2219d1e testing packages

# Rebase 6f96fe3..2219d1e onto 6f96fe3 (2 commands)
```

If we delete the first line and `:wq` that commit will be gone from the log and history and form github

----------------------

## List all latest changes in a certain repo:

```
git for-each-ref --sort=-committerdate refs/heads/ refs/remotes --format='%(authordate:short) %(color:yellow)%(objectname:short) %(color:blue)%(refname:short)%(color:reset) | %(color:green)%(committerdate:relative)%(color:reset) => by%(color:red) %(committername)'
```

Setup an alias for it with:

```
git config --global alias.latest "for-each-ref --sort=-committerdate refs/heads/ refs/remotes --format='%(authordate:short) %(color:yellow)%(objectname:short) %(color:blue)%(refname:short)%(color:reset) | %(color:green)%(committerdate:relative)%(color:reset) => by%(color:red) %(committername)'"
```

Then use with 
`git latest`

----------------------

## Abort a merge in progress by keeping the last committed changes to the current branch:
Abort the current conflict resolution process, and try to reconstruct the pre-merge state.

If there were uncommitted worktree changes present when the merge started, `git merge --abort` will in some cases be unable to reconstruct these changes. It is therefore recommended to always commit or stash your changes before running git merge.

`git merge --abort` is equivalent to `git reset --merge` when  `MERGE_HEAD` is present.

```
git reset --merge 
```

------------------------

## Rename remote and local branches and push them:
Switch to the branch you want to rename:

```
git branch -m new-name
```

Delete the old-name remote branch and push the new-name local branch

```
git push origin :old-name new-name
```
Reset the upstream branch for the new-name local branch

```
git push origin -u new-name
```

------------------------

## Create a git alias for a command
__NB!__ The `git` command must not be part of the command to be aliased as it won't work. See below:

This command will do `git push origin [current_branch]`, so make sure to be on the branch to which you want to push, before using the command.

```text
git config --global alias.po "push origin $(git symbolic-ref --short HEAD)"
```

------------------------

## Git colourful tree log
![Tree](tree.png)

Similar to `mktree`, but with full history and generated much faster

```
git config --global alias.tree 'log --graph --abbrev-commit --decorate --all --format=format:"%C(202)%h%C(reset) - %C(198)%aD%C(yellow) - %an%C(reset) %C(green)(%ar)%C(reset)%C(bold yellow)%d%C(reset)%n %C(white)%s%C(reset)"'
```

All colour codes can be found [HERE](https://misc.flogisoft.com/_media/bash/colors_format/256_colors_fg.png)

Use with `git tree`

------------------------

## Custom git commands
#### Enable `git browse origin` command
This command opens the current repo in the browser with a custom script - SUPER COOL!

- Script originates from [HERE](https://github.com/santiaro90/dotfiles/blob/master/git/commands/git-browse), however I saved it in the current repo just in case. File name is `git-browse`

- [Original article](https://medium.com/@santiaro90/write-your-own-git-subcommands-36d08f6a673e)

Instructions:
-  Create a new file: `mkdir ~/.gitbin; touch ~/.gitbin/git-browse`

__NB!__: The file name __must__ start with `git`.

- `vi ~/.gitbin/git-browse` > press `i` to insert and paste the content of the `git browse` file.

-  press `Escape` and type `:wq`

- Add this to `~/.bashrc` or `~/.zshrc file`: 
> export PATH="$HOME/.gitbin:$PATH"

- In a repo, run `git browse origin` and it will open in the browser.

*** 

#### Enable live git logs
create a file in the `/.gitbin/git-loglive.sh` and paste the following code inside:

```shell
#!/bin/bash

while :
do
    clear
    git --no-pager log `git rev-parse HEAD` -n $* --graph --pretty=oneline --abbrev-commit --decorate
    sleep 1
done
```

CD to a git repo and run the command:
`sh ~/.gitbin/git-loglive.sh 25`
25 indicates how many lines it will show

---------------------

## Copy a file from one branch to another

Switch to the destination branch

```
git checkout destinationBranch
git checkout sourceBranchName myFile.txt
```

Or if the files are multiple with almost the same names and, say, different dates, do:

```
git checkout sourceBranchName data_dump_2020-05-*.csv
```

This will copy all files with dates in May in that branch and location
data_dump_2020-05-20.csv
data_dump_2020-05-21.csv
data_dump_2020-05.22.csv

-----------------------

## Cleanup local branches
Setup alias

```
git config --global alias.cleanup "branch | grep -v "development" | grep -v "master" | xargs git branch -D"
```

Then run:

```
git cleanup
OR
git branch | grep -v "development" | grep -v "master" | xargs git branch -D
```

__BETTER RUN: (to remove all local branches)__

```
git fetch --prune --all
```

1. list all the branches
2. From the list ignore the master and development branches and take the rest of the branches
3. delete the branch

---------------------------

## Re-map local branch to its new remote 
(if branches were deleted and swapped etc)

Using git v1.8.0 or later:

```
git branch branch_name --set-upstream-to your_new_remote/branch_name
```

Or you can use the -u switch:

```
git branch branch_name -u your_new_remote/branch_name
```

----------------

## Undo LOCAL changes made to a file

```
git checkout -- filename.txt
```

------------------

## Start ignoring a previously committed file

```sh
$ echo debug.log >> .gitignore
$ git rm --cached debug.log
rm 'debug.log'
$ git commit -m "Start ignoring debug.log"
```

----------------

## Git pull multiple repos at once
Instead of running cd repo_name >> git pull, 
run `multipull` from the parent directory!!!

But first, add this line to the `~/.zshrc` file and then source it

```sh
alias multipull="find . -mindepth 1 -maxdepth 1 -type d -print -exec git -C {} pull \;"
```
```
git branch branch_name --set-upstream-to your_new_remote/branch_name
```

Or you can use the -u switch:

```
git branch branch_name -u your_new_remote/branch_name
```

---------------------------

## Track who changed what in a given file:

```
git blame <filename>
```
