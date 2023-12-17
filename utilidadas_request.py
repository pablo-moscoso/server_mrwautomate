import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)
import requests
#from conf import apikey
import os

import requests


def sacar_id(albaran):

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Authorization': apikey,
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'https://www2-vpc.mrw.es',
        'Pragma': 'no-cache',
        'Referer': 'https://www2-vpc.mrw.es/gestion3/Operativo/Envios/BuscadorEnvios',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'Pagina': 1,
        'Registros': 20,
        'Orden': "{ 'FechaRecogida' : -1}",
        'Filtro' : '{{ $and: [{{ albaran : "{}"}}] }}#',
        'RolFranquicia': None,
        'IdClienteFranquicia': '',
        'EsEdicion': '',
        'NumeroAlbaranPrecursor': '',
    }

    response = requests.post(
        'https://www2-vpc.mrw.es/Gestion3WebService/WebServicesUI/Operativa.WS.Envio/Envio/BuscarEnvios',
        headers=headers,
        json=json_data,
        verify=False
    )
    return response.json()


def request_id(albaran, apikey):

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'es-419,es;q=0.9',
        'Authorization': apikey,
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'https://www2-vpc.mrw.es',
        'Pragma': 'no-cache',
        'Referer': 'https://www2-vpc.mrw.es/gestion3/Operativo/Envios/BuscadorEnviosHistorico',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'Registros': 20,
        'Albaran': albaran,
        'FechaDesde': '2023-08-06T22:00:00.000Z',
        'FechaHasta': '2028-12-24T22:00:00.000Z',
        'Filtro': '{ $and: [ ]}#'
    }

    response = requests.post(
        'https://www2-vpc.mrw.es/Gestion3WebService/WebServicesUI/Mrw.Operativa.Enviohistory.WebService/Buscador/SearchDeliveries',
        headers=headers,
        json=json_data,
        verify=False

    )
    return response.json()



def request_print(id_envio, envio_modificado, apikey):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
        'Accept': '*/*',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://www2-vpc.mrw.es/gestion3/',
        'Origin': 'https://www2-vpc.mrw.es',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        'Content-Type': 'application/json',
        'Authorization': apikey,
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    json_data = {
        'Datos': [
            id_envio,
        ],
        'Informe': 'EtiquetaMRW',
    }

    response = requests.post(
        'https://www2-vpc.mrw.es/Gestion3WebService/WebServicesUI/Operativa.WS.Informes/Etiquetas/ImprimirHtml',
        headers=headers,
        json=json_data,
        verify=False
    )
    file_path = os.path.join("etiquetas", f"{envio_modificado}.pdf")
    if not os.path.exists("etiquetas"):
        os.mkdir("etiquetas")
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return response
