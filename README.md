# main-deep-dive

This workshop is to familiarize with rebasing and getting comfortable to modifying commit history.

Could all of these be done with changes in a regular commit? Yeah...

Is it cooler to use rebase though? Yeah!!!

More importantly, rebase keeps the commit history clean, so when the time comes to fix real mess-ups, it'll be a lot simpler!

### 0. Rebase to update branch

Our new branch `main-deep-dive` was branched off `main-deep-dive-base`. There has been some commits pushed to our base and we should get those commits into our branch by rebase.

Update the branch `main-deep-dive` by rebase.

<details>
<summary>Solution</summary>

Checkout into `main-deep-dive` and run `git rebase main-deep-dive-base`.

If you haven't checked out `main-deep-dive-base`, then you can use `origin/main-deep-dive-base` instead.

</details>

### 1. Cleaning up documentation commits

Someone decided to make a bunch of commits just to write one file documentation!

Let's fix this by squashing all of the commits that begin with `doc`, and give it a more appropriate commit message.

<details>
<summary>Solution</summary>

Run `git rebase -i --root` and squash the latter two (don't squash the first commit!).

Give it a more appropriate commit message.

</details>

### 2. Removing a bad commit

You've found out your intern pushed a commit that overrides your work on `src/main.py`!

Luckily, you have permission to force-push on `main`, which allows you to change the commit history.

Remove the commit that your intern made with `rebase`.

<details>
<summary>Solution</summary>

Run `git rebase -i --root` and drop the intern's commit.

</details>

### 3. Reintroduce deleted file

Shoot, you realized your intern actually included a useful `.gitignore` file, which was a part of the commit you removed.

Bring back the file by `checkout`, then make a new commit to add it.


<details>
<summary>Hint</summary>

If you didn't manage to catch the commit hash, you can use `git log --all --reflog --oneline`.

</details>

<details>
<summary>Solution</summary>

Using the commit hash, run `git checkout <hash> -- .gitignore`.

There should be an unstaged file, stage it and commit.

</details>

### 4. Undoing changes in commit

Your colleague recently pushed a commit to prepare a new functionality in your codebase, but it's not ready yet! In `main.py`, it should be calling `build()` with all default parameters, but your colleague accidentally used `build(False)`.

Learning from your mistakes, you decide to edit the commit through rebase.

Fix the commit with `rebase`.


<details>
<summary>Solution</summary>

Run `git rebase -i --root`, find the commit and edit.

Instead of manually making the changes in `main.py`, you realize you can just undo the changes to that file only.
```bash
git reset HEAD~ -- src/main.py # "Unstages" changes to that file only, you'll notice the only changes made was `build(False)`
git restore src/main.py # Undoes the unstaged changes
git add src/main.py
git commit --amend # Remember, you are altering the existing commit, so you should amend, not a regular commit
git rebase --continue
```
</details>
