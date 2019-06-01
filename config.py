import spotipy
import spotipy.oauth2

credentials = {}
credentials['SPOTIPY_CLIENT_ID'] = 'f933af6ad6034724b9d561f11ba45ffe'
credentials['SPOTIPY_CLIENT_SECRET'] = '92914fdbf7bc437ebb80e786e87d16c6'
credentials['SPOTIPY_REDIRECT_URI'] = ''

search_config = {}
search_config['LIMIT'] = 50 
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id = credentials['SPOTIPY_CLIENT_ID'],
																	 client_secret=credentials['SPOTIPY_CLIENT_SECRET'])

spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
results = spotify.search(q='', type='playlist', limit = 100)