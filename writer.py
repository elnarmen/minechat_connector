import asyncio


async def tcp_echo_client(message, account_hash='da751b26-5b73-11ee-aae7-0242ac110002'):
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5050)

    greeting = await reader.readline()
    print(f'Received: {greeting.decode().strip()}')

    writer.write(f"{account_hash}\n".encode())
    await writer.drain()

    response = await reader.readline()
    print(f'Received: {response.decode().strip()}')
    response = await reader.readline()
    print(f'Received: {response.decode().strip()}')

    writer.write(f"{message}\n\n".encode())
    await writer.drain()

    writer.close()
    await writer.wait_closed()


asyncio.run(tcp_echo_client('Test message'))
