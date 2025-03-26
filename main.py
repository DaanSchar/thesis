import asyncio
import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

from src.pipelines import DamoDomeintabellenScraper


async def main() -> None:
	load_dotenv()
	mongo_uri = os.getenv('MONGO_URI')
	client = AsyncIOMotorClient(mongo_uri)

	pipeline = DamoDomeintabellenScraper(client)
	result = await pipeline.run()
	print(result)


if __name__ == '__main__':
	asyncio.run(main())
