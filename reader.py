import asyncio


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5000)
    while True:
        data = await reader.read(200)
        print(data.decode().strip())


asyncio.run(tcp_echo_client())
