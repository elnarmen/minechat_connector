import asyncio
import json
import logging


FORMAT = '%(levelname)s:%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logging.getLogger('asyncio').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def tcp_echo_client(message, token='da751b26-5b73-11ee-aae7-0242ac110002'):
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5050)

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

    writer.write(f'{message}\n\n'.encode())
    logger.debug(f'Сообщение: {message}')
    await writer.drain()

    writer.close()
    await writer.wait_closed()


def main():
    asyncio.run(tcp_echo_client('Test message'))


if __name__ == '__main__':
    main()
