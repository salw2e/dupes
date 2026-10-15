# dupes

Find duplicate photos in a folder, even resized, re-saved or converted copies. Keeps the highest resolution one.

```
pip install -r requirements.txt
python dupes.py ~/Pictures           # list duplicates
python dupes.py ~/Pictures --clean   # move extra copies to ~/Pictures/.dupes-trash
```

`-t` sets how different two photos can be and still count (default 6, 0 = identical). Works with jpg, png, webp, heic and more.
