#!/usr/bin/env python
"""
Utilizing OpenAIs whisper model, this script can do text to speech of a video or audio \
file. Simply drop a video into the video folder or drop audio into the audio folder \
and it will generate a text file from what it says. NLP at its finest. Model will \
take a while to chug through the data so be patient especially if it is a long video. \

Author: Shayon Keating
Date: February 23, 2024
"""


# installing required libraries if needed, may need to be done manually 
# !pip install pydub
# !pip install git+https://github.com/openai/whisper.git
# !sudo apt update && sudo apt install ffmpeg


# import reqs
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import os
from pydub import AudioSegment
import re
import subprocess


# connect the video files
video_files = './video_files'
audio_files = './audio_files'
text_files = './text_files'


folders = [video_files, audio_files, text_files]
for folder in folders:
    # Check if the output folder exists
    if not os.path.exists(folder):
    # If not, create the folder
        os.makedirs(folder)


# extract the audio from the video and export the audio as a wav file
for video_file in os.listdir(video_files):
    if video_file.endswith('.mp4'):
        video_path = os.path.join(video_files, video_file)
        audio = AudioSegment.from_file(video_path, format="mp4")
        audio.export(os.path.join(audio_files, f"{video_file[:-4]}.wav"), format="wav")


# function to transcribe and save the output in txt file
def transcribe_and_save(audio_files, text_files, model='medium.en'):
    """
    Function will use whisper AI model from Open AI to transcribe the video NLP
    
    Args: audio files
    
    Ouptut: .txt file in ./text_file folder
    """
    # Construct the Whisper command
    whisper_command = f"whisper '{audio_files}' --model {model}"
    
    try:
        # Run the Whisper command
        transcription = subprocess.check_output(whisper_command, shell=True, text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(f"Error during transcription: {e.output}")
        return
    
    # Clean and join the sentences
    output_without_time = re.sub(r'\[\d+:\d+\.\d+ --> \d+:\d+\.\d+\]  ', '', transcription)
    sentences = [line.strip() for line in output_without_time.split('\n') if line.strip()]
    joined_text = ' '.join(sentences)

    # Create the corresponding text file name
    audio_file_name = os.path.basename(audio_files)
    text_file_name = os.path.splitext(audio_file_name)[0] + '.txt'
    file_path = os.path.join(text_files, text_file_name)

    # Save the output as a txt file
    with open(file_path, 'w') as file:
        file.write(joined_text)

    print(f'Text for {audio_file_name} has been saved to: {file_path}')


# Transcribing all the audio files in the directory
for audio_file in os.listdir(audio_files):
    if audio_file.endswith('.wav'):
        audio_files = os.path.join(audio_files, audio_file)
        transcribe_and_save(audio_files, text_files)
# This will take a while to trduge through, be patient, its a lot of data