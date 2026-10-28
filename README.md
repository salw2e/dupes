# dupes

Finds duplicate photos in a folder, including resized and recompressed copies.

```
pip install -r requirements.txt
python dupes.py ~/Pictures
python dupes.py ~/Pictures --clean
```

`--clean` keeps the largest copy and moves the rest to `.dupes-trash`. `-t` sets how close two photos need to be (default 6).
