# sakurazaka-member-img-dl
Download Sakurazaka46 members' artist images

`scrape.py`: Downloads current members' photos.

`scrape_allmembers.py`: Downloads all members' photo (including graduated members).

## How to use
1. Download or clone repo
2. In shell, change current directory to `sakurazaka-member-img-dl`
3. Run `python file-of-choice.py`
4. Images are downloaded in `/img`. Filenames are kanji names of each member.
5. For `scrape_allmembers.py`, image's suffix numbers are arbitrary.

## Requirements
- Should work with any version of python3 and on any os, as is without additional installs.
- Uses {re, os} standard libraries and invokes curl for https requests
