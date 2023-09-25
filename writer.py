import asyncio
import logging


FORMAT = '%(levelname)s:%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logging.getLogger('asyncio').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def tcp_echo_client(message, account_hash='da751b26-5b73-11ee-aae7-0242ac110002'):
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5050)

    greeting = await reader.readline()
    logger.debug(f'Response: {greeting.decode().strip()}')

    writer.write(f'{account_hash}\n'.encode())
    logger.debug(f'Message: {account_hash.strip()}')
    await writer.drain()

    response = await reader.readline()
    logger.debug(f'Response: {response.decode().strip()}')

    response = await reader.readline()
    logger.debug(f'Response: {response.decode().strip()}')

    writer.write(f'{message}\n'.encode())
    logger.debug(f'Message: {message}')
    await writer.drain()

    writer.close()
    await writer.wait_closed()


def main():
    asyncio.run(tcp_echo_client('Test message'))


if __name__ == '__main__':
    main()
