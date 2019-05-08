import math
from .models import *
# --------------Metodos de extración ------------------
def total_llamadas(sub_consultas):
	llamadas = 0
	for sc in sub_consultas:
		residuo = sc.total_resultados % 25
		llamadas += math.floor(sc.total_resultados / 25)
		if residuo != 0:
			llamadas += 1
	return llamadas

# -------------- Metodos de extración ------------------
def guardar_publicacion(publication, idjson, pos):
	objPub = None
	dcIdentifier = ''
	try:
		identifier = publication['dc:identifier'].split(':')
		dcIdentifier = identifier[1]
		print(dcIdentifier)
		objPub = ScpPublication.objects.filter(dc_identifier= dcIdentifier).first()
		print(objPub)
		guardar = False
		if objPub == None:
			objPub = ScpPublication()
			guardar = True
		#Armando el objeto
		objPub.dc_title = getvalueJson(publication,'dc:title')
		objPub.prism_url = getvalueJson(publication,'prism:url')
		objPub.dc_identifier = dcIdentifier
		objPub.eid = getvalueJson(publication,'eid')
		objPub.dc_creator = getvalueJson(publication,'dc:creator')
		objPub.prism_publicationname = getvalueJson(publication,'prism:publicationName')
		objPub.prism_issn = getvalueJson(publication,'prism:issn')
		objPub.prism_eissn = getvalueJson(publication,'prism:eIssn')
		objPub.prism_volume = getvalueJson(publication,'prism:volume')
		objPub.prism_pagerange = getvalueJson(publication,'prism:pageRange')
		objPub.prism_coverdate = getvalueJson(publication,'prism:coverDate')
		objPub.prism_coverdisplaydate = getvalueJson(publication,'prism:coverDisplayDate')
		objPub.prism_doi = getvalueJson(publication,'prism:doi')
		objPub.dc_description = getvalueJson(publication,'dc:description')
		objPub.citedby_count = getvalueJson(publication,'citedby-count')
		objPub.prism_aggregationtype = getvalueJson(publication, 'prism:aggregationType')
		objPub.subtype = getvalueJson(publication,'subtype')
		objPub.subtypedescription = getvalueJson(publication,'subtypeDescription')
		objPub.authkeywords = getvalueJson(publication,'authkeywords')
		objPub.intid = getvalueJson(publication,'intid')
		objPub.source_id = getvalueJson(publication,'source-id')
		objPub.article_number = getvalueJson(publication,'article-number')
		objPub.found_acr = getvalueJson(publication,'found_acr')
		objPub.found_sponsor = getvalueJson(publication,'found_sponsor')
		objPub.found_no = getvalueJson(publication,'found_no')
		objPub.pii = getvalueJson(publication,'pii')
		objPub.author_count = getvalueJson(publication,'author_count')
		objPub.prism_issueidentifier = getvalueJson(publication,'prism_issueIdentifier')
		objPub.pubmed_id = getvalueJson(publication,'pubmed_id')
		objPub.scp_json = ScpJson(id=idjson)
		objPub.pos_json = pos
		#GUARDAR Objeto
		objPub.save()
		#Buscar Keywords
		keywordsAuth = getvalueJson(publication,'authkeywords')
		if keywordsAuth != None:
			lstKw = keywordsAuth.split('|')
			for k in lstKw:
				kwObj = ScpPublicationAuthkw()
				kwObj.dc_identifier = objPub.dc_identifier
				kwObj.keyword = k.strip()
				kwObj.scp_publication = objPub
				kwObj.save()
				print('KW Guardada')
		print('Publicación guardada')

		#insertamos en tabla PUBLICATION-AUTHOR KW ***
	except Exception as e:
		raise e
	return objPub


def guardar_afiliacion(afiliation):
	afiliationObj = ScpAffiliation.objects.filter(afid=afiliation['afid']).first()
	if afiliationObj == None:
		afiliationObj = ScpAffiliation()
	afiliationObj.affiliation_url = getvalueJson(afiliation,'affiliation-url')
	afiliationObj.afid = getvalueJson(afiliation,'afid')
	afiliationObj.affilname = getvalueJson(afiliation,'affilname')
	afiliationObj.affiliation_city = getvalueJson(afiliation,'affiliation-city')
	afiliationObj.affiliation_country = getvalueJson(afiliation,'affiliation-country')
	#GuardarObjeto
	afiliationObj.save()
	print('Afiliation Guardado')

	#comprobando Afiliation Variant
	listNV = getvalueJson(afiliation, 'name-variant')
	if listNV != None:
		for n in listNV:
			avObj = ScpAffiliationVariant()
			avObj.name_variant = getvalueJson(n,'$')
			avObj.afid = getvalueJson(n,'afid')
			avObj.scp_affiliation = afiliationObj
			#Guardar Objeto
			avObj.save()
			print('Af Var Guardado')

	return afiliationObj

def guardar_autores(author):
	authorObj = ScpAuthor.objects.filter(authid=author['authid']).first()
	if authorObj == None:
		authorObj = ScpAuthor()
	authorObj.author_url = getvalueJson(author,'author-url')
	authorObj.authid = getvalueJson(author,'authid')
	authorObj.authname = getvalueJson(author,'authname')
	authorObj.given_name = getvalueJson(author,'given-name')
	authorObj.surname = getvalueJson(author,'surname')
	authorObj.initials = getvalueJson(author,'initials')
	#guardar objeto
	authorObj.save()
	print('Author Guardado', authorObj.authid)
	return authorObj


def procesar_json(json):
	entry = json['search-results']['entry']
	for pub in entry:
		pass


# --- Adicionales -----
def remove_duplicates(duplicate):
	final_list = [] 
	for e in duplicate: 
		if e not in final_list: 
			final_list.append(e) 
	return final_list

def getvalueJson(jsonObj, key):
	rta = None
	try:
		rta = jsonObj[key]
	except Exception as e:
		print(e)
	return rta

