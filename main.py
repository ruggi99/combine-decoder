import asyncio
from pypykatz import pypykatz
from pypykatz.commons.common import UniversalEncoder
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import json

from dump import parse_dump


async def main():
    # Create a socket
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(("0.0.0.0", 6666))
    sock.listen(1)
    print("Waiting connection")

    # Accept the first connection
    conn, addr = sock.accept()
    print("Started receiving data")
    data = bytes()
    while True:
        partial_data = conn.recv(1024 * 1024)
        if partial_data is None or partial_data == b'':
            break
        data += partial_data
    print("Done receiving data")

    dump_dict = await parse_dump(data)

    print(json.dumps(dump_dict, cls=UniversalEncoder, indent=4, sort_keys=True))

asyncio.run(main())