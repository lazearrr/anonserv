import socket
import sys
import os

def readFile(completePath):
    try:
        with open(completePath, "rb") as content:
            payload = content.read()
            content_length = len(payload)
        return payload, content_length
    except FileNotFoundError as f:
        preEncodedPayload = f"Error 404: Page Not Found \n{f}"
        payload = preEncodedPayload.encode("UTF-8")
        content_length = len(payload)
        return payload, content_length
    except Exception as e:
        print(f"Unknown Error: {e}")


def decodeData(data):
    try:
        if not data:
            print("No Data Received")
        decodedData = data.decode("ISO-8859-1")
        splitDecodedData = decodedData.split()
        fullPath = splitDecodedData[1]
        strippedPath = fullPath.strip("/")
        fileExtension = strippedPath.split(".")[-1]
        return decodedData, fileExtension, strippedPath, splitDecodedData
    except IndexError:
        print("list index out of range")

def buildHTML(files, fullPath):
    fullPath = f"{fullPath}/"
    print(fullPath)
    homePage = []
    homePage.append("<html><body><h1>anonserv</h1>")
    for file in files:
        middle = f"<a href=\"{fullPath}{file}\">{file}</a><br>"
        homePage.append(middle)
    end = "</body></html>"
    homePage.append(end)
    html = "".join(homePage)
    return html

def buildSocket(port):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    s.listen()
    return s

def acceptConnection(s, conn_count):
    conn_count += 1
    new_conn, host = s.accept()
    new_socket = new_conn
    data = new_socket.recv(4096)
    return data, host, new_socket, conn_count

def buildLog(conn_count, host, splitDecodedData, decodedData, preEncodedResponse):
            print("INCOMING CONNECTION")
            print("Request Number:", conn_count)
            print("IP Address:", host[0])
            print("Request Type: ", splitDecodedData[0],"\n")
            print("REQUEST")
            print(decodedData)
            print("RESPONSE HEADER:")
            print(preEncodedResponse)
            print("---------------------------------------------------------------------------------------------------------------------")

def buildPayload(fileExtension, fullPath):
    if os.path.isdir(fullPath):
        files = os.listdir(fullPath)
        html = buildHTML(files, fullPath)
        preEncodedPayload = html 
        content_type = "text/html"
        payload = preEncodedPayload.encode("ISO-8859-1")
        content_length = len(payload)
        currentDir = fullPath

    elif fileExtension == "txt":
        content_type = "text/plain"
        payload, content_length = readFile(fullPath)

    elif fileExtension == "html":
        content_type = "text/html"
        payload, content_length = readFile(fullPath)

    elif fileExtension == "ico":
        content_type = "image/vnd.microsoft.icon"
        payload, content_length = readFile(fullPath)

    elif fileExtension == "pdf":
        content_type = "application/pdf"
        payload, content_length = readFile(fullPath)

    elif fileExtension == "webp":
        content_type = "image/webp"
        payload, content_length = readFile(fullPath)

    elif fileExtension == "jpeg":
        content_type = "image/jpeg"
        payload, content_length = readFile(fullPath)

    elif fileExtension == "png":
        content_type = "image/png"
        payload, content_length = readFile(fullPath)

    elif fileExtension == "gif":
        content_type = "image/gif"
        payload, content_length = readFile(fullPath)

    elif fileExtension == "":
        html = buildHTML(files)
        preEncodedPayload = html 
        content_type = "text/html"
        payload = preEncodedPayload.encode("ISO-8859-1")
        content_length = len(payload)

    else:
        content_type = "text/plain"
        payload, content_length = readFile(fullPath)

    return payload, content_length, content_type


def startServer(port, folder):
    splash = r"""
   __ _ _ __   ___  _ __  ___  ___ _ ____   __
  / _` | '_ \ / _ \| '_ \/ __|/ _ \ '__\ \ / /
 | (_| | | | | (_) | | | \__ \  __/ |   \ V /
  \__,_|_| |_|\___/|_| |_|___/\___|_|    \_/  
    """
    print(splash)
    conn_count = 0
    while True:
        m = True
        s = buildSocket(port)

        data, host, new_socket, conn_count = acceptConnection(s, conn_count)
        #decodedData, fileExtension, strippedPath, splitDecodedData = decodeData(data)

        path = f".{folder}"
        
        while m == True:

            try:
                decodedData, fileExtension, strippedPath, splitDecodedData = decodeData(data)

            except TypeError as e:
                print("Cannot unpack because decodedData function probably returned nothing since connection has been sitting idle")
                print(e)
            
            path = f".{folder}"
            fullPath = f"{path}{strippedPath}"
            print(strippedPath)
            print(fullPath)
            payload, content_length, content_type = buildPayload(fileExtension, fullPath)
            preEncodedResponse = f"HTTP/1.1 200 OK\nContent-Type: {content_type}\nContent-Length: {content_length}\nConnection: close\n\n"
            encodedHeaders = preEncodedResponse.encode("ISO-8859-1")
            buildLog(conn_count, host, splitDecodedData, decodedData, preEncodedResponse)

            try:
                new_socket.sendall(encodedHeaders)
                new_socket.sendall(payload)
                new_socket.close()
                s.close()
                m = False

            except BrokenPipeError:
                new_socket.close()
                s.close()
                m = False

# start program
if __name__ == "__main__":
    port = int(sys.argv[1])
    folder = sys.argv[2]
    startServer(port, folder)

