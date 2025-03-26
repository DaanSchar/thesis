import asyncio
import json
from typing import TypedDict

import aiohttp


class Service(TypedDict):
	name: str
	type: str


class ArcGIS:
	def __init__(self, url: str) -> None:
		self.url = url

	async def get_services(self) -> list[dict]:
		folders = await self.__get_folders()

		if not folders:
			services = await self.__get_available_services(None)
		else:
			services = await asyncio.gather(*(self.__get_available_services(folder) for folder in folders))
			services = [service for folder in services for service in folder]

		services = await asyncio.gather(*(self.__get_service(service) for service in services))
		return [service for service in services if service is not None]

	async def __get_service(self, service: Service) -> dict | None:
		url = f'{self.url}/{service["name"]}/{service["type"]}?f=json'

		async with aiohttp.ClientSession() as session, session.get(url) as response:
			try:
				response.raise_for_status()
			except aiohttp.ClientResponseError as e:
				if e.status == 401:
					return None
				raise e

			try:
				result = await response.json()

				return {**service, 'service': result}
			except aiohttp.ClientResponseError:
				result = await response.text()
				result = json.loads(result)

				return {**service, 'service': result}

	async def __get_folders(self) -> list[str] | None:
		url = f'{self.url}?f=json'

		async with aiohttp.ClientSession() as session, session.get(url) as response:
			try:
				response.raise_for_status()
			except aiohttp.ClientResponseError as e:
				if e.status == 401:
					return None
				raise e

			result = await response.json()

			if 'folders' not in result:
				return None

			return result['folders']

	async def __get_available_services(self, folder: str | None) -> list[Service]:
		url = f'{self.url}/{folder}?f=json' if folder else f'{self.url}?f=json'

		async with aiohttp.ClientSession() as session, session.get(url) as response:
			response.raise_for_status()

			result = await response.json()

			unauthorized = 'error' in result and result['error'].get('code') == 499

			if unauthorized:
				return []

			return result['services']
