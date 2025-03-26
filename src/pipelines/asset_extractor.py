import json

import aiohttp
from motor.motor_asyncio import AsyncIOMotorClient

from src.pipeline import AsyncDataPipeline
from src.pipeline.result import PipelineResult


class StuwPipeline(AsyncDataPipeline):
	def __init__(self, client: AsyncIOMotorClient) -> None:
		self.client = client
		super().__init__()

	async def run(self) -> PipelineResult:
		try:
			with open('assets.json', 'r') as file:
				data = file.read()
				json_data = json.loads(data)
				sources: list[dict] = json_data['assets']

				for source in sources:
					waterschap = source['waterschap']
					print(f'Processing {waterschap["name"]}({waterschap["code"]})')
					assets = source['assets']
					service_url = source['url']

					for asset in assets:
						print("Processing", asset['asset'])
						asset_name = asset['asset']
						collection = self.client[waterschap['code']][asset_name]
						await collection.drop()

						result = await self.__get_assets(service_url, asset['location'])
						await collection.insert_many(result['features'])

			return {'success': True}
		except Exception:
			return {'success': False}

	async def __get_assets(self, service_url: str, location: str) -> dict:
		url = f'{service_url}/{location}/query?f=geoJson&where=1%3D1&outFields=*'

		async with aiohttp.ClientSession() as session, session.get(url) as response:
			response.raise_for_status()
			return await response.json()
