# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 15:36:42 2016

@author: marco
"""
'''
[x]Status messages displayed to the console. These messages simply let the user know what the program is currently computing (e.g. "Reading in playlist information from playlist1.txt...", etc.).
[x]Track information and statistics written to an output file. Name your output file <input file base name>_stats.txt. For example, for the provided input file, "top10alltime.txt", the corresponding output file is "top10alltime_stats.txt". The stats to be written to the output file include:
[x]Track name, artist, duration (in minutes and seconds), and popularity for each song. See the starter code below for how to get this information.
[x]The number of tracks in the playlist.
[x]The average duration (in minutes and seconds) of the tracks in the playlist.
[x]The name of the longest track in the playlist and its duration (in minutes and seconds).
[x]The average popularity of the tracks in the playlist.
[x]The name of the most popular track in the playlist and its popularity.
'''
'''
Programmer: Marco Arceo
Class: CptS 111-01, Fall 2016
Programming Assignment #5
11/02/16

Description: "Spotify API Playlist"
'''

import urllib.request
import webbrowser

def format_search_term(search_term):
    '''
    111 students: no need to call this function
    To prepare the search term string for the query:
    1. remove comma
    2. replace spaces with +
    '''
    search_term = search_term.replace(",", "")
    search_term = search_term.replace(" ", "+")
    return search_term
  
def build_query(query):
    '''
    111 students: no need to call this function
    Builds the query string for the Spotify Search API according to this website:
    https://developer.spotify.com/web-api/console/get-search-item/
    '''
    query_base = "https://api.spotify.com/v1/search?q="    
    query = query_base + query
    # perform a track search and only return the top result
    query += "&type=track&limit=1"
    return query
    
def extract_numeric_value(results_str, label):
    '''
    111 students: no need to call this function
    Extracts an integer value represented by the label parameter from the JSON response.
    '''
    index = results_str.find(label)
    results_str = results_str[index:]
    index = results_str.find(":")
    results_str = results_str[index + 2:]
    index = results_str.find(",")
    results_str = results_str[:index]
    value = int(results_str)
    return value
    
def extract_preview_url(results_str):
    '''
    111 students: no need to call this function
    Extracts the preview url from the JSON response.
    '''
    index = results_str.find("preview_url")
    results_str = results_str[index:]
    index = results_str.find(":")
    results_str = results_str[index:]
    index = results_str.find("\"")
    results_str = results_str[index + 1:]
    index = results_str.find("\"")
    results_str = results_str[:index]
    return results_str
    
def get_track_information(track, artist, info_type):
    '''
    111 STUDENTS: THIS IS THE FUNCTION YOU WILL CALL
    Accepts 3 strings representing a track and its artist, and the name of the information to retrieve (info_type).
    info_type can be:
        "duration_ms": returns an integer representing the duration of the song in MILLISECONDS        
        "popularity": returns an integer representing the popularity of the song
        "preview_url": returns a string representing a url hosting a short clip of the song
    Returns the requested information for track and artist
    '''
    track = format_search_term(track)
    artist = format_search_term(artist)
    
    # search the spotify database for a track by artist
    search_terms = track + "+" + artist
    
    query = build_query(search_terms)

    web_obj = urllib.request.urlopen(query)
    # web_obj.read() returns an array of bytes, need to convert to a string
    results_str = str(web_obj.read())
    web_obj.close()
    
    info = ""
    if info_type == "popularity" or info_type == "duration_ms":
        info = extract_numeric_value(results_str, info_type)
    elif info_type == "preview_url":
        info = extract_preview_url(results_str)
    else:
        print("Unknown information type")
    return info
    
    
def status_message():
    '''
    Display message telling the user that information is being gathered
    '''
    print("Gathering playlist information...")
    print("")
    

def query_message(track, artist):
    '''
    Tells the user that information about a song and artist is being gathered
    '''
    print("Querying Spotify for information regarding %s by %s ..." %(track, artist))
    
def gather_message():
    '''
    Displays message telling the user that more information is being gathered
    '''
    print("")
    print("Gathering additional information...")
    
def open_preview(song_name, artist_name):
    '''
    Tells the user that a preview of the most popular song is going to open
    '''
    print("A preview of %s by %s is about to play in a seperate browser..." %(song_name, artist_name))
def main():
    '''
    '''
    
    #infile = open(filename.txt, "r")
    infile = open("rapmusic.txt", "r") #Copy the above template
    #outfile= open(filename + "_stats", "w")
    outfile = open("rapmusic_stats.txt", "w") #Copy the above template
    
    #Display query message
    status_message()
    
    songs = 0
    duration = 0
    all_pop = 0
    longest = -1
    most_pop = -1
   
   #Read the file and add the information
    while True:
        track = infile.readline().strip() #Gathers Track names
        songs += 1
        artist = infile.readline().strip() #Gathers Artist Names
        blank = infile.readline() #Skips blank lines
        query_message(track, artist) #Displays query message
        outfile.write("Track %s \n" %(track)) #Writes Track name to outfile
        outfile.write("Artist %s \n" %(artist)) #Writes Track name to outfile
        pop = get_track_information(track, artist, "popularity") #Gathers popularity based on the track and artist
        if most_pop == -1 or pop > most_pop: #Calculates the most popular song, the name of the sogn and its artist
            most_pop = pop
            song_name = track
            artist_name = artist
        all_pop += pop #Adds all of the popularities together
        dur = get_track_information(track, artist, "duration_ms") #Gathers the duration of each song in ms
        if longest == -1 or dur > longest: #Calculates the longest song
            longest = dur
            long_song_name = track
            long_artist_name = artist
        sec = (dur / 1000) % 60 
        minu = ((dur / (1000*60)) % 60)
        duration += dur #Adds all of the durations together
        url = get_track_information(track, artist, "preview_url")
        outfile.write("Popularity %s \n" %(pop)) #Writes popularity per song to outfile
        outfile.write("Duration %d:%d \n" %(minu, sec)) #Writes duration per song to outfile
        outfile.write("Preview the song: %s \n\n" %(url))
        if blank == "": #Stops the list once it reaches a blank
            break
        
    #Display message saying more information is being gathered
    gather_message()
    
    #Display the total amount of songs
    outfile.write("Total songs in the playlist: %d \n" %(songs))
    
    #Calculate the average duration of the songs and display it
    avg_duration = duration / songs
    seconds = (avg_duration / 1000) % 60 
    minutes = ((avg_duration / (1000*60)) % 60)
    outfile.write("Average song duration in the playlist: %d:%d \n" %(minutes, seconds))
    
    #Calculate the longest song in the playlist
    long_sec = (longest / 1000) % 60 
    long_minutes = ((longest / (1000*60)) % 60)
    outfile.write("The longest song name and duration in the playlist: %s by %s and %d:%d \n" %(long_song_name, long_artist_name, long_minutes, long_sec))
    
    #Calculate the most popular song in the playlist
    avg_popularity = all_pop / songs
    outfile.write("Average popularity of the tracks in the playlist: %d \n" %(avg_popularity))
    
    #Calculate the most popular track in the playlist
    outfile.write("Most popular song and its popularity: %s by %s and %d \n" %(song_name, artist_name, most_pop))
    
    #Opens browser for the preview
    open_preview(song_name, artist_name)
    url_most_pop = get_track_information(song_name, artist_name, "preview_url")
    webbrowser.open(url_most_pop)
    
    #Close the files
    infile.close()
    outfile.close()
    
main()