# Koodiklinikan MM2024 Pistepörssiskaba

A website to show who's winning in [Koodiklinikka's](https://koodiklinikka.fi) Points Leader competition for IIHF World Championships.

It's running live at [https://kk-mm2024.netlify.app/](https://kk-mm2024.netlify.app/).

## How to operate

### Prerequisites

Create three files to `_data/`:

`games.json` with contents of `[]`, `participants.json` with contents of `[]` and `scores.json` with contents of `[]`.

### Add a new game

Head over to `_scripts` to run a Python script. To do that, you'll need to create a virtualenv and install a few packages:

#### Requirements

```
cd _scripts/
python -m venv venv
source venv/bin/activate
pip install bs4 selenium
```

#### Find a game from IIHF site

To add a game, find its Play-by-play gamecenter site (like [this one](https://www.iihf.com/en/events/2024/wm/gamecenter/playbyplay/54187/1-sui-vs-nor)) from IIHF's site.

#### Parse it to a JSON flat file database

Run

```
python parse.py https://www.iihf.com/en/events/2024/wm/gamecenter/playbyplay/54187/1-sui-vs-nor
```

This will open a Firefox window (that autocloses once it's read), parses scoring data and stores it in `games.json`.

### Add participants

For each participant, add a JSON object to `participants.json` with this template:

```json
{
    "name": "[username]",
    "finns": {
        "name": "[player name in ascii]",
        "points": [estimate in integer]
    },
    "all": {
        "name": "[player name in ascii]",
        "points": [estimate in integer]
    }
}
```

### Build the final data

After either changing the `participants.json` or `games.json` (via running `parse.py`), one more script is needed to run to generate final data. This must be run in the root of the project, not in `_scripts`

```
node _scripts/build.js
```

This will generate `scores.json` which is used in the Eleventy site.

### Tests

To run tests, run

```
pip install pytest
python -m pytest
```

### Dev serve and building the site

#### Prerequisites

```
npm install
```

to install [Eleventy](https://11ty.dev)

#### Run locally

To run a local developer site, run

```
npm run dev
```

which will run Eleventy and serve it in localhost.

#### Build it

To build the site, run

```
npm run build
```

which will generate `_site/index.html` that can be deployed to a webserver as a static site.

## Notes

The architecture of this is version "just put something together" and could probably be simpler and definitely more error-prone.

But for something that lives for a couple of weeks during the competition, it's good enough.
