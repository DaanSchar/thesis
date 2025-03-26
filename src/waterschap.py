from enum import Enum


class Waterschap(Enum):
	NOORDERZIJLVEST = {
		'name': 'Waterschap Noorderzijlvest',
		'code': 'WNZ',
		'arcgisURL': 'https://arcgis.noorderzijlvest.nl/server/rest/services',
	}
	DRENTS_OVERIJSSELSE_DELTA = {
		'name': 'Waterschap Drents Overijsselse Delta',
		'code': 'WDO',
		'arcgisURL': 'https://services6.arcgis.com/BZiPrSbS4NknjGsQ/arcgis/rest/services',
	}
	VECHTSTROMEN = {
		'name': 'Waterschap Vechtstromen',
		'code': 'WVS',
		'arcgisURL': 'https://services1.arcgis.com/3RkP6F5u2r7jKHC9/ArcGIS/rest/services',
	}
	VALLIJ_EN_VELUWE = {
		'name': 'Waterschap Vallei en Veluwe',
		'code': 'WVV',
		'arcgisURL': 'https://services1.arcgis.com/ug8NBKcLHVNmdmdt/ArcGIS/rest/services',
	}
	RIJN_EN_IJSSEL = {
		'name': 'Waterschap Rijn en IJssel',
		'code': 'WRI',
		'arcgisURL': 'https://opengeo.wrij.nl/arcgis/rest/services',
	}
	DE_STRICHTSE_RIJNLANDEN = {
		'name': 'Waterschap De Strichtse Rijnlanden',
		'code': 'WSR',
		'arcgisURL': 'https://services1.arcgis.com/1lWKHMyUIR3eKHKD/ArcGIS/rest/services',
	}
	LIMBURG = {
		'name': 'Waterschap Limburg',
		'code': 'WL',
		'arcgisURL': 'https://maps.waterschaplimburg.nl/arcgis/rest/services',
	}
	ZUIDERZEELAND = {
		'name': 'Waterschap Zuiderzeeland',
		'code': 'WZZ',
		'arcgisURL': 'https://services.arcgis.com/84oM5NriBghHdQ3Z/ArcGIS/rest/services',
	}
