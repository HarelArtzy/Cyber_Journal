# Client/server protocol

Install the dependencies with `pip install -r requirements.txt`, start `server.py`, and then start `client.py`. Both use port 8081 by default; set `CYBER_PORT` to the same port for both programs to change it. The requirements include PyAutoGUI and Pillow for the SCREENSHOT command. On Linux, PyAutoGUI also documents installing the system packages `scrot` and Tkinter (often `python3-tk`); these cannot be installed through pip. SCREENSHOT currently saves to a hard-coded Windows path that must be changed for your machine.

When a client connects, the server generates an RSA key pair and sends its public key to the client. The client generates a fresh Fernet key, encrypts it using the public key with RSA-OAEP (SHA-256), and sends it to the server. The server uses its private key to decrypt it. Both sides then use that Fernet key for the connection.

Each command and response is encrypted and authenticated with Fernet (AES-128-CBC and HMAC-SHA256). Messages are sent as a four-byte network-order length followed by the Fernet token. The encrypted content contains a four-byte command length, the UTF-8 command, and the binary data. Encrypted frames are limited to 64 MiB; Fernet encoding and encryption add overhead, so the maximum plaintext size is smaller.

**Security limitation:** The server's public key is sent without authentication. An attacker who can intercept the connection could substitute their own key and read or modify traffic. Use TLS with certificate verification for a real deployment, particularly because the server accepts commands that can execute programs and delete files. This protocol does not authenticate clients either.

The client and server log the RSA public key and Fernet session key to `Server-Client.log`; the server also logs its RSA private key. Anyone with access to these logs can decrypt recorded traffic, so use this only for testing and protect or delete the logs afterward.

The log also records sent and received messages before and after encryption, including the complete command, data, and Fernet token. Binary data is shown as a Python bytes representation. This can make the log large and expose message contents.
