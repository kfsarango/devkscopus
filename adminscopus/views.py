from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from django.utils import timezone
from .serializers import *
from .functions import *
from .models import *

import requests
import json
import datetime

HOST = 'https://api.elsevier.com/content/search/scopus'
AK = '06ae77e56373588d4e00bbd2f9b494e8'
YEAR = datetime.datetime.now().year


# Create your views here.
def get_entries(url):
    res = requests.get(url)
    if res.status_code != 200:
        # algo salio mal
        raise ApiError(url + ' {}'.format(res.status_code))
    return res.text


def makeRequest(url):
    res = requests.get(url)
    if res.status_code != 200:
        # algo salio mal
        raise ApiError(url + ' {}'.format(res.status_code))
    data_string = json.dumps(res.json())
    return json.loads(data_string)


def getYear():
    now = datetime.datetime.now()
    return now.year()


class consultas(generics.ListAPIView):
    serializer_class = ProyectoSerializer

    def get_queryset(self):

        # Procesamiento de consultas
        country = self.kwargs['country']
        myProyect = ScpProyecto.objects.filter(nombre=country).first()
        if myProyect == None:
            myProyect = ScpProyecto()
            myProyect.nombre = country
            myProyect.register = timezone.now()
            myProyect.scp_usuario = ScpUsuario(id=1)
            myProyect.save()
            print('Proyecto Guardado')
        sentence = 'AFFILCOUNTRY(' + myProyect.nombre + ')'
        myConsultaObj = guardar_consulta(sentence, myProyect.id)

        # Procesamiento de subconsultas
        anio_start = 2012
        country = myProyect.nombre
        sentence = 'AFFILCOUNTRY(' + country + ')'
        listSentences = []
        # Ajustando numero de publicaciones hasta un cierto año
        while True:
            query_sentence = sentence + ' AND PUBYEAR BEF ' + str(anio_start)
            rtaSubconsulta = resultados_subconsulta(query_sentence)
            publicaciones = rtaSubconsulta[0]
            urlSunconsulta = rtaSubconsulta[1]
            if publicaciones < 5000:
                # La sentencia es valida
                listSentences.append([query_sentence, publicaciones, urlSunconsulta])
                break
            else:
                anio_start = anio_start - 1
            query_sentence = ''

        # Haciendo subconsultas a partir de una año
        anio_start -= 1
        anio_range_limit = anio_start + 2
        last_nro_publicaciones = 0
        last_sentence = ''
        for x in range(anio_start, YEAR):
            # Subconsulta por rangos de años
            # print ('\n\nIniciando bucle: as',anio_start)
            while anio_range_limit <= YEAR:
                query_sentence = sentence + ' AND PUBYEAR AFT ' + str(anio_start) + ' AND PUBYEAR BEF ' + str(
                    anio_range_limit)
                rtaSubconsulta = resultados_subconsulta(query_sentence)
                publicaciones = rtaSubconsulta[0]
                urlSunconsulta = rtaSubconsulta[1]
                # print('Nro R. in Range: ', publicaciones)
                if publicaciones < 5000:
                    anio_range_limit += 1
                    last_nro_publicaciones = publicaciones
                    last_sentence = query_sentence
                    last_url = urlSunconsulta
                else:
                    anio_start = anio_range_limit - 2
                    break
                query_sentence = None
            # print('anio_start in while: ', anio_start)
            listSentences.append([last_sentence, last_nro_publicaciones, last_url])
        # Se hace ultima consulta para el año actual en adelante
        query_sentence = sentence + ' AND PUBYEAR AFT ' + str(YEAR - 1)
        rtaSubconsulta = resultados_subconsulta(query_sentence)
        publicaciones = rtaSubconsulta[0]
        urlSunconsulta = rtaSubconsulta[1]
        listSentences.append([query_sentence, publicaciones, urlSunconsulta])

        listSentences = remove_duplicates(listSentences)

        # Guardando Subconsultas
        for sc in listSentences:
            subconsultaObj = ScpSubconsulta()
            subconsultaObj.nombre = sc[0]
            subconsultaObj.total_resultados = sc[1]
            subconsultaObj.cosechado = False
            subconsultaObj.register = timezone.now()
            subconsultaObj.link = sc[2]
            subconsultaObj.scp_consulta = myConsultaObj
            subconsultaObj.save()
            print('Guardando SUBCONSULTA')

        return myProyect


