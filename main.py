import json
import os
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from pprint import pprint

class StateHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_POST(self):
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        self.send_header("Content-type", "text/html")
        self.send_response(200)
        self.end_headers()
        data = urlparse.parse_qs(self.data_string)
        service = GeoLocationService()
        res = service.check_point(float(data['longitude'][0]),float(data['latitude'][0]))
        self.wfile.write('{0}\n'.format(res))
        return

class GeoLocationService:

    def __init__(self):
        self.stateList = self.load_data()

    def load_data(self):
        with open("states.json") as file:
            return [json.loads(x.strip('\n')) for x in file.readlines()]

    def check_point(self,x,y):
        for state in self.stateList:
            if self.point_inside_polygon(x,y,state['border']):
                return state['state']

    def point_inside_polygon(self,x,y,poly):

        n = len(poly)
        inside =False

        p1x,p1y = poly[0]
        for i in range(n+1):
            p2x,p2y = poly[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside

def main():
    try:
        server = HTTPServer(('localhost', 8080), StateHandler)
        print('Started http server')
        server.serve_forever()
    except KeyboardInterrupt:
        pass
        server.socket.close()

    # x = -77.036133
    # y = 40.513799
    # service = GeoLocationService()
    # res = service.check_point(x, y)
    # print res


if __name__ == "__main__":
    main()