# Multithreaded File Transfer using TCP Socket in Python

A multithreaded file transfer client-server program build using a python programming language. The server has the capability to handle multiple clients concurrently at the same by using threading. The server assigns each client a thread to handle working for that client. 

To run server : python server.py
To run client : python client.py 4456

The server supports the following functions:
 - upload path: Upload a file to the server
 - get path: Download a file from the server
