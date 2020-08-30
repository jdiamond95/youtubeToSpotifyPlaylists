import requests
import json
import os
from secrets import youtubeAPIKey, spotifyUserId, spotifyToken
 
s = requests.Session()
spotifyHeaders = {"Authorization": "Bearer " + spotifyToken}
 
#Get Youtube Playlist
def getYoutubePlaylist():
    #Return the name of the playlist and all the songs in the playlist
    channelName = input("Enter the channel name: ")
    r = s.get("https://www.googleapis.com/youtube/v3/search?q={}&type=channel&key={}".format(channelName, youtubeAPIKey))
    channelId = r.json()['items'][0]['id']['channelId']
    r = s.get("https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId={}&key={}".format(channelId, youtubeAPIKey))
    playlistName = input("Enter the playlist name: ")
    playlistId = False
    for playlist in r.json()['items']:
        if playlist['snippet']['title'] == playlistName:
            playlistId = playlist['id']
    r = s.get("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={}&key={}".format(playlistId, youtubeAPIKey))
    videoNames = []
    #Doesnt handle pagination - max is 5 videos
    for video in r.json()['items']:
        videoNames.append(video['snippet']['title'])
    return playlistName, videoNames
 
 
#Create the spotify playlist
def createSpotifyPlaylist(playlistName):
    r = s.post("https://api.spotify.com/v1/users/{}/playlists".format(spotifyUserId), json={"name":playlistName, "description":"Imported Youtube Playlist", "public": "false"}, headers=spotifyHeaders)
    #r = s.post(spotifyCreatePlaylistURL + spotifyUserId + "/playlists", json={"name":playlistName, "description":"Imported Youtube Playlist", "public": "false"}, headers=spotifyHeaders)
    return r.json()['id']
 
 
#Find the individual songs in Spotify
def getSpotifySong(songName, artist):
    r = s.get("https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=1".format(songName, artist), headers=spotifyHeaders)
    # Return the Spotify URI of the song
    return r.json()['tracks']['items'][0]['uri']


#Add the found song to the Spotify playlist
def addToSpotifyPlaylist(playlistId, songURI):
    r = s.post("https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(playlistId, songURI), headers=spotifyHeaders)
 
 
def main():
    #playlistName, videoNames = getYoutubePlaylist()
    #print(playlistName)
    #print(videoNames)
    #playlistId = createSpotifyPlaylist("Fun playlist")
    #songURI = getSpotifySong("bad guy", "billie eilish") 
    #addToSpotifyPlaylist(playlistId, songURI)
    createSpotifyPlaylist("potato")

if __name__=="__main__":
    main()
