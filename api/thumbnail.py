"""
file created by cool-dev-guy
----------------------------
Script to get the thumbnail.
"""
from http.server import BaseHTTPRequestHandler
import cv2
import random
import m3u8

class handler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        # Handle HEAD requests
        self.send_response(200)
        self.send_header('Content-type', 'image/jpeg')
        self.send_header('Content-Length', '0')  # Set content length to 0 for HEAD requests
        self.end_headers()
    def do_GET(self):
        try:
            playlist = m3u8.load("https://www101.anifastcdn.info/videos/hls/BX05AI0RBZdW08yjjfb6nw/1708711219/150231/7244984011002ee29dc294666636b688/ep.1.1703884989.m3u8")
            playlist = m3u8.load(playlist.playlists[0].absolute_uri)
            random_number = random.randint(0, len(playlist.segments) - 1)  # Adjusted to prevent IndexError
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
