from pprint import pprint

import aiohttp
from bs4 import BeautifulSoup
from motor.motor_asyncio import AsyncIOMotorClient

from src.pipeline.pipeline import AsyncDataPipeline
from src.pipeline.result import PipelineResult


class DamoDomeintabellenScraper(AsyncDataPipeline):
	def __init__(self, client: AsyncIOMotorClient) -> None:
		super().__init__()
		self.client = client
		self.base_url = 'https://damo.hetwaterschapshuis.nl/DAMO%202.5/Objectenhandboek%20DAMO%202.5/html'

	async def run(self) -> PipelineResult:
		names = await self.get_stuff()
		pprint(names)
		return {'success': True}

	async def get_stuff(self):
		url = f'{self.base_url}/AtotenmetM.html'

		async with aiohttp.ClientSession() as session, session.get(url) as response:
			response.raise_for_status()
			html = await response.text()

			soup = BeautifulSoup(html, 'html.parser')

			h3 = soup.find_all('h3')

			names = [x.get_text() for x in h3]
			names = [x.replace('&nbsp;', '').replace('\xa0', '') for x in names]
			names = [x for x in names if x != '']

			tables = soup.find_all('table')
			print("total tables", len(tables))
			print("total names", len(names))

			return names

	# async def get_domeintabel_names(self):
	# url = f'{self.base_url}/Domeinen.html'

	# names = []

	# async with aiohttp.ClientSession() as session, session.get(url) as response:
	# response.raise_for_status()
	# html = await response.text()

	# soup = BeautifulSoup(html, 'html.parser')

	# table = soup.find('table')

	# if table is None:
	# raise Exception('No table found')

	# rows = table.find_all('tr')

	# for row in rows:
	# cells = row.find_all('td')

	# if cells is None:
	# raise Exception('No cells found')

	# for cell in cells[1:]:
	# paragraphs = cell.find_all('p')

	# if paragraphs is None:
	# continue

	# for paragraph in paragraphs:
	# anchor = paragraph.find('a')
	# span = paragraph.find('span')

	# if anchor is not None:
	# if anchor.get_text() == '':
	# continue
	# names.append(anchor.get_text())
	# elif span is not None:
	# if span.get_text() == '':
	# continue
	# names.append(span.get_text())
	# else:
	# print('ohoooh')

	# return names
