# generateTrackInfo
This is a tool used for https://jaydenzkoci.github.io/ to generate track info easier.

# Website
You can load a website off of this repository for easier setup

# How it works
Go to data/jam_tracks.json and use My Oh My by Ava Max as an example.
## Every track needs
- Title
- Artist
- Spotify ID - Example for https://open.spotify.com/track/377uEWjxVKksQDlwDqaIfx. It would be 377uEWjxVKksQDlwDqaIfx.
## After you get those things down. Run run.bat.
It will grab the info from the jam_tracks.json file and it will detect if they need updating
## The Canvas Download.
It will ask you to go to a link and copy the video address of the video on the webpage. This is to prevent any bot detection
## Track Info
It will ask for you to click another site and you need to type the values on the page. Specfically the BPM, Release Year, and Duration of the song.

That's basically the gist. This is to make my life easier. This is most likely not for someone else's use purposes lol.
## Dependencies
- os
- requests
- spotipy
- spotipy.oauth2
- dotenv
- json
- re
