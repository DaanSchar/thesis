import asyncio
from datetime import UTC, datetime

from motor.motor_asyncio import AsyncIOMotorClient

from src.arcgis import ArcGIS
from src.pipeline import AsyncDataPipeline, PipelineResult
from src.waterschap import Waterschap


class ExtractServices(AsyncDataPipeline):
	def __init__(self, client: AsyncIOMotorClient) -> None:
		self.client = client

	async def run(self) -> PipelineResult:
		try:
			await self.client.arcGISDB.services.drop()
			tasks = [self.save_services(waterschap) for waterschap in Waterschap]
			await asyncio.gather(*tasks)

			return {'success': True}
		except Exception as e:
			raise e
			return {'success': False}

	async def save_services(self, waterschap: Waterschap) -> None:
		try:
			client = self.client

			arcgis = ArcGIS(waterschap.value['arcgisURL'])
			services = await arcgis.get_services()

			inserted_at = datetime.now(tz=UTC)

			services = [
				{**service, 'source': {'waterschapId': waterschap.value['code']}, 'insertedAt': inserted_at}
				for service in services
			]
			print(f'INSERTING {len(services)} services for waterschap {waterschap.value["name"]}')
			await client.arcGISDB.services.insert_many(services)
		except Exception as e:
			print('error while processing waterschap ', waterschap.value['name'])
			raise e
