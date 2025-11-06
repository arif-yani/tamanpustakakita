import json 
from odoo import SUPERUSER_ID 
from odoo.http import Controller, request, route  
import http.client

DEFAULT_ORIGIN = 2117
 
class RajaOngkir(object): 
    def __init__(self):
        self.rajaongkir = {}

    def get_costs(self, destination, courier, weight, destinationType='subdistrict', origin=False, originType='subdistrict'):
        # origin = origin and origin or DEFAULT_ORIGIN
        # config = request.env['res.company'].Config()
        # if config.origin:
        #     origin = config.origin
            
        payload = "origin=2117"
        payload += "&originType=" + originType
        payload += "&destination=" + str(destination)  
        payload += "&destinationType=" + destinationType
        payload += "&courier=" + str(courier)
        payload += "&weight=" + str(int(weight))

        headers = {
            'key': '2d64870e5a15ace105dc21b453632b61', 
            'content-type': "application/x-www-form-urlencoded" 
        }

        try:
            conn = http.client.HTTPSConnection("pro.rajaongkir.com")
            conn.request("POST", "/api/cost", payload, headers)

        except Exception as e:
            return []

        resp = conn.getresponse()
        data = resp.read()
        data = data.decode("utf-8")

        if resp.status == 200:
            data = json.loads(data)
            rajaongkir = data['rajaongkir'] 
            if rajaongkir['status']['code'] == 200:
                costs = rajaongkir['results'][0]['costs']
                return costs

        return []

    def get_costs_and_destination(self, destination, courier, weight, destinationType='subdistrict', origin=False,originType='subdistrict'):
        origin = origin and origin or DEFAULT_ORIGIN
        config = request.env['res.company'].Config()

        if config.origin:
            origin = config.origin

        payload = "origin=2117" 
        payload += "&originType=" + originType
        payload += "&destination=" + str(destination)  
        payload += "&destinationType=" + destinationType
        payload += "&courier=" + str(courier)
        payload += "&weight=" + str(int(weight))

        headers = {
            'key': '2d64870e5a15ace105dc21b453632b61', 
            'content-type': "application/x-www-form-urlencoded" 
        }

        try:
            conn = http.client.HTTPSConnection("pro.rajaongkir.com")
            conn.request("POST", "/api/cost", payload, headers)

        except Exception as e:
            return []

        resp = conn.getresponse()
        data = resp.read()
        data = data.decode("utf-8")
        
        
        if 'Error' not in str(data) and 'error' not in str(data):
            if resp.status == 200:
                data = json.loads(data)
                rajaongkir = data['rajaongkir']

                if rajaongkir['status']['code'] == 200:
                    results = rajaongkir
                    return results

        return []

    def get_provice(self):
        config = request.env['res.company'].Config()
        headers = { 'key': '2d64870e5a15ace105dc21b453632b61' } 
        conn = http.client.HTTPSConnection("pro.rajaongkir.com")

        try:
            conn.request("GET", "/api/province", headers=headers)

        except Exception as e:
            return []

        resp = conn.getresponse()
        data = resp.read()
        data = data.decode("utf-8")

        if resp.status == 200:
            data = json.loads(data)
            rajaongkir = data['rajaongkir']

            if rajaongkir['status']['code'] == 200:
                results = rajaongkir['results']
                return results

        return []

    def get_all_city(self):
        config = request.env['res.company'].Config()
        headers = { 'key': '2d64870e5a15ace105dc21b453632b61' } 
        conn = http.client.HTTPSConnection("pro.rajaongkir.com")
        url = "/api/city"
        
        try:
            conn.request("GET", url, headers=headers)
        
        except Exception as e:
            return []

        resp = conn.getresponse()
        data = resp.read()
        data = data.decode("utf-8")

        if resp.status == 200:
            data = json.loads(data)
            rajaongkir = data['rajaongkir']

            if rajaongkir['status']['code'] == 200:
                results = rajaongkir['results']
                return results

        return []

    def get_city(self,province):
        config = request.env['res.company'].Config()
        headers = { 'key': '2d64870e5a15ace105dc21b453632b61' } 
        conn = http.client.HTTPSConnection("pro.rajaongkir.com")
        url = "/api/city?province=%s" % str(province)
        
        try:
            conn.request("GET", url, headers=headers)
        
        except Exception as e:
            return []

        resp = conn.getresponse()
        data = resp.read()
        data = data.decode("utf-8") 

        if resp.status == 200:
            data = json.loads(data)
            rajaongkir = data['rajaongkir'] 
            
            if rajaongkir['status']['code'] == 200:
                results = rajaongkir['results']
                return results

        return []

    def get_district(self,city):
        config = request.env['res.company'].Config()
        headers = { 'key': '2d64870e5a15ace105dc21b453632b61' }
        conn = http.client.HTTPSConnection("pro.rajaongkir.com")
        url = "/api/subdistrict?city=%s" % str(city)
        
        try:
            conn.request("GET", url, headers=headers)
        
        except Exception as e:
            return []

        resp = conn.getresponse()
        data = resp.read()
        data = data.decode("utf-8") 
        
        if resp.status == 200:
            data = json.loads(data)
            rajaongkir = data['rajaongkir'] 
            
            if rajaongkir['status']['code'] == 200:
                results = rajaongkir['results']
                return results
        
        return []

    def get_starter_province(self,province):
        config = request.env['res.company'].Config()
        headers = { 'key': '2d64870e5a15ace105dc21b453632b61' }
        conn = http.client.HTTPSConnection("api.rajaongkir.com")
        url = "/starter/province?id=%s" % str(province)
        
        try:
            conn.request("GET", url, headers=headers)
        
        except Exception as e:
            return []

        resp = conn.getresponse()
        data = resp.read()
        data = data.decode("utf-8") 
        
        if resp.status == 200:
            data = json.loads(data)
            rajaongkir = data['rajaongkir'] 
            
            if rajaongkir['status']['code'] == 200:
                results = rajaongkir['results']
                return results

        return []

    def get_starter_city(self,city):
        config = request.env['res.company'].Config()
        headers = { 'key': '2d64870e5a15ace105dc21b453632b61' }
        conn = http.client.HTTPSConnection("api.rajaongkir.com")
        url = "/starter/city?id=%s" % str(city) 
        
        try:
            conn.request("GET", url, headers=headers)
        
        except Exception as e:
            return []

        resp = conn.getresponse()
        data = resp.read()
        data = data.decode("utf-8") 
        
        if resp.status == 200:
            data = json.loads(data)
            rajaongkir = data['rajaongkir'] 
            
            if rajaongkir['status']['code'] == 200:
                results = rajaongkir['results']
                return results
                
        return []

    def get_waybill_information(self, courier, waybill):
        config = request.env['res.company'].Config()
        conn = http.client.HTTPSConnection("pro.rajaongkir.com")
        headers = { 
            'key': '2d64870e5a15ace105dc21b453632b61',
            'content-type': "application/x-www-form-urlencoded" 
        }
        payload = "courier=%s&waybill=%s"%(str(courier), str(waybill))

        try: 
            conn.request("POST", "/api/waybill", payload, headers)
            resp = conn.getresponse()
            data = resp.read()
            data = data.decode("utf-8")
            if resp.status == 200:
                data = json.loads(data)
                return data
        except Exception as e:
            pass

        return []