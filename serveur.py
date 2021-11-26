# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 10:06:27 2021

@author: user
"""

from flask import Flask, render_template, request, jsonify
from geopy.geocoders import Nominatim 
from openrouteservice.directions import directions
from soap import calcul_distance
from sql import get_voiture

import Client_SOAP as SOAP

import math
import requests
import folium

import openrouteservice



start_coords = []
end_coords = []
pointPath = []
coord_borne = []
liste_borne = []
app = Flask(__name__)

@app.route('/')
def home():
    car = get_voiture()

    return render_template('index.html', voiture = car)
 
    
@app.route('/calcul', methods=['POST'])
    
def get_values():
    start_coords.clear()
    end_coords.clear()    
    
    result=request.form
    ville1=result["ville1"]
    ville2=result["ville2"]
 
    
    autonomie=result["autonomie"]
    loc = Nominatim(user_agent="GetLoc")
    
    getLoc1 = loc.geocode(ville1)
    getLoc2 = loc.geocode(ville2)
  
    lon1=getLoc1.longitude
    lat1=getLoc1.latitude
    lon2=getLoc2.longitude
    lat2=getLoc2.latitude

    start_coords.append(lat1)
    start_coords.append(lon1)
    end_coords.append(lat2)
    end_coords.append(lon2)
    
    
    distance_parcourue=SOAP.calcul_distance(lat1,lon1,lat2,lon2)
    
    nbr_recharge =  math.ceil(int(distance_parcourue[0]) / float(autonomie))
    
    v_lat = (float(lat2) - float(lat1)) / nbr_recharge
    v_lng = (float(lon2) - float(lon1)) / nbr_recharge
        
    point_lat = float(lat1)
    point_lng = float(lon1)
        
        
    pointPath = []
    point = []

    for i in range(nbr_recharge-1):
         point_lat = point_lat + float(v_lat)
         point_lng = point_lng + float(v_lng)
         point.append(point_lat)
         point.append(point_lng)
         borne = api(point_lng, point_lat, 50000)
         coord_borne.append(point_lat)
         coord_borne.append(point_lng)
         liste_borne.append(borne)
         pointPath.append(get_city(borne))
         point = []
         
        
    
    return render_template('calcul.html',distance=round(distance_parcourue[0],2), duree=round(distance_parcourue[1],2),borne=pointPath, nbr=nbr_recharge)


@app.route('/api', methods=['POST'])
def api(borne_lon,borne_lat,autonomie):
    
    url = "https://opendata.reseaux-energies.fr/api/records/1.0/search/?dataset=bornes-irve&q=&facet=region&geofilter.distance="+str(borne_lat)+"%2C+"+str(borne_lon)+"%2C+"+str(autonomie)+""

    r = requests.get(url)
    rjson=r.json()

    position = []
    position.append(rjson['records'][0]['fields']['ylatitude'])
    position.append(rjson['records'][0]['fields']['xlongitude'])
    
    
    return position



@app.route('/loc')
def fonct():
    loc = Nominatim(user_agent="GetLoc") 
    getLoc = loc.geocode("peillonex") 
    prince =  "test "+getLoc.address+"\n lat :" + str(getLoc.latitude)+ " long: "+str(getLoc.longitude)
    return prince

@app.route('/con')
def con():
    coords = ((8.34234,48.23424),(8.34423,48.26424))

    client = openrouteservice.Client(key='5b3ce3597851110001cf6248b29cc9bd2f9d4e0496c4d699c56b0f41') # Specify your personal API key
    routes = directions(client, coords)
    
    return routes

def get_city(pos):
    loc = Nominatim(user_agent="GetLoc")
    location = loc.reverse(pos)

    return location.address


@app.route('/map', methods=['POST'])
def map():
    
    tooltip = "Borne"
    folium_map = folium.Map(location=start_coords, zoom_start=7)
    
    
    depart = folium.Marker(start_coords, popup="<i>Ville de départ</i>", tooltip="Départ")
    depart.add_to(folium_map)
    arrivee = folium.Marker(end_coords, popup="<i>Ville d'arrivée</i>", tooltip="Arrivée")
    arrivee.add_to(folium_map)
    
   
    for i in range(len(liste_borne)):
        mark = folium.Marker(liste_borne[i], popup="<i>Borne à utiliser</i>", tooltip=tooltip+" n°"+str(i+1), icon=folium.Icon(color="green"))
        
        mark.add_to(folium_map)
    
    return folium_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)