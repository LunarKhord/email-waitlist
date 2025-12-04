from aio_pika import connect_robust, RobustConnection, Channel
from contextlib import asynccontextmanager
from typing import Optional
import logging
from fastapi import FastAPI
import asyncio
from aio_pika import Channel


"""
This module serves the purpose of connecting to RabbitMQ
"""

# Set up a logger
logger = logging.getLogger(__name__)

RABBIT_MQ_CONNECTION: Optional[RobustConnection] = None
RABBIT_MQ_CHANNEL: Optional[Channel] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
	"""
	FastAPI Lifespan function, its purpose is to create a connection to the rabbitmq server before the fastapi server bootsup completely
	or accepts incoming traffic
	"""
	try:
		# Create a connection
		RABBIT_MQ_CONNECTION = await connect_robust("amqp://guest:guest@localhost/", client_properties={"connection_name": "email-waitlist"})
		# Create a channel
		RABBIT_MQ_CHANNEL = await RABBIT_MQ_CONNECTION.channel()
		logger.info(f"[INFO]: {RABBIT_MQ_CONNECTION} {RABBIT_MQ_CHANNEL}")
		# Declare an Exchange
		await RABBIT_MQ_CHANNEL.declare_exchange(name="waitlist.direct", type="direct", durable=True)
		# Declare a Queue
		waitlist_queue = await RABBIT_MQ_CHANNEL.declare_queue(name="email", durable=True)
		await waitlist_queue.bind("waitlist.direct", routing_key="email-key")

		# Consumer incoming message
	except Exception as e:
		raise e
	yield