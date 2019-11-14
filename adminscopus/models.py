# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Hub(models.Model):
    identifier = models.CharField(max_length=255)
    label = models.TextField(db_column='LABEL')  # Field name made lowercase.
    description = models.TextField(db_column='DESCRIPTION', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    subtype = models.CharField(db_column='SUBTYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    subjectarea = models.CharField(db_column='SUBJECTAREA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    year = models.IntegerField(db_column='YEAR')  # Field name made lowercase.
    language = models.CharField(db_column='LANGUAGE', max_length=50)  # Field name made lowercase.
    organization = models.CharField(db_column='ORGANIZATION', max_length=255)  # Field name made lowercase.
    source = models.CharField(db_column='SOURCE', max_length=50)  # Field name made lowercase.
    link = models.CharField(db_column='LINK', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = '_hub'


class Autores(models.Model):
    nombre = models.CharField(max_length=45, blank=True, null=True)
    primer_nombre = models.CharField(max_length=45, blank=True, null=True)
    segundo_nombre = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'autores'


class GenderApi(models.Model):
    name_base = models.CharField(max_length=45, blank=True, null=True)
    name_sanitized = models.CharField(max_length=45, blank=True, null=True)
    gender = models.CharField(max_length=45, blank=True, null=True)
    samples = models.CharField(max_length=45, blank=True, null=True)
    accuracy = models.CharField(max_length=45, blank=True, null=True)
    source = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'gender_api'


class GenderApiV2(models.Model):
    name_base = models.CharField(max_length=45, blank=True, null=True)
    name_sanitized = models.CharField(max_length=45, blank=True, null=True)
    gender = models.CharField(max_length=45, blank=True, null=True)
    samples = models.CharField(max_length=45, blank=True, null=True)
    accuracy = models.CharField(max_length=45, blank=True, null=True)
    source = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'gender_api_v2'


class GsAuthor(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    citedby = models.IntegerField(blank=True, null=True)
    workplace = models.CharField(max_length=1000, blank=True, null=True)
    authid_scopus = models.CharField(max_length=45, blank=True, null=True)
    url_perfil = models.CharField(max_length=500, blank=True, null=True)
    html_perfil = models.TextField(blank=True, null=True)
    auth_kw = models.CharField(max_length=1000, blank=True, null=True)
    url_image = models.CharField(max_length=1000, blank=True, null=True)
    name_search = models.CharField(max_length=100, blank=True, null=True)
    register = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'gs_author'


class GsAuthorKw(models.Model):
    kw = models.CharField(max_length=500, blank=True, null=True)
    url_auth_similar = models.CharField(max_length=1000, blank=True, null=True)
    gs_perfil = models.ForeignKey('GsPerfil', models.DO_NOTHING, db_column='gs_perfil', default="1")
    register = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'gs_author_kw'


class GsAuthorPublication(models.Model):
    gs_perfil = models.ForeignKey('GsPerfil', models.DO_NOTHING, db_column='gs_perfil', default="1")
    gs_publication = models.ForeignKey('GsPublication', models.DO_NOTHING, db_column='gs_publication', default="1")

    class Meta:
        managed = True
        db_table = 'gs_author_publication'


class GsHtml(models.Model):
    gs_perfil = models.ForeignKey('GsPerfil', models.DO_NOTHING, db_column='gs_perfil', default="1")
    url_publications_page = models.CharField(max_length=1000, blank=True, null=True)
    html_publications = models.TextField(blank=True, null=True)
    register = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'gs_html'


class GsPerfil(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    citedby = models.IntegerField(blank=True, null=True)
    workplace = models.CharField(max_length=1000, blank=True, null=True)
    url_perfil = models.CharField(max_length=500, blank=True, null=True)
    auth_kw = models.CharField(max_length=1000, blank=True, null=True)
    url_image = models.CharField(max_length=1000, blank=True, null=True)
    name_search = models.CharField(max_length=100, blank=True, null=True)
    register = models.DateTimeField(blank=True, null=True)
    gs_author = models.ForeignKey(GsAuthor, models.DO_NOTHING, db_column='gs_author', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'gs_perfil'


class GsPublication(models.Model):
    title = models.TextField(blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    doi = models.CharField(max_length=200, blank=True, null=True)
    magazine = models.CharField(max_length=1000, blank=True, null=True)
    article_link = models.CharField(max_length=1000, blank=True, null=True)
    publication_date = models.CharField(max_length=45, blank=True, null=True)
    volume = models.CharField(max_length=45, blank=True, null=True)
    number = models.CharField(max_length=45, blank=True, null=True)
    pages = models.CharField(max_length=45, blank=True, null=True)
    publisher = models.CharField(max_length=1000, blank=True, null=True)
    total_citation = models.IntegerField(blank=True, null=True)
    medio = models.CharField(max_length=45, blank=True, null=True)
    authors = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'gs_publication'


class ProvidersOai(models.Model):
    baseurl = models.CharField(db_column='baseURL', unique=True, max_length=255)  # Field name made lowercase.
    informationurl = models.CharField(db_column='informationURL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    statushttp = models.IntegerField(db_column='statusHTTP')  # Field name made lowercase.
    repositoryname = models.TextField(db_column='repositoryName', blank=True, null=True)  # Field name made lowercase.
    repositorysoftware = models.CharField(db_column='repositorySoftware', max_length=255, blank=True, null=True)  # Field name made lowercase.
    repositoryidentifier = models.CharField(db_column='repositoryIdentifier', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sampleidentifier = models.CharField(db_column='sampleIdentifier', max_length=255, blank=True, null=True)  # Field name made lowercase.
    adminemail = models.CharField(db_column='adminEmail', max_length=255, blank=True, null=True)  # Field name made lowercase.
    protocolversion = models.CharField(db_column='protocolVersion', max_length=25, blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(max_length=255, blank=True, null=True)
    harvestsets = models.IntegerField(db_column='harvestSets')  # Field name made lowercase.
    processsets = models.IntegerField(db_column='processSets')  # Field name made lowercase.
    harvestxml = models.IntegerField(db_column='harvestXML')  # Field name made lowercase.
    processxml = models.IntegerField(db_column='processXML')  # Field name made lowercase.
    organization = models.TextField(blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    country_name = models.CharField(max_length=100, blank=True, null=True)
    region_name = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    team = models.CharField(max_length=255, blank=True, null=True)
    lastresumptiontoken = models.CharField(db_column='lastResumptionToken', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lastresumptiontokensets = models.CharField(db_column='lastResumptionTokenSets', max_length=255, blank=True, null=True)  # Field name made lowercase.
    siglas = models.CharField(max_length=255, blank=True, null=True)
    identifier = models.CharField(db_column='Identifier', max_length=255, blank=True, null=True)  # Field name made lowercase.
    scopus_identifier = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'providers_OAI'


class ProvidersEquiv(models.Model):
    provider_oai = models.ForeignKey(ProvidersOai, models.DO_NOTHING, db_column='provider_oai', blank=True, null=True)
    identifier = models.BigIntegerField(unique=True, blank=True, null=True)
    name_variant = models.CharField(max_length=1000, blank=True, null=True)
    siglas = models.CharField(max_length=45, blank=True, null=True)
    fuente = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'providers_equiv'


class ScpAffiliation(models.Model):
    affiliation_url = models.CharField(max_length=500, blank=True, null=True)
    afid = models.BigIntegerField()
    affilname = models.CharField(max_length=500, blank=True, null=True)
    affiliation_city = models.CharField(max_length=200, blank=True, null=True)
    affiliation_country = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'scp_affiliation'


class ScpAffiliationVariant(models.Model):
    name_variant = models.CharField(max_length=1000, blank=True, null=True)
    afid = models.BigIntegerField(blank=True, null=True)
    scp_affiliation = models.ForeignKey(ScpAffiliation, models.DO_NOTHING, db_column='scp_affiliation', null=True)

    class Meta:
        managed = True
        db_table = 'scp_affiliation_variant'


class ScpAuth(models.Model):
    scp_usuario = models.ForeignKey('ScpUsuario', models.DO_NOTHING, db_column='scp_usuario', null=True)
    user = models.CharField(max_length=45, blank=True, null=True)
    clave = models.CharField(max_length=45, blank=True, null=True)
    ultimo_ingreso = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'scp_auth'


class ScpAuthor(models.Model):
    author_url = models.CharField(max_length=500, blank=True, null=True)
    authid = models.BigIntegerField()
    authname = models.CharField(max_length=200, blank=True, null=True)
    given_name = models.CharField(max_length=45, blank=True, null=True)
    surname = models.CharField(max_length=500, blank=True, null=True)
    initials = models.CharField(max_length=45, blank=True, null=True)
    document_count = models.IntegerField(blank=True, null=True)
    eid = models.CharField(max_length=50, blank=True, null=True)
    orcid = models.CharField(max_length=50, blank=True, null=True)
    download = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    samples = models.IntegerField(blank=True, null=True)
    accuracy = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'scp_author'


class ScpAuthorAffiliation(models.Model):
    dc_identifier = models.BigIntegerField()
    authid = models.BigIntegerField(blank=True, null=True)
    afid = models.BigIntegerField(blank=True, null=True)
    orden = models.IntegerField(blank=True, null=True)
    scp_publication = models.ForeignKey('ScpPublication', models.DO_NOTHING, db_column='scp_publication', null=True)
    scp_author = models.ForeignKey(ScpAuthor, models.DO_NOTHING, db_column='scp_author', blank=True, null=True)
    scp_affiliation = models.ForeignKey(ScpAffiliation, models.DO_NOTHING, db_column='scp_affiliation', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'scp_author_affiliation'


class ScpFuncionalidad(models.Model):
    padre = models.CharField(max_length=45, blank=True, null=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)
    url = models.CharField(max_length=45, blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    icono = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'scp_funcionalidad'

class ScpJson(models.Model):
    json = models.TextField(blank=True, null=True)
    register = models.DateTimeField(blank=True, null=True)
    total_resultados = models.IntegerField(blank=True, null=True)
    desde = models.IntegerField(blank=True, null=True)
    hasta = models.IntegerField(blank=True, null=True)
    link = models.CharField(max_length=1000, blank=True, null=True)
    procesado = models.IntegerField(blank=True, null=True)
    scp_subconsulta = models.ForeignKey('ScpSubconsulta', models.DO_NOTHING, db_column='scp_subconsulta', null=True)

    class Meta:
        managed = True
        db_table = 'scp_json'

    def __unicode__(self):
        return '%s | %s | %s | %s | %s | %s | %s | %s' % (self.json, self.register, self.total_resultados, self.desde, self.hasta, self.link, self.procesado, self.scp_subconsulta)

class ScpPublication(models.Model):
    dc_title = models.CharField(max_length=2000, blank=True, null=True)
    prism_url = models.CharField(max_length=500, blank=True, null=True)
    dc_identifier = models.BigIntegerField()
    eid = models.CharField(max_length=50, blank=True, null=True)
    dc_creator = models.CharField(max_length=50, blank=True, null=True)
    prism_publicationname = models.CharField(db_column='prism_publicationName', max_length=500, blank=True, null=True)  # Field name made lowercase.
    prism_issn = models.CharField(max_length=50, blank=True, null=True)
    prism_eissn = models.CharField(max_length=50, blank=True, null=True)
    prism_volume = models.CharField(max_length=200, blank=True, null=True)
    prism_pagerange = models.CharField(db_column='prism_pageRange', max_length=45, blank=True, null=True)  # Field name made lowercase.
    prism_coverdate = models.CharField(db_column='prism_coverDate', max_length=45, blank=True, null=True)  # Field name made lowercase.
    prism_coverdisplaydate = models.CharField(db_column='prism_coverDisplayDate', max_length=45, blank=True, null=True)  # Field name made lowercase.
    prism_doi = models.CharField(max_length=100, blank=True, null=True)
    dc_description = models.CharField(max_length=10000, blank=True, null=True)
    citedby_count = models.IntegerField(blank=True, null=True)
    prism_aggregationtype = models.CharField(db_column='prism_aggregationType', max_length=45, blank=True, null=True)  # Field name made lowercase.
    subtype = models.CharField(max_length=45, blank=True, null=True)
    subtypedescription = models.CharField(db_column='subtypeDescription', max_length=45, blank=True, null=True)  # Field name made lowercase.
    authkeywords = models.CharField(max_length=5000, blank=True, null=True)
    intid = models.IntegerField(db_column='intId', blank=True, null=True)  # Field name made lowercase.
    source_id = models.CharField(max_length=45, blank=True, null=True)
    article_number = models.CharField(max_length=100, blank=True, null=True)
    found_acr = models.CharField(max_length=500, blank=True, null=True)
    found_sponsor = models.CharField(max_length=500, blank=True, null=True)
    found_no = models.CharField(max_length=500, blank=True, null=True)
    pii = models.CharField(max_length=100, blank=True, null=True)
    author_count = models.IntegerField(blank=True, null=True)
    prism_issueidentifier = models.CharField(db_column='prism_issueIdentifier', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pubmed_id = models.IntegerField(blank=True, null=True)
    scp_json = models.ForeignKey(ScpJson, models.DO_NOTHING, db_column='scp_json', null=True)
    pos_json = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'scp_publication'


class ScpPublicationAffiliation(models.Model):
    dc_identifier = models.BigIntegerField()
    afid = models.BigIntegerField(blank=True, null=True)
    scp_publication = models.ForeignKey(ScpPublication, models.DO_NOTHING, db_column='scp_publication', null=True)
    scp_affiliation = models.ForeignKey(ScpAffiliation, models.DO_NOTHING, db_column='scp_affiliation', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'scp_publication_affiliation'


class ScpPublicationAuthkw(models.Model):
    dc_identifier = models.BigIntegerField(blank=True, null=True)
    keyword = models.CharField(max_length=1000, blank=True, null=True)
    scp_publication = models.ForeignKey(ScpPublication, models.DO_NOTHING, db_column='scp_publication', null=True)

    class Meta:
        managed = True
        db_table = 'scp_publication_authkw'


class ScpRol(models.Model):
    nombre = models.CharField(max_length=45, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'scp_rol'


class ScpRolFuncionalidad(models.Model):
    scp_funcionalidad = models.ForeignKey(ScpFuncionalidad, models.DO_NOTHING, db_column='scp_funcionalidad', null=True)
    scp_usuario = models.ForeignKey('ScpUsuario', models.DO_NOTHING, db_column='scp_usuario',null=True)

    class Meta:
        managed = True
        db_table = 'scp_rol_funcionalidad'


class ScpRolUsuario(models.Model):
    scp_rol = models.ForeignKey(ScpRol, models.DO_NOTHING, db_column='scp_rol', null=True)
    scp_usuario = models.ForeignKey('ScpUsuario', models.DO_NOTHING, db_column='scp_usuario', null=True)

    class Meta:
        managed = True
        db_table = 'scp_rol_usuario'

class ScpConsulta(models.Model):
    nombre = models.CharField(max_length=500, blank=True, null=True)
    total_resultados = models.IntegerField(blank=True, null=True)
    register = models.DateTimeField(blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    link = models.CharField(max_length=500, blank=True, null=True)
    proyecto = models.ForeignKey('ScpProyecto', models.DO_NOTHING, db_column='proyecto', null=True)

    class Meta:
        managed = True
        db_table = 'scp_consulta'


class ScpSubconsulta(models.Model):
    nombre = models.CharField(max_length=500, blank=True, null=True)
    total_resultados = models.IntegerField(blank=True, null=True)
    cosechado = models.IntegerField(blank=True, null=True)
    register = models.DateTimeField(blank=True, null=True)
    link = models.CharField(max_length=1500, blank=True, null=True)
    scp_consulta = models.ForeignKey(ScpConsulta, models.DO_NOTHING, db_column='scp_consulta', null=True)

    class Meta:
        managed = True
        db_table = 'scp_subconsulta'




class ScpProyecto(models.Model):
    nombre = models.CharField(max_length=200, blank=True, null=True)
    descripcion = models.CharField(max_length=1000, blank=True, null=True)
    register = models.DateTimeField(blank=True, null=True)
    apikey = models.CharField(max_length=45, blank=True, null=True)
    tipo = models.CharField(max_length=45, blank=True, null=True)
    scp_usuario = models.ForeignKey('ScpUsuario', models.DO_NOTHING, db_column='scp_usuario', null=True)

    class Meta:
        managed = True
        db_table = 'scp_proyecto'

class ScpUsuario(models.Model):
    nombre = models.CharField(max_length=45, blank=True, null=True)
    correo = models.CharField(max_length=45, blank=True, null=True)
    usuario = models.CharField(max_length=45, blank=True, null=True)
    register = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'scp_usuario'

