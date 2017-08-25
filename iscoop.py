#!/usr/bin/env python
import cgi
import os
import shutil
import socket
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from argparse import ArgumentParser

import signal

DESCRIPTION = """

Usage: ./iscoop.py [-p port_number 8080] [-o base_upload_folder "output"]

"""


def get_current_dir():
    return os.path.dirname(os.path.realpath(__file__))


def get_output_dir():
    current_dir = get_current_dir()

    basedir = os.path.join(current_dir, "output")
    if os.path.exists(basedir):
        if not os.path.isdir(basedir):
            print('You have a file named "output" which causes conflicts')
            exit(1)
    else:
        os.mkdir(basedir)

    return basedir


def get_args():
    parser = ArgumentParser(description=DESCRIPTION)

    parser.add_argument('-p',
                        '--port',
                        type=int,
                        default=8080)

    parser.add_argument('-o',
                        '--output',
                        type=str,
                        default=get_output_dir())

    args = parser.parse_args()
    return args.port, args.output


class ScoopHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_POST(self):

        if self.path != '/upload/':
            return

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })

        if 'myfile' not in form:
            return

        form_file = form['myfile']

        filename = form_file.filename
        basedir = globals()['output_dir']
        output_path = os.path.join(basedir, filename)

        with open(output_path, 'wb') as outfile:
            shutil.copyfileobj(form_file.file, outfile)

        print('got {}'.format(filename))

        self.respond('')

    @staticmethod
    def strip_query_params(path_with_params):
      position = path_with_params.find('?')
      if position == -1:
        return path_with_params

      return path_with_params[0:position]

    def serve_static(self, path):
        local_dir = get_current_dir()
        local_path = path[1:]

        stripped_path = ScoopHandler.strip_query_params(local_path)

        local_f = os.path.join(local_dir, stripped_path)

        if not os.path.exists(local_f):
            print('doesnt exist: {}'.format(local_f))
        else:
            with open(local_f, 'rb') as infile:
                data = infile.read()
                self.send_head(length=len(data))
                self.wfile.write(data)
        return

    def do_GET(self):
        if self.path.startswith('/static/'):
            self.serve_static(self.path)
            return

        formatted_page = PAGE.format(css=CSS, body=BODY)
        self.respond(formatted_page)

    def send_head(self, status=200, length=0):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-length', length)
        self.end_headers()

    def respond(self, response):
        self.send_head(length=len(response))
        self.wfile.write(response)


def get_local_address():
    # from here: https://stackoverflow.com/a/25850698/2789057

#    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    s.connect(('8.8.8.8', 1))
#    ip = s.getsockname()[0]

    ip = '10.42.0.1'
    return ip


def runserver(host, port):

    # Handle the INTERRUPT exit
    signal.signal(signal.SIGINT, signal_handler)

    server = HTTPServer((host, port), ScoopHandler)

    output = globals()['output_dir']

    local_addr = get_local_address()
    print('iscoop is running at {}:{} with files to {}'.format(local_addr, port, output))
    print('You can stop it with <Ctrl-C>')

    server.serve_forever()


def signal_handler(signal, frame):
    print('\tGood-bye!')
    exit(0)


PAGE = """
<!doctype html>

<html>
<head>
  <meta charset="utf-8">

  <title>iscoop</title>
  <meta name="description" content="get your photos/videos">
  <meta name="author" content="aditya@jawns.us">

  {css}
  <link href="static/skeleton.css" rel="stylesheet">
  <script src="static/jquery.min.js"></script>
  <script src="static/jquery.uploadfile.min.js"></script>

</head>

{body}

</html>

"""

BODY = """
<body>

  <div class="container">
  
    <h3> Get Your Stuff </h3>
    
    <p> Select the files you'd like to have saved to your computer </p>
  
    <div class="row" id="upload">Upload</div>
    <script>
      $(document).ready(function(){
	      $("#upload").uploadFile({
	      url:"upload/",
	      multiple:true,
	      dragDrop:true,
	      fileName:"myfile"});
      });
      

  </script>
</body>
"""


