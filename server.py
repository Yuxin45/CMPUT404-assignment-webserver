#  coding: utf-8 
import socketserver, os
from os import path
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
		reponse = ""
		if len(split_request) >= 2:
			request_method = split_request[0].decode('utf-8')
			print("request method:", request_method)
			new_url =  split_request[1].decode('utf-8')[1:]
			file_url = ("/www/" + (split_request[1].decode('utf-8')))[1:]

			print("requested file url:", file_url)

			if file_url.endswith('/'):
				file_url += "index.html"
				file_content = self.obtain_file_content(file_url)

			else:
				file_content = self.obtain_file_content(file_url)

			reponse = self.pack_http_response(request_method, file_url, file_content)
		self.request.sendall(bytearray(reponse,'utf-8'))


	def pack_http_response(self, method, file_url, content):

		if method == "GET":
			if len(file_url.split("../")) >= 2:
				content = self.obtain_file_content("www/404.html")
				response = "HTTP/1.1 404 Not Found\r\n\r\n" + content
				print(response)

			elif path.isdir(file_url):
				print("into 301")
				# content = self.obtain_file_content("www/301.html")
				content, directory = self.obtain_moved_file(file_url)
				response = "HTTP/1.1 301 Moved Permanently\r\n" +"Location: " + directory + ";\r\n\r\n" + content
				print(response)
				# return response

			elif content == None:
				content = self.obtain_file_content("www/404.html")
				response = "HTTP/1.1 404 Not Found\r\n\r\n" + content
				print(response)
				# return response
				
			# elif path.isdir(file_url):
			# 	print("into 301")
			# 	# content = self.obtain_file_content("www/301.html")
			# 	content = self.obtain_moved_file(file_url)
			# 	response = "HTTP/1.1 301 Moved Permanently\r\n\r\n" + content
			# 	print(response)
			# 	# return response

			elif file_url.endswith(".css"):
				response = "HTTP/1.1 200 OK \r\nContent-Type: text/css;\r\n\r\n" + content
				print(response)
				# return response

			else:
				response = "HTTP/1.1 200 OK\r\nContent-Type: text/html;\r\n\r\n" + content
				print(response)
				# return response

		else:
			response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
		print(response)
		return response


	def obtain_file_content(self, path):
		# print("directory:",os.path.abspath(__file__))
		try:
			f = open(path, "r")
			file_content = f.read()
			print("file data:", file_content)
			return file_content

		except BaseException as e:
			#print(str(e))
			return None


	def obtain_moved_file(self, file_url):
		print("file_url: ", file_url)
		directory = file_url.split('/')[-1] + '/'
		print("directory:", directory)
		data = """<!DOCTYPE html>
			<html>
			<head>
				<title>Page Moved Permanently</title>
			        <meta http-equiv="Content-Type"
			        content="text/html;charset=utf-8"/>
			        <!-- check conformance at http://validator.w3.org/check -->
			        <!-- <link rel="stylesheet" type="text/css" href="base.css"> -->
			</head>

			<body>
				<div class="eg">
					<h1>301 Moved Permanently</h1>
					<ul>
						<li>moved to here
			                        <li><a href=""" + directory + """>go to correct page</a></li>
					</ul>
				</div>
			</body>
			</html> 
			"""

		return data, directory


if __name__ == "__main__":
	HOST, PORT = "localhost", 8080

	socketserver.TCPServer.allow_reuse_address = True
	# Create the server, binding to localhost on port 8080
	server = socketserver.TCPServer((HOST, PORT), MyWebServer)

	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()
