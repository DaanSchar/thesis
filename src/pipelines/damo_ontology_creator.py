from motor.motor_asyncio import AsyncIOMotorClient
from rdflib import RDF, XSD, BNode, Graph, Literal, Namespace
from rdflib.namespace import OWL, RDFS

from src.pipeline.pipeline import AsyncDataPipeline
from src.pipeline.result import PipelineResult


class DamoOntologyCreatorPipeline(AsyncDataPipeline):
	def __init__(self, client: AsyncIOMotorClient) -> None:
		self.client = client
		self.namespace = 'http://www.semanticweb.org/daan/ontologies/2025/2/DAMO#'
		super().__init__()

	async def run(self) -> PipelineResult:
		damo_handboek = self.client['DAMODB']['handboek']
		objecten = await damo_handboek.find().to_list(length=None)

		graph = Graph()
		graph.parse('C:\\Users\\Daan\\Documents\\rdf\\DAMO.ttl', format='ttl')
		DAMO = Namespace('http://www.semanticweb.org/daan/ontologies/2025/2/DAMO#')

		data_properties = {
			'Double': XSD.double,
			'Integer': XSD.integer,
			'SmallInteger': XSD.integer,
			'String': XSD.string,
			'string': XSD.string,
			'Date': XSD.date,
		}

		for object in objecten:
			object_name: str = object['object']
			print(object_name)
			object_definition = object['definitie']
			object_node = DAMO[object_name]

			graph.add((object_node, RDF.type, OWL.Class))
			graph.add((object_node, RDFS.label, Literal(object_name, lang='nl')))
			graph.add((object_node, RDFS.comment, Literal(object_definition, lang='nl')))
			graph.add((object_node, RDFS.subClassOf, DAMO['Object']))

			for attribute in object['attributen']:
				attribute_name = attribute['Attribuutnaam'].replace(' ', '')
				attribute_definition = attribute['Toelichting']
				attribute_node = DAMO[attribute_name]

				is_primitive_data_type = attribute['Type']['value'] in data_properties

				if is_primitive_data_type:
					property_type = data_properties[attribute['Type']['value']]

					graph.add((attribute_node, RDF.type, OWL.DatatypeProperty))
					graph.add((attribute_node, RDFS.domain, object_node))
					graph.add((attribute_node, RDFS.range, property_type))
					graph.add((attribute_node, RDFS.label, Literal(attribute_name, lang='nl')))
					graph.add((attribute_node, RDFS.comment, Literal(attribute_definition, lang='nl')))

					restriction = BNode()
					graph.add((restriction, RDF.type, OWL.Restriction))
					graph.add((restriction, OWL.onProperty, attribute_node))
					graph.add((restriction, OWL.onDataRange, property_type))
					graph.add((restriction, OWL.someValuesFrom, property_type))
					graph.add((object_node, RDFS.subClassOf, restriction))
				else:
					property_type_name = attribute['Type']['value'].replace(' ', '')
					property_type = DAMO[property_type_name]

					graph.add((property_type, RDF.type, OWL.Class))
					graph.add((property_type, RDFS.label, Literal(property_type_name, lang='nl')))

					graph.add((attribute_node, RDF.type, OWL.ObjectProperty))
					graph.add((attribute_node, RDFS.label, Literal(attribute_name, lang='nl')))
					graph.add((attribute_node, RDFS.comment, Literal(attribute_definition, lang='nl')))
					graph.add((attribute_node, RDFS.domain, object_node))
					graph.add((attribute_node, RDFS.range, property_type))

					restriction = BNode()
					graph.add((restriction, RDF.type, OWL.Restriction))
					graph.add((restriction, OWL.onProperty, attribute_node))
					graph.add((restriction, OWL.onClass, property_type))
					graph.add((restriction, OWL.someValuesFrom, property_type))
					graph.add((object_node, RDFS.subClassOf, restriction))

		graph.serialize('test_ontology_2.ttl', format='ttl')

		return {'success': True}

	# async def run(self) -> PipelineResult:
	# damo_handboek = self.client['DAMODB']['handboek']

	# graph = Graph()
	# graph.parse('C:\\Users\\Daan\\Documents\\rdf\\DAMO.ttl', format='ttl')
	# kunstwerk = URIRef(f'{self.namespace}Kunstwerk')

	# if (kunstwerk, None, None) in graph:
	# pprint(list(graph.triples((kunstwerk, None, None))))

	# graph.serialize("test_ontology.ttl", format="ttl")

	# return {'success': True}
