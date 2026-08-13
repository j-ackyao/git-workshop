

### 1. Checking out feature branch

Make sure you're currently on `main`. 
Branch from `main` into a feature branch.

<details>
<summary>Hint</summary>

```bash
git checkout -b feature-mainpy
```
</details>

### 2. Creating and tracking `main.py`

Create a file `src/main.py`. 

Import the function `build()` from module `builder` and call it.

<details>
<summary>Hint</summary>

```python
# src/main.py
from builder import build

build()
```
</details>
<br/>

Now track and stage `main.py`.

<details>
<summary>Hint</summary>

```bash
git add src/main.py
```
</details>

### 3. Configuring `.gitignore` and commiting

Run `main.py`, and then run `git status`. You should see untracked directories be generated.

Create a file `.gitignore` at the repo root. Ignore these new untracked directories. Add this `.gitignore`.

<details>
<summary>Hint</summary>

```
# .gitignore
*/build/
*/__pycache__/
```
```bash
git add .gitignore
```
</details>
<br/>

Run `git status` again, you should only see `src/main.py` and `.gitignore` staged with no untracked files. Make your commit.

<details>
<summary>Hint</summary>

```bash
git commit -m "Added main.py and .gitignore"
```
</details>

### 4. Merging and addressing conflict

Change branches back to `main` and merge your feature branch.

<details>
<summary>Hint</summary>

```bash
git checkout main
git merge feature-mainpy
```
</details>
<br/>

You should see an error, prompting that a conflict has happened in `src/main.py`.
```
Auto-merging src/main.py
CONFLICT (add/add): Merge conflict in src/main.py
Automatic merge failed; fix conflicts and then commit the result.
```

You can also see the unmerged files with `git status`.

Resolve the merge conflict and double check the code still works.

<details>
<summary>Hint</summary>

Since your current branch is `main` and you are attempting to merge your feature branch, changes in `main` are indicated by `HEAD`, while your changes are indicated by the feature branch name.

Adopt either `HEAD` or your own changes. Alternatively, you could rewrite the file (highly not recommended). Save your changes in `main.py` with your editor, then stage and continue the conflict resolution:

```bash
git add src/main.py
git merge --continue
```

</details>
<br/>
