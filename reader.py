import asyncio
import aiofiles
from datetime import datetime


async def tcp_echo_client():
    while True:
        try:
            reader, writer = await asyncio.open_connection(
                'minechat.dvmn.org', 5000)
            try:
                while True:
                    current_datetime = datetime.now()
                    current_datetime_str = current_datetime.strftime("%d.%m.%y %H:%M")
                    data = await reader.read(200)
                    if not data:
                        raise ConnectionError("Connection lost")
                    formatted_data = \
                        f'[{current_datetime_str}] {data.decode("utf-8", "ignore")}'
                    async with aiofiles.open('output.txt', 'a') as file:
                        await file.write(formatted_data)
                    print(formatted_data.strip())
            finally:
                writer.close()
                await writer.wait_closed()
        except ConnectionError:
            print(f'[{datetime.now().strftime("%d.%m.%y %H:%M")}] Connection lost. Reconnecting in 5 seconds...')
            await asyncio.sleep(5)


asyncio.run(tcp_echo_client())
