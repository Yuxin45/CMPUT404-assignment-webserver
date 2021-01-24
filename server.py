#  coding: utf-8 
import socketserver, os
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#	 http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(socketserver.BaseRequestHandler):
	
	def handle(self):
		self.data = self.request.recv(1024).strip()
		print ("Got a request of: %s\n" % self.data)
		
		split_request = self.data.split()
		request_method = split_request[0].decode('utf-8')
		print("request method:", request_method)
		file_url = split_request[1].decode('utf-8')[1:]
		print("requested file url:", file_url)

		file_content = self.obtain_file_content(file_url)
		reponse = self.pack_http_response(request_method, file_url, file_content)
		self.request.sendall(bytearray(reponse,'utf-8'))

	def pack_http_response(self, method, file_url, content):

		if method == "GET":
			if content == None:
				response = "HTTP/1.1 404 Not Found\r\n\r\n"

			elif file_url.endswith(".css"):
				response = "HTTP/1.1 200 OK \r\nContent-Type: text/css;\r\n\r\n" + content

			elif file_url.endswith('/'):

			else:
				response = "HTTP/1.1 200 OK\r\nContent-Type: text/html;\r\n\r\n" + content

		else:
			response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"

		return response




	def obtain_file_content(self, path):
		# print("directory:",os.path.abspath(__file__))
		try:
			f = open(path, "r")
			file_content = f.read()
			print("file data:", file_content)
			return file_content

		except BaseException as e:
			print(str(e))
			return None



if __name__ == "__main__":
	HOST, PORT = "localhost", 8080

	socketserver.TCPServer.allow_reuse_address = True
	# Create the server, binding to localhost on port 8080
	server = socketserver.TCPServer((HOST, PORT), MyWebServer)

	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()
