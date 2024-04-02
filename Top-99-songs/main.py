#libraries
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from required_data import *


date=input("Which year you want to travel to? Input in the format of YYYY-MM-DD\n")
response=requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
webpage=response.text

soup=BeautifulSoup(webpage,"html.parser")
songs=soup.find_all("h3",class_="c-title")
top100temp=[]
for song in songs:
    top100temp.append(song.getText().strip().replace("\n","").replace("\t",""))
top100=[]
for i in top100temp:
    if i not in ["Songwriter(s):","Producer(s):","Imprint/Promotion Label:"]:
        top100.append(i)
top100=top100[5:-13]
#spotify credentials



sp = SpotifyOAuth(client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                redirect_uri=REDIRECT_URI,
                scope="playlist-modify-public playlist-modify-private")

track_id=[]

spp=spotipy.Spotify(auth_manager=sp)

track_id=[]
for i in top100:
    track_id.append(spp.search(q=i,type="track")['tracks']['items'][0]['id'])
playlist_name = f"Top 99 {date}"  
spp.user_playlist_create(USER_NAME, playlist_name)
playlist_id=None
playlists=spp.current_user_playlists()
for playlist in playlists["items"]:
    if playlist["name"]==playlist_name:
        playlist_id=playlist["id"]
        break

spp.user_playlist_add_tracks("USERNAME", playlist_id, track_id)
