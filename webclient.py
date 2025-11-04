import socket
import sys

def query(url, port, fileName):
    file_ext = fileName.split(".")[1]
    print(file_ext)
    if file_ext == "txt":
        t = "text/plain"
    elif file_ext == "html":
        t = "text/html"
    else:
        t = "unknown"
    contentLength = len(fileName) #temporary until we implement file parsing
    preEncodedRequestHeader = f"GET /{fileName} HTTP/1.1\r\nHost: {url}\r\nContent-Type: {t}\r\nContent-Length: {contentLength}\r\nConnection: close\r\n\r\n"
    requestHeader = preEncodedRequestHeader.encode("ISO-8859-1")
    response_parts = []
    try:
        s = socket.socket()
        s.connect((url, port))
        s.sendall(requestHeader)
        while True:    
            data = s.recv(4096)
            if not data:
                break
            response_parts.append(data)
        response = b"".join(response_parts)
        print(response.decode("ISO-8859-1"))
                
    except ConnectionRefusedError:
        print("Error Connection Refused")
    except socket.error as error:
        print(f"Socket error: {error}")

if __name__ == "__main__":
    url = sys.argv[1]
    port = int(sys.argv[2])
    fileName = sys.argv[3]
    query(url, port, fileName)


