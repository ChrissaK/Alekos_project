# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 00:59:23 2018

@author: chrissak
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 21:37:04 2018

@author: chrissak
"""

import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
import os
#from __future__ import unicode_literals
import urllib
#import urllib2
from bs4 import BeautifulSoup
import youtube_dl


def Google_SR(audio,r):
    """
    Calls Google speech recognition to transcribe an a 16bit audio speech file
    
    Parameters
    ----------
    audio: 16bit audio file
    r: object of the form: r = sr.Recognizer()
    
    Returns
    -------
    recognition: string
        The audio file transcription in text
    """
    
    try:
        recognition = r.recognize_google(audio)
        return recognition
    except sr.UnknownValueError:
        return "Google Cloud Speech could not understand audio"
    except sr.RequestError as e:
        return "Could not request results from Google Cloud Speech service"
            
def AudioFileTranscribe(FILENAME,r):
    """
    AudioFileTranscribe: Transcribes audio from a WAV file and 
    returns and prints the transcription to terminal
    
    FILENAME: local or system path to file as a string including file format
    e.g. .wav
    r: an object of the form: r = sr.Recognizer()
    
    """
    with sr.AudioFile(FILENAME) as source:
        audio = r.record(source) 
    transcription = Google_SR(audio,r)
    
    return transcription



def Record(datapath,fs,searchID):
    print "Recording begins..."
    duration = 4  # seconds
    recording = sd.rec(int(duration * fs),blocking = True,dtype = 'int16')
    print "Saving file..."

    filename = "Search%d.wav" %(searchID)
    filenameFULL = os.path.join(datapath,filename)
    sf.write(filenameFULL,recording,fs)
    
    return filenameFULL


def SearchYouTube(ydl_opts,textToSearch):
    print "Searching for song..."
    query = urllib.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    song_list = []
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        print('https://www.youtube.com' + vid['href'])
        song_list.append('https://www.youtube.com' + vid['href'])
    
    #ydl_opts['outtmpl'] = unicode(textToSearch + '.wav')
    #ydl_opts['outtmpl']= u'%(textToSearch)s.%(ext)s']
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print "Downloading song..."
        ydl.download([song_list[0]]) # download the 1st video

if __name__ == "__main__":
        
    # Initialise sound recognition
    r = sr.Recognizer()
    
    # Set default parameters for the recording
    fs = 44100
    sd.default.samplerate = fs # 44.1 kHz
    sd.default.channels = 2
    
    # Set parameters for youtube search
    ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist' : True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    }
    
    datapath = r"C:\Users\chrissak\Documents\Python_Scripts\tracks"
    filenameFULL = Record(datapath,fs,1)
    transcription = AudioFileTranscribe(filenameFULL,r)
    print transcription
    SearchYouTube(ydl_opts,transcription)
    
    
    
    
    #sf.write('new_file.ogg', data, samplerate)
    
    
    
    