# from http://hayageek.github.io/jQuery-Upload-File/4.0.10/uploadfile.css
CSS = """
  <style>
    .ajax-file-upload-statusbar {
    border: 1px solid #0ba1b5;
    margin-top: 10px;
    width: 420px;
    margin-right: 10px;
    margin: 5px;
    -moz-border-radius: 4px;
    -webkit-border-radius: 4px;
    border-radius: 4px;
    padding: 5px 5px 5px 15px
    }
    
    .ajax-file-upload-filename {
    width: 300px;
    height: auto;
    margin: 0 5px 5px 0px;
    
    }
    
    .ajax-file-upload-filesize {
    width: 50px;
    height: auto;
    margin: 0 5px 5px 0px;
    display: inline-block;
    vertical-align:middle;
    }
    .ajax-file-upload-progress {
    margin: 5px 10px 5px 0px;
    position: relative;
    width: 250px;
    border: 1px solid #ddd;
    padding: 1px;
    border-radius: 3px;
    display: inline-block;
    color:#FFFFFF;
    
    }
    .ajax-file-upload-bar {
    background-color: #0ba1b5;
    width: 0;
    height: 20px;
    border-radius: 3px;
    color:#FFFFFF;
    
    }
    .ajax-file-upload-percent {
    position: absolute;
    display: inline-block;
    top: 3px;
    left: 48%
    }
    .ajax-file-upload-red {
    -moz-box-shadow: inset 0 39px 0 -24px #e67a73;
    -webkit-box-shadow: inset 0 39px 0 -24px #e67a73;
    box-shadow: inset 0 39px 0 -24px #e67a73;
    background-color: #e4685d;
    -moz-border-radius: 4px;
    -webkit-border-radius: 4px;
    border-radius: 4px;
    display: inline-block;
    color: #fff;
    font-family: arial;
    font-size: 13px;
    font-weight: normal;
    padding: 4px 15px;
    text-decoration: none;
    text-shadow: 0 1px 0 #b23e35;
    cursor: pointer;
    vertical-align: top;
    margin: 5px 10px 5px 0px;
    }
    .ajax-file-upload-green {
    background-color: #77b55a;
    -moz-border-radius: 4px;
    -webkit-border-radius: 4px;
    border-radius: 4px;
    margin: 0;
    padding: 0;
    display: inline-block;
    color: #fff;
    font-family: arial;
    font-size: 13px;
    font-weight: normal;
    padding: 4px 15px;
    text-decoration: none;
    cursor: pointer;
    text-shadow: 0 1px 0 #5b8a3c;
    vertical-align: top;
    margin: 5px 10px 5px 0px;
    }
    .ajax-file-upload {
      font-family: Arial, Helvetica, sans-serif;
      font-size: 16px;
       font-weight: bold;
      padding: 15px 20px;
      cursor:pointer;
      line-height:20px;
      height:25px;
      margin:0 10px 10px 0;
      display: inline-block;
      background: #fff;
      border: 1px solid #e8e8e8;
      color: #888;
      text-decoration: none;
      border-radius: 3px;
      -webkit-border-radius: 3px;
      -moz-border-radius: 3px;
      -moz-box-shadow: 0 2px 0 0 #e8e8e8;
      -webkit-box-shadow: 0 2px 0 0 #e8e8e8;
      box-shadow: 0 2px 0 0 #e8e8e8;
      padding: 6px 10px 4px 10px;
      color: #fff;
      background: #2f8ab9;
      border: none;
      -moz-box-shadow: 0 2px 0 0 #13648d;
      -webkit-box-shadow: 0 2px 0 0 #13648d;
      box-shadow: 0 2px 0 0 #13648d;
      vertical-align: middle;
      }
    
    .ajax-file-upload:hover {
          background: #3396c9;
          -moz-box-shadow: 0 2px 0 0 #15719f;
          -webkit-box-shadow: 0 2px 0 0 #15719f;
          box-shadow: 0 2px 0 0 #15719f;
    }
    
    .ajax-upload-dragdrop
    {
    
      border:2px dotted #A5A5C7;
      width:420px;
      color: #DADCE3;
      text-align:left;
      vertical-align:middle;
      padding:10px 10px 0px 10px;
    }
    
    .state-hover
    {
        border:2px solid #A5A5C7;
    }
    .ajax-file-upload-container
    {
      margin:20px 0px 20px 0px;
    }
  </style>
"""

if __name__ == '__main__':
    port, output_dir = get_args()

    runserver('', port)

