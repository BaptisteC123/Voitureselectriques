import zeep

def calcul_distance(lat1,lon1,lat2,lon2):
    wsdl = 'http://127.0.0.1:8000/?wsdl'
    client = zeep.Client(wsdl=wsdl)
    return client.service.calcul_distance(lat1,lon1,lat2,lon2)