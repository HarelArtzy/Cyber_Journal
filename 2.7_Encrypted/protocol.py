"""Encrypted client/server protocol using RSA-OAEP and Fernet."""

import logging
import struct

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.fernet import Fernet

MAX_FRAME_SIZE = 64 * 1024 * 1024


def recv_all(sock, length):
    """Read exactly length bytes, or raise if the connection closes."""
    data = bytearray()
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Socket closed unexpectedly")
        data.extend(chunk)
    return bytes(data)


def _send_frame(sock, data):
    if len(data) > MAX_FRAME_SIZE:
        raise ValueError("Message exceeds the maximum frame size")
    sock.sendall(struct.pack("!I", len(data)) + data)


def _recv_frame(sock):
    length = struct.unpack("!I", recv_all(sock, 4))[0]
    if length > MAX_FRAME_SIZE:
        raise ValueError("Message exceeds the maximum frame size")
    return recv_all(sock, length)


def _oaep():
    return padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(), label=None)


def server_handshake(sock):
    """Send an RSA public key and decrypt the client's Fernet session key."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
    private_pem = private_key.private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption())
    logging.info("Server RSA private key:\n%s", private_pem.decode())
    logging.info("Server RSA public key:\n%s", public_key.decode())
    _send_frame(sock, public_key)
    key = private_key.decrypt(_recv_frame(sock), _oaep())
    logging.info("Server Fernet session key: %s", key.decode())
    return Fernet(key)


def client_handshake(sock):
    """Encrypt a new Fernet session key with the server's RSA public key."""
    public_key = serialization.load_pem_public_key(_recv_frame(sock))
    if not isinstance(public_key, rsa.RSAPublicKey) or public_key.key_size < 2048:
        raise ValueError("Invalid server RSA public key")
    logging.info("Client received server RSA public key:\n%s",
                 public_key.public_bytes(serialization.Encoding.PEM,
                                         serialization.PublicFormat.SubjectPublicKeyInfo).decode())
    key = Fernet.generate_key()
    logging.info("Client Fernet session key: %s", key.decode())
    _send_frame(sock, public_key.encrypt(key, _oaep()))
    return Fernet(key)


def protocol_send(sock, cipher, cmd: str, data: bytes):
    """Encrypt and send a command and its binary data."""
    cmd_bytes = cmd.encode("utf-8")
    plaintext = struct.pack("!I", len(cmd_bytes)) + cmd_bytes + data
    logging.info("Sending decrypted message: command=%r data=%r", cmd, data)
    token = cipher.encrypt(plaintext)
    logging.info("Sending encrypted message: %s", token.decode("ascii"))
    _send_frame(sock, token)


def protocol_recv(sock, cipher):
    """Receive and authenticate a command and its binary data."""
    packet = _recv_frame(sock)
    logging.info("Received encrypted message: %r", packet)
    plaintext = cipher.decrypt(packet)
    if len(plaintext) < 4:
        raise ValueError("Invalid message")
    cmd_len = struct.unpack("!I", plaintext[:4])[0]
    if cmd_len > len(plaintext) - 4:
        raise ValueError("Invalid command length")
    cmd = plaintext[4:4 + cmd_len].decode("utf-8")
    data = plaintext[4 + cmd_len:]
    logging.info("Received decrypted message: command=%r data=%r", cmd, data)
    return cmd, data
