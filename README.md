<img src="https://github.com/shayonkeating/relationalknowledgegpt/blob/main/text_files/graph_image.png" width="500" height="500">

# relationalknowledgegpt
Relational NLP Knowledge Graphs with videos and/or audio

## 🚀 What are knowledge graphs
Knowledge graphs are a graphical representation of knowledge (duh)! But an easier way to describe it is to say that we want to know xyz, how can we get there through different iterations? An even EASIER way to describe it would be imagine a spider web and each node represents an idea and each strand represents a bridge between those ideas connecting them. Getting the picture? This project aimed at taking video files or audio files, extracting the audio into a text file (utilizing OpenAIs whisper model) and then using gpt-3.5-turbo to analyze the text for words that connect to other words. This could be pushed out further into the diagnostic space, imagine a doctor charting, and what they say can be used to make the most likely diagnosis through a “spider web” of knowledge.

## 🛠️ Technologies

- `NLP`
- `GPTs`
- `Jupyter Notebooks`
- `Python`

## 🚦 Running the Project

```shell
git clone
```
the repository and create three new folders in the repository

```shell
mkdir ./video_files
mkdir ./audio_files
mkdir ./auth
```

Drop your openAI API key into the auth folder as a .txt file and run 

```shell
python knowledge_graph_scripts/video_audio_transcribe.py
python knowledge_graph_scripts/knowledge_graph_gen.py
```

## 💡 Improvements
- Definitely could take this into a database

## 🐞 Issues
- None (so far)
