import random
import tempfile
from pathlib import Path

from PIL import Image

from dupes import group, scan


def photo(seed):
    rng = random.Random(seed)
    small = Image.new("RGB", (8, 8))
    small.putdata([tuple(rng.randrange(256) for _ in range(3)) for _ in range(64)])
    return small.resize((800, 600), Image.BICUBIC)


def test_finds_resized_and_resaved_copies():
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "sub").mkdir()
        photo(1).save(d / "a.png")
        photo(1).resize((400, 300)).save(d / "sub" / "a_small.jpg", quality=40)
        photo(1).save(d / "a_copy.webp")
        photo(2).save(d / "b.png")
        photo(3).save(d / "c.jpg")
        (d / "notes.txt").write_text("not a photo")

        photos = scan(d)
        groups = group(photos, 6)

        assert len(photos) == 5
        assert len(groups) == 1
        names = [p[0].name for p in groups[0]]
        assert sorted(names) == ["a.png", "a_copy.webp", "a_small.jpg"]
        assert names[-1] == "a_small.jpg"  # lowest resolution is never the one kept


if __name__ == "__main__":
    test_finds_resized_and_resaved_copies()
    print("ok")
