# DJ-enerative - automated control of Rekordbox with GPT 4 Vision and Computer Vision

DJ-enerative is a project that uses GPT 4 Vision and Computer Vision to automate the control of Rekordbox. This project is designed to help DJs create unique and dynamic sets by using AI to generate new and interesting transitions between songs.

[![DJ-enerative Logo](https://img.youtube.com/vi/KclN_sV4JBo/0.jpg)](https://youtu.be/KclN_sV4JBo?si=joaAN2Em7rzjkP6X)

## How it works

DJ-enerative uses GPT 4 Vision to analyze the audio and video of a song and generate a unique transition based on the content of the song. This transition is then sent to Rekordbox, which automatically applies the transition to the next song in the playlist. This might look like cutting the bass, where the transitions are etc.

## Technology used

This is built to run on the premier DJ software Rekordbox using GPT 4 Vision and computer vision supported by PyTesseract and PyAutoGUI. With these tools we've handed over the reign to the bot to play the songs and transition between them.

PyAutoGUI and PyTesseract is useful for us to map the application out so we can have the mouse and keyboard shortcuts navigate the bot around. PyTesseract is especially useful with the OCR capabilities, allowing the bot to 'see' without calling GPT-4V which might introduce latency in trigger actions that DJs usually take (for eg, pressing play on transitions, changing the EQ etc).

Where GPT-4V is useful, however, is in picking what songs get played. After a song is transitioned out, the bot takes a screenshot to share the state of the application with the GPT-4 model. The model then picks the next song to play based on songs that are currently playing and a myriad of factors such as the key and tempo of the song, the genre they belong to, the artist who might have written that track - much like how a human DJ does! This information is passed back to the bot which is able to search through the music catalogue available and load up the desired track, ready to play.

## Why this? Why us?

Artists and DJs are always looking for new ways to create unique and engaging performances, and these experiences shouldn't be only left to the practioners. With DJ-enerative, anyone with this tool would be able to create endless unique DJ sets which can span across genres and artists.

Why us? Well we're both long time musicians, and I'm a DJ!
