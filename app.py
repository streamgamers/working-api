from flask import Flask, render_template, request, url_for, redirect, send_file, session
from pytube import YouTube
from io import BytesIO
import jsonpickle

app = Flask(__name__)
app.config['SECRET_KEY'] = "654c0fb3968af9d5e6a9b3edcbc7051b"

@app.route("/check", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        session['link'] = request.form.get('url')
        try:
            url = YouTube(session['link'])
            url.check_availability()
            n = url.streams
        except:
            return {"Error": "Invalid request"}
        return {"thumbnail": url.thumbnail_url,
                "title": url.title,
                "array" : jsonpickle.encode(n)}
    return {"Error": "Invalid Link"}

@app.route("/download", methods = ["GET", "POST"])
def download_video():
    if request.method == "POST":
        buffer = BytesIO()
        session['link'] = request.form.get('url')
        url = YouTube(session['link'])
        itag = request.form.get("itag")
        video = url.streams.get_by_itag(itag)
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="Video - YT2Video.mp4", mimetype="video/mp4")
    return {"Error": "Invalid request"}

if __name__ == '__main__':
    app.run(debug=True)
