cd /home/dino/server
gunicorn3 -D server:app
nohup python3 bot.py &