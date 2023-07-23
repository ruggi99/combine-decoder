from pypykatz.commons.common import UniversalEncoder
from pathlib import Path
import json
import asyncio
import sys

from dump import parse_dump


async def main():
    p = sys.argv[1] if len(sys.argv) > 1 else "temp.bin"
    with open(p, "rb") as f:
        data = f.read()
    print("Done receiving data")

    dump_dict = await parse_dump(data)

    Path("dump.json").write_text(json.dumps(dump_dict, cls=UniversalEncoder, indent=4, sort_keys=True))


asyncio.run(main())