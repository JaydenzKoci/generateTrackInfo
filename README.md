# generateTrackInfo
This is a tool used for https://jaydenzkoci.github.io/ to generate track info easier.

# How it works
Go to data/jam_tracks.json and use My Oh My by Ava Max as an example.
## Every track needs
- Title
- Artist
- Simplifed Spotify Link - Example
## After you get those things down. Run run.bat.
It will grab the info from the jam_tracks.json file and it will detect if they need updating
## The Canvas Download.
It will ask you to go to a link and copy the video address of the video on the webpage. This is to prevent any bot detection
## Track Info
It will ask for you to click another site and you need to type the values on the page. Specfically the BPM, Release Year, and Duration of the song.

That's basically the gist. This is to make my life easier most likely not someone else lol.
## Dependencies
- os
- requests
- spotipy
- spotipy.oauth2
- dotenv
- json
- re
