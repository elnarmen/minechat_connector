import argparse
import asyncio
import json
import logging
import os
import aiofiles
import contextlib

from dotenv import load_dotenv


FORMAT = '%(levelname)s:%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logging.getLogger('asyncio').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def manage_tcp_connection(host, port):
    reader, writer = await asyncio.open_connection(host, port)
    try:
        yield reader, writer
    finally:
        writer.close()
        await writer.wait_closed()


async def register(username, host, port, message):
    async with manage_tcp_connection(host, port) as (reader, writer):
        response = await reader.readline()
        logger.debug(f'Ответ: {response.decode().strip()}')

        writer.write('\n'.encode())
        logger.debug('Отправлено пустое сообщение для перехода в регистрацию')
        await writer.drain()

        response = await reader.readline()
        logger.debug(f'Ответ: {response.decode().strip()}')

        username = username.replace('\n', '').strip()
        writer.write(f'{username}\n'.encode())
        logger.debug(f'Отправлен никнейм {username} для регистрации')
        await writer.drain()

        registration_result = json.loads(await reader.readline())
        token = registration_result['account_hash']
        async with aiofiles.open('.env', 'a') as file:
            await file.write(f'USER_TOKEN={token}')
        logger.debug(f'Ответ: {registration_result}')
        logger.debug('Токен сохранен в файле ".env"')

        writer.close()
        await writer.wait_closed()

        await tcp_client(message, token, host, port)


async def submit_message(writer, message):
    message = message.replace('\n', '').strip()
    writer.write(f'{message}\n\n'.encode())
    logger.debug(f'Сообщение: {message}')
    await writer.drain()


async def tcp_client(message, token, host, port):
    async with manage_tcp_connection(host, port) as (reader, writer):
        greeting = await reader.readline()
        logger.debug(greeting.decode().strip())

        writer.write(f'{token}\n'.encode())
        logger.debug(f'Отправлен токен: {token}')
        await writer.drain()

        auth_result = json.loads(await reader.readline())
        if not auth_result:
            logger.debug(f'Ответ: Неизвестный токен. Проверьте его или зарегистрируйте заново.')
            return

        logger.debug(f'Ответ: {auth_result}')
        response = await reader.readline()
        logger.debug(f'Ответ: {response.decode().strip()}')

        await submit_message(writer, message)


def main():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument('message', help='Сообщение')
    parser.add_argument('--token', '-t', help='Токен, полученный при авторизации')
    parser.add_argument('--host', type=str, default='minechat.dvmn.org')
    parser.add_argument('--port', type=int, default=5050)
    parser.add_argument('--username', default='anonymous')

    args = parser.parse_args()

    token = args.token if args.token else os.getenv('USER_TOKEN')
    message, host, port, username = args.message, args.host, args.port, args.username

    if token:
        asyncio.run(tcp_client(message, token, host, port))
    else:
        asyncio.run(register(username, host, port, message))


if __name__ == '__main__':
    main()
