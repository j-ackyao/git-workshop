import secrets
import pathlib
import random

"""
Mocks a build process, generates random hexes in random files inside `../build/`
"""
def build(use_hex: bool = True):
    _generate_files(use_hex)

def _generate_files(use_hex):
    base = pathlib.Path(__file__).resolve().parent
    error_path = (base / ".." / "build_errors.txt")

    if not use_hex:
        error_path.write_text("Not hex unsupported!")
        return

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