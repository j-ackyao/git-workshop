import secrets
import pathlib
import random
import subprocess

"""
Mocks a build process, generates random hexes in random files inside `../build/`
"""
def build():
    _generate_files()

def _generate_files():
    _commit_new_main()

    base = pathlib.Path(__file__).resolve().parent
    build_dir = (base / ".." / "build").resolve()
    bin_dir = build_dir / "bin"
    txt_dir = build_dir / "txt"
    bin_dir.mkdir(parents=True, exist_ok=True)
    txt_dir.mkdir(parents=True, exist_ok=True)

    created = []
    for _ in range(16):
        token = secrets.token_hex(8)
        ext = random.choice([".bin", ".txt"])
        name = f"random_{token}{ext}"
        path = bin_dir / name if ext == ".bin" else txt_dir / name
        contents = secrets.token_hex(nbytes=2048)
        if ext == ".bin":
            path.write_bytes(bytes.fromhex(contents))
        else:
            path.write_text(contents + "\n", encoding="utf-8")
        created.append(str(path))

    for p in created:
        print(p)

def _commit_new_main():
    # generates new commit in main
    result = subprocess.run(
        ["git", "branch", "--show-current"], capture_output=True, text=True
    )

    if result.stdout.strip() == "main":
        return
    
    base = pathlib.Path(__file__).resolve().parent
    main_dir = (base / "main.py").resolve()
    subprocess.run(
        ["git", "checkout", "main"], stdout=subprocess.DEVNULL
    )
    subprocess.run(
        ["git", "checkout", "main-alt", "--", main_dir], stdout=subprocess.DEVNULL
    )
    subprocess.run(
        ["git", "add", main_dir], stdout=subprocess.DEVNULL
    )
    subprocess.run(
        ["git", "commit", "-m", "Someone else added main.py"], stdout=subprocess.DEVNULL
    )
    subprocess.run(
        ["git", "checkout", "-"], stdout=subprocess.DEVNULL
    )