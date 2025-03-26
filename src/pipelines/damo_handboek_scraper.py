import aiohttp
from bs4 import BeautifulSoup
from motor.motor_asyncio import AsyncIOMotorClient

from src.pipeline.pipeline import AsyncDataPipeline
from src.pipeline.result import PipelineResult


class DamoHandboekScraperPipeline(AsyncDataPipeline):
	def __init__(self, client: AsyncIOMotorClient) -> None:
		self.base_url = 'https://damo.hetwaterschapshuis.nl/DAMO%202.5/Objectenhandboek%20DAMO%202.5/html'
		self.client = client
		super().__init__()

	async def run(self) -> PipelineResult:
		objects = await self.__get_all_object_names()

		collection = self.client['DAMODB']['handboek']
		await collection.drop()

		for object_name in objects:
			obj = await self.process_object(object_name)
			await collection.insert_one(obj)

		return {'success': True}

	async def process_object(self, object_name: str) -> dict:
		attributes = await self.get_object_attributes(object_name)
		definition = await self.get_object_definition(object_name)
		return {'object': object_name, 'attributen': attributes, 'definitie': definition}

	async def __get_all_object_names(self) -> list[str]:
		objects = []
		url = f'{self.base_url}/DAMO%20Objectenhandboek.html'

		async with aiohttp.ClientSession() as session, session.get(url) as response:
			response.raise_for_status()
			html = await response.text()

			soup = BeautifulSoup(html, 'html.parser')

			objecten_li = soup.find('li', id='Objecten')

			if objecten_li is None:
				raise Exception('No <li> with id "Objecten"')

			objecten_ul = objecten_li.find('ul')

			if objecten_ul is None:
				raise Exception('No child <ul> of <li> with id "Objecten"')

			for li in objecten_ul.find_all('li'):
				text = li.get_text()
				objects.append(text)

		return objects

	async def get_object_attributes(self, object_name: str) -> list[dict]:
		if object_name == 'Onderhoudsplicht':
			object_name = 'Onderhoudsplicht1'

		url = f'{self.base_url}/{object_name}.html'
		print(url)
		attributes = []

		async with aiohttp.ClientSession() as session, session.get(url) as response:
			response.raise_for_status()
			html = await response.text()

			soup = BeautifulSoup(html, 'html.parser')

			div_with_table = soup.find('div', class_='rvps7')

			if div_with_table is None:
				print(f'{object_name} has no attributes')
				return []

			table = div_with_table.find('table')

			if table is None:
				raise Exception(f'No <table> in <div> with class "rvps7" for object {object_name}')

			table_header_row = table.find('tr')
			header_cells = table_header_row.find_all('td')
			header_values = [self.__get_data_cell_text(td).get('value') for td in header_cells]
			print(header_values)

			for tr in table.find_all('tr')[1:]:
				tds = tr.find_all('td')
				values = [self.__get_data_cell_text(td) for td in tds]

				obj = {}

				for i, header_value in enumerate(header_values):
					if header_value == 'Type':
						obj[header_value] = values[i]
					else:
						obj[header_value] = values[i].get('value')

				attributes.append(obj)

				# attributes.append(
				# {
				# 'attribuutnaam': values[0].get('value'),
				# 'toelichting': values[1].get('value'),
				# 'type': values[2],
				# 'eenheid': values[3].get('value'),
				# 'bron_definitie': values[4].get('value'),
				# 'model': values[5].get('value'),
				# }
				# )

		return attributes

	async def get_object_definition(self, object_name: str) -> str | None:
		if object_name == 'Onderhoudsplicht':
			object_name = 'Onderhoudsplicht1'

		url = f'{self.base_url}/{object_name}.html'
		print('url', url)

		async with aiohttp.ClientSession() as session, session.get(url) as response:
			response.raise_for_status()
			html = await response.text()

			soup = BeautifulSoup(html, 'html.parser')
			paragraph = soup.find('p', class_='rvps11')

			if paragraph is None:
				print(f'No definition found for {object_name}')
				return None

			span = paragraph.find('span')

			if span is None:
				raise Exception(f'No <span> in <p> with class "rvps11" for object {object_name}')

			return span.get_text()

	def __get_data_cell_text(self, element) -> dict[str, str | None]:
		# The text is nested inside a span OR anchor which is nested inside a paragraph
		paragraph = element.find('p')

		if paragraph is None:
			return {'type': None, 'value': None}

		span = paragraph.find('span')
		anchor = paragraph.find('a')

		if span is not None:
			return {'type': 'span', 'value': span.get_text()}
		if anchor is not None:
			return {'type': 'anchor', 'value': anchor.get_text()}

		return {'type': None, 'value': None}