class proyecto(generics.ListAPIView):
    serializer_class = ProyectoSerializer

    def get_queryset(self):
        pass
        return None


# extraccion OK
class extraccion(generics.ListAPIView):
    serializer_class = ProyectoSerializer

    def get_queryset(self):
        avance = 0
        country = self.kwargs['country']
        # recuperando consultas
        consultas = ScpConsulta.objects.filter(proyecto__nombre=country, estado=False)
        for c in consultas:
            # recuperando Subconsultas
            sub_consultas = ScpSubconsulta.objects.filter(scp_consulta=c.id, cosechado=False)
            llamadas = total_llamadas(sub_consultas)
            for s_c in sub_consultas:
                parametros = '?query=' + s_c.nombre.replace(' ',
                                                            '%20') + '&apikey=' + AK + '&view=COMPLETE&httpAccept=application/json'
                url = HOST + parametros
                pag = 24
                count = '&count=1'
                count_2 = '&count=' + str(pag + 1)
                print('\n', s_c.nombre)
                # print(url+count)

                countResults = contarNumeroPublicaciones(url + count)
                # paginando
                myCont = 0
                while myCont < countResults:
                    # hacer un requests, para obtener la paginación
                    linkToextract = url + str(count_2) + "&start=" + str(myCont)
                    myRtaJson = get_entries(linkToextract)
                    # guardando json
                    jsonObj = ScpJson()
                    jsonObj.json = myRtaJson
                    jsonObj.register = timezone.now()
                    jsonObj.total_resultados = len(json.loads(myRtaJson)['search-results']['entry'])
                    jsonObj.desde = myCont
                    jsonObj.hasta = myCont + pag
                    jsonObj.link = linkToextract
                    jsonObj.procesado = False
                    jsonObj.scp_subconsulta = s_c
                    # GUARDAR objeto
                    try:
                        jsonObj.save()
                    except Exception as e:
                        print('Exception: {}'.format(e))
                    print('json guardado')

                    myCont = myCont + pag + 1
                # Actualizar subconsulta
                s_c.cosechado = True
                # ACTUALIZAR
                s_c.save()
                print('Subconsulta ', s_c.nombre, ' EXTRAIDO')
                print('\n\n\t\t', list(sub_consultas).index(s_c), ' / ', len(sub_consultas))
        print('EXTRACCION END')
        return 1


