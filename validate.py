import subprocess
import sys
from pathlib import Path


def run_git(args):
    cp = subprocess.run(["git"] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return cp


def fail(msg):
    print(f"❌ {msg}")
    sys.exit(1)


def passed(msg):
    print(f"✅ {msg}")


def main():
    repo_root = Path(__file__).parent.resolve()

    # Step 1: verify branch 'feature-mainpy' exists
    cp = run_git(["show-ref", "--verify", "--quiet", "refs/heads/feature-mainpy"])
    if cp.returncode != 0:
        fail("Step 1: branch 'feature-mainpy' not found")
    passed("Step 1: branch 'feature-mainpy' exists")

    # Step 2: check src/main.py exists and is staged
    main_py = repo_root / 'src' / 'main.py'
    if not main_py.exists():
        fail("Step 2.1: 'src/main.py' does not exist")
    passed("Step 2.1: 'src/main.py' exists")

    # Step 3: check build/ generated, .gitignore created, and a commit was made including the files
    # 3.1 build directory exists somewhere
    build_path = None
    for p in repo_root.rglob('build'):
        if p.is_dir():
            build_path = p
            break
    if not build_path:
        fail("Step 3.1: no 'build' directory found in the repository")
    passed("Step 3.1: 'build' directory found")

    # 3.2 .gitignore exists
    gitignore = repo_root / '.gitignore'
    if not gitignore.exists():
        fail("Step 3.2: '.gitignore' does not exist")
    passed("Step 3.2: '.gitignore' exists")

    # 3.3 ensure 'build/' and 'src/__pycache__/' are ignored
    cp = run_git(["status", "--ignored", "--porcelain"])
    ignore_dirs = ["!! build/", "!! src/__pycache__/"]
    if not all(any(line.startswith(ignore) for line in cp.stdout.splitlines()) for ignore in ignore_dirs):
        fail(f"Step 3.3: autogen dirs aren't ignored properly")
    passed("Step 3.3: 'build/' and 'src/__pycache__/' are ignored")

    # Step 4: ensure we're on 'main', files still exist, working tree is clean, and no merge in progress
    # 4.1 check branch is main
    cp = run_git(["symbolic-ref", "--short", "-q", "HEAD"])  # quiet if HEAD is detached
    current_branch = cp.stdout.strip()
    if current_branch != "main":
        fail(f"Step 4.1: current branch is '{current_branch}' (expected 'main')")
    passed("Step 4.1: currently on 'main' branch")

    # 4.2 check files still exist
    if not main_py.exists() or not gitignore.exists():
        fail("Step 4.2: 'src/main.py' or '.gitignore' is missing")
    passed("Step 4.2: 'src/main.py' and '.gitignore' still exist")

    # 4.3 working tree clean
    cp = run_git(["status", "--porcelain"])
    if cp.returncode != 0:
        fail("Step 4.3: 'git status' failed")
    if cp.stdout.strip() != "":
        fail("Step 4.3: working directory is not clean (uncommitted changes present)")
    passed("Step 4.3: working directory is clean (no uncommitted changes)")

    # 4.4 no merge in progress (check MERGE_HEAD in git dir)
    cp = run_git(["rev-parse", "--git-dir"])
    if cp.returncode != 0:
        fail("Step 4.4: could not determine git directory")
    gitdir = Path(cp.stdout.strip())
    # If gitdir is relative, resolve against repo_root
    if not gitdir.is_absolute():
        gitdir = (repo_root / gitdir).resolve()
    merge_head = gitdir / 'MERGE_HEAD'
    if merge_head.exists():
        fail("Step 4.4: a merge is still in progress")
    passed("Step 4.4: no merge in progress")

    print('\nWorkshop passed! 🎉')


if __name__ == '__main__':
    main()
