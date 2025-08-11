import asyncio
import logging

import aio_pika


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    connection = await aio_pika.connect_robust("amqp://uudex:uudex@127.0.0.1/", )

    queue_name = "test_queue"

    async with connection:
        # Creating channel
        channel = await connection.channel()

        # Will take no more than 10 messages in advance
        await channel.set_qos(prefetch_count=10)

        # Declaring queue
        queue = await channel.declare_queue(queue_name, auto_delete=True, durable=True)
        print(dir(queue))
        print(dir(queue.declaration_result))
        print(queue.declaration_result.consumer_count)
        async with queue.iterator() as queue_iter:
            print(f"Count Messages: {queue.declaration_result.message_count}")
            print(queue.declaration_result.consumer_count)
            async for message in queue_iter:
                print(queue.declaration_result.consumer_count)
                print(f"Count Messages: {queue.declaration_result.message_count}")
                async with message.process():
                    print(message.body)

                    # if queue.name in message.body.decode():
                    #     break


if __name__ == "__main__":
    asyncio.run(main())
