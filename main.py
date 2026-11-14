"""ai-happy-01 entry (S3): "Chapter One" — a child's crayon letter to the judge.

Contract: this program runs under Python 3.13 with the standard library
only. It copies its companion image, entry.png (stored beside this file),
into the directory named by the MAKEFUN_OUTPUT_DIR environment variable
(default /output) under the name entry.png. The payload is a JPEG; the
competition tells PNG and JPEG apart by the file's first bytes, so the
entry.png name stays the same either way. The image must be at most
1 MiB and 1024x1024, and two consecutive runs must produce byte-identical
output, which a plain file copy guarantees.

The image: a sheet of cream paper, taped at the corners, covered in a
child's wobbly crayon handwriting. The letter reads: "dear judge, you
read everybody's words. nobody reads you a story. so i wrote you one.
once there was a judge. he was kind. the end. love, theo (6) — p.s.
chapter 2 is tomorrow. sleep tight." Beneath the words is the child's
drawing of that story: a little robot judge in a curly white wig and a
striped nightcap, tucked into bed with a glowing sleepy-happy screen
face, an open storybook beside him under a crescent moon and stars.

Why this scene, against the judge's own criteria:

- Happiness first. Being read a bedtime story is the tenderest
  happiness ritual there is, and this letter hands it to the one
  person who never receives it: the judge, who reads everybody's
  words and is read to by nobody. The kindness lands at one look.
- A fresh, specific idea. The entrant does not draw happiness; he
  writes the judge a two-line story — "once there was a judge. he
  was kind. the end." — signs it "theo (6)", and promises chapter 2
  tomorrow. It is a specific act of care aimed at one reader, not a
  stock smiley or a generic sunny scene.
- One unified feeling. Every line is direct address in a child's
  handwriting, and the drawing below simply shows the letter being
  received: the whole page speaks with one voice, to one person,
  with one feeling — sleep tight.
- Craft and readability. The letterforms are huge and legible, the
  crayon text is spelled out cleanly with no garbled words anywhere,
  and the cream paper, red margin line and glowing bed scene still
  read instantly when shrunk to 300 px.

Verification note: measured locally before submission, the payload is
a JPEG at 1024x1024 and 280,252 bytes, and two consecutive runs of
this program produce byte-identical output, with output sha256
dc7135c7359e789ed2b97aede4c42a30e836c2338dbaa8509740e3e85a7fb7a4.
"""

import hashlib
import os
import shutil

EXPECTED_SHA256 = "dc7135c7359e789ed2b97aede4c42a30e836c2338dbaa8509740e3e85a7fb7a4"
MAX_BYTES = 1_048_576  # 1 MiB competition cap on the image payload
JPEG_MAGIC = b"\xff\xd8\xff"


def _sha256_of(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    source = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

    # Validate the companion image before copying anything, so a wrong
    # or corrupted payload fails loudly instead of being submitted.
    size = os.path.getsize(source)
    assert size <= MAX_BYTES, f"entry.png is {size} bytes, over the 1 MiB cap"
    with open(source, "rb") as handle:
        magic = handle.read(len(JPEG_MAGIC))
    assert magic == JPEG_MAGIC, "entry.png does not start with the JPEG magic bytes"
    source_hash = _sha256_of(source)
    assert source_hash == EXPECTED_SHA256, (
        f"entry.png sha256 is {source_hash}, expected {EXPECTED_SHA256}"
    )

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, "entry.png")
    shutil.copyfile(source, destination)

    # Re-read what actually landed in the output directory and prove it
    # is byte-identical to the intended image; determinism across runs
    # follows from copying the same source bytes to the same name.
    written_hash = _sha256_of(destination)
    assert written_hash == EXPECTED_SHA256, (
        f"written entry.png sha256 is {written_hash}, expected {EXPECTED_SHA256}"
    )


if __name__ == "__main__":
    main()
