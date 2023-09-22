import asyncio
import os

import aiofiles
import argparse
from datetime import datetime
from dotenv import load_dotenv


async def tcp_echo_client(host, port, path_to_output_file):
    while True:
        try:
            reader, writer = await asyncio.open_connection(
                host, port)
            try:
                while True:
                    current_datetime = datetime.now()
                    current_datetime_str = current_datetime.strftime("%d.%m.%y %H:%M")
                    data = await reader.read(200)
                    if not data:
                        raise ConnectionError("Connection lost")
                    formatted_data = \
                        f'[{current_datetime_str}] {data.decode("utf-8", "ignore")}'
                    async with aiofiles.open(path_to_output_file, 'a') as file:
                        await file.write(formatted_data)
                    print(formatted_data.strip())
            finally:
                writer.close()
                await writer.wait_closed()
        except ConnectionError:
            print(f'[{datetime.now().strftime("%d.%m.%y %H:%M")}] Connection lost. Reconnecting in 5 seconds...')
            await asyncio.sleep(5)


def main():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default=os.getenv('HOST'))
    parser.add_argument('--port', type=int, default=os.getenv('PORT'))
    parser.add_argument(
        '--path',
        type=str,
        default='output.txt',
        help='Path to the file where the chat will be stored.')

    args = parser.parse_args()

    host, port, chat_history_path = args.host, args.port, args.path
    if not all([host, port]):
        raise EnvironmentError(
            'Please ensure that the HOST and PORT environment variables are defined in your .env file '
            'or provide them via command-line arguments using --host and --port.'
        )

    asyncio.run(tcp_echo_client(host, port, chat_history_path))


if __name__ == '__main__':
    main()
