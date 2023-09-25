import asyncio
import json
import logging
import os
import aiofiles

from dotenv import load_dotenv


FORMAT = '%(levelname)s:%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logging.getLogger('asyncio').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def register(username='anonymous'):
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5050)

    response = await reader.readline()
    logger.debug(f'Ответ: {response.decode().strip()}')  # Hello %username%! Enter your personal hash or leave it empty to create new account.

    writer.write('\n'.encode())
    logger.debug('Отправлено пустое сообщение для перехода в регистрацию')
    await writer.drain()

    response = await reader.readline()
    logger.debug(f'Ответ: {response.decode().strip()}')

    writer.write(f'{username}\n'.encode())
    logger.debug(f'Отправлен никнейм {username} для регистрации')
    await writer.drain()

    registration_result = json.loads(await reader.readline())
    async with aiofiles.open('.env', 'a') as file:
        await file.write(f'USER_TOKEN={registration_result["account_hash"]}')
    logger.debug(f'Ответ: {registration_result}')
    logger.debug('Токен сохранен в файле ".env"')

    writer.close()
    await writer.wait_closed()


async def tcp_client(message, token):
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5050)

    greeting = await reader.readline()
    logger.debug(greeting.decode().strip())  # Hello %username%! Enter your personal hash or leave it empty to create new account.

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

    writer.write(f'{message}\n\n'.encode())
    logger.debug(f'Сообщение: {message}')
    await writer.drain()

    writer.close()
    await writer.wait_closed()


def main():
    load_dotenv()
    token = os.getenv('USER_TOKEN')
    if token:
        asyncio.run(tcp_echo_client(message='Test message', token=token))
    else:
        asyncio.run(register())


if __name__ == '__main__':
    main()
