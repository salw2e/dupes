# dupes

Finds duplicate photos in a folder. It compares perceptual hashes, so resized or recompressed copies are matched too.

```
pip install -r requirements.txt
python dupes.py ~/Pictures
python dupes.py ~/Pictures --clean
```

`--clean` moves every copy except the highest resolution one into `.dupes-trash` inside the folder. Nothing gets deleted.

`-t` changes how close two photos have to be (default 6, 0 means identical).
