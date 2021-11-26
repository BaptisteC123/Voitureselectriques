# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 10:32:12 2021

@author: user
"""
import openrouteservice
from openrouteservice.directions import directions


def calcul_distance(lat1,lon1,lat2,lon2):
        coords = ((lon1,lat1),(lon2,lat2))
    
        client = openrouteservice.Client(key='5b3ce3597851110001cf6248b29cc9bd2f9d4e0496c4d699c56b0f41') # Specify your personal API key
        routes = directions(client, coords)
        data = []
        data.append(routes['routes'][0]['summary']['distance']/1000)
        data.append(float(routes['routes'][0]['summary']['duration']/3600))
        return data 

#print (calcul_distance(43.703546, 7.217619,49.798027, 2.350944))