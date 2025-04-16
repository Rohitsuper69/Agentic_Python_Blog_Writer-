# Agentic_Python_Blog_Writer
<<<<<<< HEAD
=======

## Introduction

Sincere Greetings, it was a great experience working on this project. I always wanted to create something like this now this opportunity to push beyond my limits and work on it. So, lets start.

## Set up

1. First clone this app from github by writing the following line on git bash

   ```
      git clone https://github.com/Rohitsuper69/Agentic_Python_Blog_Writer-
   ```
2. Start with creating a virtual enviornment using python venv if not installed then
   ```
      pip install venv
   ```
   then create a virtual enviornment to avoid any dependency conflict
   ```
      python -m venv venv
   ```
   now activate the enviornment
   ```
      venv/Scripts/activate
   ```
3. Now install requirements file
   ```
      pip install -r requirements.txt
   ```
4. Now create a .env file in main directory to provide with keys of Newsapi and geminiapi in following format
   NEWSDATA_API_KEY={NEWSDATA_API_KEY}
   GEMINI_API_KEY={GEMINI_API_KEY}
5. Now execute the following command on the terminal
   ```
      streamlit run streamlit.py
   ```
   
## Usage
In the streamlit app on the web input can be given for multiple input seperate them with commas. It will give the output below it along with CLI summary and download options for the .md and .json file
Following are some example images
![1](examples/ss1.png)
