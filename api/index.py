"""
file created by cool-dev-guy
----------------------------
Script to get the thumbnail and save it.
"""
from http.server import BaseHTTPRequestHandler
import json,requests,secrets,string,re
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse
def session(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # GET NECESSARY KEYS
        _session_upload = int(datetime.now().timestamp() * 1000)
        _session = requests.get('https://postimages.org/web')
        _session_time = datetime.now()
        _session_time = _session_time.strftime("%d/%m/%Y,%H:%M:%S")
        _ui = [24, 1600, 900, "true", "", "",_session_time]

        _upload_session = session(32)
        _soup = BeautifulSoup(_session.text,'html.parser')

        # EXTRACT KEY
        data = _soup.find_all('script')[-1].get_text()
        pattern = r'\b\w{40}\b'
        match = re.search(pattern,data)
        _token = match.group()

        # UPLOAD HEADERS
        headers = {
            "Origin":"https://postimages.org/web",
            "Referer":'https://postimages.org/web',
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest"
        }

        _data = {
            'token':_token,
            'upload_session':_upload_session,
            'url':'https://thumbzer.vercel.app/api/thumbnail',
            'numfiles':1,
            'gallery':'',
            'ui':_ui,
            'optsize':0,
            'expire':0,
            'session_upload':_session_upload
        }
        # PARSE DICT TO PARAM FORM
        _data = urllib.parse.urlencode(_data)
        _data = urllib.parse.unquote(_data)

        # UPLOAD THE IMAGE
        _upload = requests.post('https://postimages.org/json/rr',headers=headers,data=_data)
        data = _upload.json()

        # Set the appropriate content type header
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Encode JSON data and write it to the response body
        json_data = json.dumps(data)
        self.wfile.write(json_data.encode('utf-8'))
        return
