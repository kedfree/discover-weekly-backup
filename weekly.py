# weekly.py
#
# created by: Kedan F.
# updated: February 3, 2023
import spotipy
import time
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect, render_template
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'dsfasSDFIU*@&#(WDKSAdsfasdkn' #example key
TOKEN_INFO = 'token_info'

@app.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return render_template('index.html', a_url = auth_url)

@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('save_discover_weekly', external = True))

@app.route('/saveDiscoverWeekly')
def save_discover_weekly():

    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect('/')
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_id = sp.current_user()['id']
    user_name = sp.current_user()['display_name']
    discover_weekly_playlist_id = None
    saved_weekly_playlist_id = None
    
    current_playlists = sp.current_user_playlists()['items']
    for playlist in current_playlists:
        if(playlist['name'] == "Discover Weekly"):
            discover_weekly_playlist_id = playlist['id']
        if(playlist['name'] == "Saved Discover Weekly"):
            saved_weekly_playlist_id = playlist['id']
    
    if not discover_weekly_playlist_id:
        return "Discover Weekly not found, make sure you have the Discover Weekly playlist saved in your library"
    
    if not saved_weekly_playlist_id:
        new_playlist = sp.user_playlist_create(user_id, 'Saved Discover Weekly', True)
        saved_weekly_playlist_id = new_playlist['id']

    discover_weekly_playlist = sp.playlist_items(discover_weekly_playlist_id)
    saved_weekly_playlist = sp.playlist_items(saved_weekly_playlist_id)
    song_uris = []
    for song in discover_weekly_playlist['items']:
        song_uri = song['track']['uri']
        song_uris.append(song_uri)
    
    for song in saved_weekly_playlist['items']:
        song_uri = song['track']['uri']
        if song_uri in song_uris:
            song_uris.remove(song_uri)

    if song_uris != []:
        sp.user_playlist_add_tracks(user_id, saved_weekly_playlist_id, song_uris, None)

    return render_template('success.html', name = user_name)

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect(url_for('login', external = True))

    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        spotify_oath = create_spotify_oauth
        token_info = spotify_oath.refresh_access_token(token_info['refresh_token'])

    return token_info


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        redirect_uri = url_for('redirect_page', _external = True),
        scope = 'user-library-read playlist-modify-public playlist-modify-private playlist-read-collaborative playlist-read-private'
    )

app.run(debug=True)