class procesamiento(generics.ListAPIView):
    serializer_class = ProyectoSerializer

    def get_queryset(self):
        country = self.kwargs['country']
        # El procesamiento se lo realiza por Proyecto(País)
        jsonRows = ScpJson.objects.filter(scp_subconsulta__scp_consulta__proyecto__nombre=country, procesado=False)
        for j in jsonRows:
            entries = json.loads(j.json)
            entries = entries['search-results']['entry']
            for pub in entries:
                # guardar publicacion ok
                publicacion = guardar_publicacion(pub, j.id, entries.index(pub))
                # afiliaciones
                affs = getvalueJson(pub, 'affiliation')
                if affs != None:
                    # recorriendo afiliaciones
                    for a in affs:
                        afiliacion = guardar_afiliacion(a)
                        # inserción de PUBLICACIÓN-AFILIACIÓN ***
                        pub_affObj = ScpPublicationAffiliation.objects.filter(scp_publication=publicacion.id,
                                                                              scp_affiliation=afiliacion.id).first()
                        if pub_affObj == None:
                            pub_affObj = ScpPublicationAffiliation()
                        pub_affObj.dc_identifier = publicacion.dc_identifier if publicacion != None else None
                        pub_affObj.afid = afiliacion.afid if afiliacion != None else None
                        pub_affObj.scp_publication = publicacion
                        pub_affObj.scp_affiliation = afiliacion
                        # guardar objeto
                        pub_affObj.save()
                        print('Pub Aff Guardado')

                # inserción de los AUTORES ***
                auths = getvalueJson(pub, 'author')
                if auths != None:
                    for a in auths:
                        autor = guardar_autores(a)
                        # inserción de PUBLICACIÓN-AFILIACIÓN-AUTOR ***
                        orden = -1
                        try:
                            orden = int(a['@seq'])
                        except Exception as e:
                            print(e)
                        affids = getvalueJson(a, 'afid')
                        if affids != None:
                            for af in affids:
                                afid = getvalueJson(af, '$')
                                affObj = ScpAffiliation.objects.filter(afid=afid).first()
                                au_affObj = ScpAuthorAffiliation.objects.filter(scp_publication=publicacion.id,
                                                                                scp_author=autor.id).first()
                                if au_affObj == None:
                                    au_affObj = ScpAuthorAffiliation()
                                au_affObj.dc_identifier = publicacion.dc_identifier if publicacion != None else None
                                au_affObj.authid = autor.authid if autor != None else None
                                au_affObj.afid = afiliacion.afid
                                au_affObj.orden = orden
                                au_affObj.scp_publication = publicacion
                                au_affObj.scp_author = autor
                                au_affObj.scp_affiliation = affObj
                                # guardar Obj
                                au_affObj.save()
                                print('Auth Aff Guardado')
                        else:
                            au_affObj = ScpAuthorAffiliation.objects.filter(scp_publication=publicacion.id,
                                                                            scp_author=autor.id).first()
                            if au_affObj == None:
                                au_affObj = ScpAuthorAffiliation()
                            au_affObj.dc_identifier = publicacion.dc_identifier if publicacion != None else None
                            au_affObj.authid = autor.authid if autor != None else None
                            au_affObj.afid = afid
                            au_affObj.orden = orden
                            au_affObj.scp_publication = publicacion
                            au_affObj.scp_author = autor
                            au_affObj.scp_affiliation = afiliacion
                            # guardar Obj
                            au_affObj.save()
                            print('Auth Aff-2 Guardado')
                print('\t\tPublicaciones ', entries.index(pub), ' / ', len(entries))
            # actualizando Json Obj
            j.procesado = True
            j.save()
            print('Json Actualizado -> True')
            print('\n\t', list(jsonRows).index(j), ' / ', len(jsonRows))
        # Actualizando consulta y subconsulta
        # proyecto = ScpProyecto.objects.filter(nombre=country).first()
        # consulta = ScpConsulta.objects.filter(proyecto=proyecto.id).first()
        # consulta.estado = True
        print('Process END')
        return 1


def guardar_consulta(sentence, idProyecto):
    query = '?query=' + sentence
    url = HOST + query + '&apikey=' + AK + '&view=COMPLETE&httpAccept=application/json&count=1'
    rta = makeRequest(url)
    # the result is a Python dictionary:
    nro_of_results = rta['search-results']['opensearch:totalResults']

    proyectoObj = ScpProyecto(id=idProyecto)

    consultaObj = ScpConsulta()
    consultaObj.nombre = sentence
    consultaObj.total_resultados = nro_of_results
    consultaObj.register = timezone.now()
    consultaObj.estado = False
    consultaObj.link = url
    consultaObj.proyecto = proyectoObj
    # GUARDAR Objeto
    consultaObj.save()

    print('Consulta ', consultaObj.nombre, ' GAURDADO')
    return consultaObj


def resultados_subconsulta(sentence):
    # print(sentence)
    sentence = sentence.replace(' ', '%20')
    url = HOST + '?query=' + sentence + '&apikey=' + AK + '&view=COMPLETE&httpAccept=application/json'
    # print(url)
    rta = makeRequest(url)
    nro_of_results = rta['search-results']['opensearch:totalResults']
    return [int(nro_of_results), url]


def contarNumeroPublicaciones(url):
    rta = makeRequest(url)
    nro_of_results = rta['search-results']['opensearch:totalResults']
    return int(nro_of_results)
