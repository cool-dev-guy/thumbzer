"""
file created by cool-dev-guy
----------------------------
Script to get the thumbnail.
"""
from http.server import BaseHTTPRequestHandler
import cv2
import random
import m3u8,requests
import urllib.parse as urlparse
class handler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        # Handle HEAD requests
        self.send_response(200)
        self.send_header('Content-type', 'image/jpeg')
        self.send_header('Content-Length', '0')
        self.end_headers()
    def do_GET(self):
        try:
            _query = urlparse.urlparse(self.path)
            _params = urlparse.parse_qs(_query.query)
            xid = _params.get('id',None)

            api = requests.get(f'https://api.anime-dex.workers.dev/episode/{xid[0]}')
            # LOG FOR TROUBLESHOOTING
            print(f'https://api.anime-dex.workers.dev/episode/{xid[0]}')
            playlist = m3u8.load(api.json()["results"]["stream"]["sources"][0]["file"])
            playlist = m3u8.load(playlist.playlists[1].absolute_uri)
            random_number = random.randint(0, len(playlist.segments) - 1)
            input_file = playlist.segments[random_number].absolute_uri

            ts = cv2.VideoCapture(input_file)
            ret, frame = ts.read()
            ts.release()
            if ret:
                _, img_encoded = cv2.imencode('.jpg', frame)
                image_data = img_encoded.tobytes()
            else:
                raise ValueError("Failed to read frame from video")
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.send_header('Content-Disposition', 'attachment; filename=thumbnail.jpg')
            self.end_headers()
            self.wfile.write(image_data)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Error: {}".format(str(e)).encode('utf-8'))
        return
