import asyncio
import aiofiles
from datetime import datetime


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5000)
    while True:
        now = datetime.now().strftime("%d.%m.%y %H:%M")
        data = await reader.read(200)
        formatted_data = f'[{now}] {data.decode()}'
        async with aiofiles.open('output.txt', 'a') as file:
            await file.write(formatted_data)
        print(formatted_data.strip())

asyncio.run(tcp_echo_client())
