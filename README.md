# spotify_personal

Access and modify personal Spotify account, using Spotify's API

2021 Jason Portenoy

- [spotify_personal](#spotify_personal)
	- [Environament variables](#environament-variables)
	- [Getting started](#getting-started)
		- [Using Docker](#using-docker)
		- [Connecting to the Spotify API](#connecting-to-the-spotify-api)

## Environament variables

The following variables need to be set in a `.env` file:

```sh
SPOTIPY_CLIENT_ID=...
SPOTIPY_CLIENT_SECRET=...
SPOTIPY_REDIRECT_URI=...
```

(Can use `SPOTIPY_REDIRECT_URI='https://www.spotify.com'`)

## Getting started

### Using Docker

Jupyter notebooks can be finicky when using WSL. Running with Docker can help with this. Make sure Docker and Docker-compose are installed, then run:


```
docker-compose up --build
```

Open [http://localhost:8870](http://localhost:8870) to start using Jupyter notebook.

### Connecting to the Spotify API

Use the `SpotifyPersonal` class to interact with the Spotify API. To set up an instance of this:

```python
from dotenv import load_dotenv, find_dotenv
# Make sure the environment variables are available in a `.env.` file
load_dotenv(find_dotenv())

import spotipy
from spotipy.oauth2 import SpotifyOAuth

scopes = ["user-library-read"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scopes))

from spotify_personal import SpotifyPersonal
spp = SpotifyPersonal(sp)
```