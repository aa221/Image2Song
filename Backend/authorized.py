from credentials import spotty_creds as sc
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials(client_id = sc.SPOTIPY_CLIENT_ID,client_secret = sc.SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager,retries=10,requests_timeout=10)
