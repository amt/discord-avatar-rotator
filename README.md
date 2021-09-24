# Discord Avatar Rotator

## Usage

```
usage: rotator.py [-h] (-f FILE | -d DIR) [-c] [-q]

Update Discord profile picture via command line

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File to use as profile picture
  -d DIR, --dir DIR     Folder to choose profile picture from, chosen at random from media files in the directory.
  -c, --creds           Indicates the creds from creds.py should be used. If not supplied then environment variables will be used. See creds.py for more information.
  -q, --quiet           Enable quiet mode only logging warnings+.
```

---

## Example

Running manually:
```
./rotator.py -c --file image.jpg
```

or via cron
```bash
*/10 * * * * (cd /mnt/d/discord && ./rotator.py -c --dir profiles)
```