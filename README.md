# shrinkPics
This is a script for shrinking pictures recursively in a directory, based on [tinypng](https://tinypng.com/).

Before you use this script, go to [tinypng](https://tinypng.com/developers) and get an API key.

Then for the first time, just copy the `main.py` to the directory where you want pics to be shrunked, then run the following command:

```shell
python main.py your-api-key
```
And it will be done!

After you ran the command, the API key would be cached in `key_cache.txt` in the same folder. And next time you don't have to input this key in the command, just

```shell
python main.py
```

is OK.

