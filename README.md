# autoSubtitle
A self-build project that could help user add subtitles into video and download srt and mp4 from the server

## Features
- Speech recognition
- Auto-generate subtitles
- Edit subtitles online(simple UI)
- Add subtitles into video

## Techniques
- **Docker** to setup develop environment
- Lightweight **Flask** to build server
- **SQLAlchemy** to interact with MySQL database
- **JWT** set in cookies to help server verify users' identity

## How to use?
1. Make sure you have docker running on your back
2. Under root folder, type 
`docker compose up` in CLI
3. Visit `http://127.0.0.1:5555` and you could register, login and add subtitles to your own video.

## System Design
1. Folder Sturcture

<img width="354" alt="截圖 2023-02-02 上午9 50 37" src="https://user-images.githubusercontent.com/43340166/216808174-0fd5b75b-668c-4687-86c0-886c66320c0c.png">
