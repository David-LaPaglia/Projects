import requests 
import pandas as pd
import lyricsgenius as lg 
import musicbrainzngs
from dotenv import load_dotenv
import os

#Application name	music_recs_discord_bot LASTfm.api

# will need last.fm api_key to run code yourself

load_dotenv('3510.env')
TOKEN = os.getenv('DISCORD_TOKEN')
geniusClient = os.getenv("GENIUS_CLIENT_ID")
geniusSecret = os.getenv("GENIUS_CLIENT_SECRET")
geniusClientAccess = os.getenv("GENIUS_CLIENT_ACCESS_TOKEN")
API_key	=os.getenv('API_key') #last.fm
shared_secret=os.getenv('shared_secret')# last.fm


def getArtistReccomendations(artist):
    rootURL = 'http://ws.audioscrobbler.com/2.0/'
    artistURL = '?method=artist.getsimilar&artist='+artist+'&api_key='+API_key+'&format=json'
    artist_data = []
    rec = requests.get(rootURL + artistURL).json()
    similar_artists = rec['similarartists']['artist'][0:9]
    
    artist_data = {
        'Name': [artist['name'] for artist in similar_artists], #For index in similar artists add as the key 
        #value pair to name of the artist
        'URL': [artist['url'] for artist in similar_artists],
        'Match': [float(artist['match']) for artist in similar_artists]
    }
    df = pd.DataFrame(artist_data)
    return df

# I wanna go to different Countries! Lets get inspired by different countries!
# geo.getTopArtists
def getTopArtistsByCountry(country):
    rootURL = 'http://ws.audioscrobbler.com/2.0/'
    artistURL = '?method=geo.gettopartists&country='+country+'&api_key='+API_key+'&format=json'
    artist_data = []
    rec = requests.get(rootURL + artistURL).json()
    artist_data = rec['topartists']['artist']
    data = {
        'Artist': [artist['name'] for artist in artist_data],
        'Listeners': [int(artist['listeners']) for artist in artist_data]
    }
    df = pd.DataFrame(data)
    
    return df

## Attempt to use some LyricsGenius ||| No song is returning lyrics, I hate lyrics genius


genius = lg.Genius(geniusClientAccess,sleep_time=0.2,retries=4) #the key to this project
def getSongLyrics(songName,artistName):
    songLyrics = genius.search_song(songName,artistName)
    return(songLyrics.lyrics)

# Third data source doesn't work : https://docs.ksoft.si/api

# Forth Data Source: musicbrainz

# Find artist ID with MusicBrainz
def findArtist(itemQueryString):
    musicbrainzngs.set_useragent(
        "INFO3510 music app", 
        "0.1", 
        "https://canvas.colorado.edu/courses/109882/assignments/2106008"
    )
    result = musicbrainzngs.search_artists(artist=itemQueryString)
    formatted_results = []
    for artist in result['artist-list']:
        artist_info = f"{artist['id']}: {artist['name']} (Match Score: {artist['ext:score']})"
        formatted_results.append(artist_info)

    return "\n".join(formatted_results[:10]) 


# Use MusicBrainz id to find albums # this doesn't really work.
def getArtistInfo(artistID, limit=5):
    musicbrainzngs.set_useragent(
        "INFO3510 music app", 
        "0.1", 
        "https://canvas.colorado.edu/courses/109882/assignments/2106008"
    )
    artist_id = artistID
    result = musicbrainzngs.get_artist_by_id(artist_id)
    for release_group in result["artist"]:
        print(release_group)
        return result


# Discord Message Slicer
# Simplfied from class, 
def discordMessageSlicer(message, pageSize):
    messagePieces = []
    for i in range(0, len(message), pageSize):
        currentPiece = message[i:i + pageSize] #slices the message from index to pageSize
        messagePieces.append(currentPiece)
    print(f"Message Length: {len(message)}")
    print(f"Page Size: {pageSize}")
    #print(f"Message: {message}") # This is good to see since I am an informatics freak and want to make sure this is always working
    print(f"messagePieces amount: {len(messagePieces)}")
    return messagePieces


def main():
    result = getArtistReccomendations("Taylor Swift")
    print(result)


if __name__ == "__main__":
    main()

