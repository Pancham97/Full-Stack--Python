from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import cgi

from database_setup import Base, Restaurant, MenuItem
engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a new restaurant</h1>"
                output += "<form method=POST enctype='multipart/form-data' action='/restaurant/new'>"
                output += "<input type='text' name='newRestaurant' placeholder='Name of new restro'>"
                output += "<input type='submit' value='Create'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurant/%s/edit' >" % restaurantIDPath
                    output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurant/%s/delete' >" % restaurantIDPath
                    output += "Delete %s?" % myRestaurantQuery.name
                    output += "<input type = 'submit' value = 'Delete'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)

            if self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""

                output += "<html><body>"
                output += "<h2><a href='restaurant/new'>Make a new restaurant</a></h2><br/><br/>"
                restaurantName = session.query(Restaurant).all()
                for restros in restaurantName:
                    output += "<h2> %s </h2>" %restros.name
                    output += "\n"
                    output += "<a href='/restaurant/%s/edit'>Edit</a> " % restros.id
                    output += "\n"
                    output += "<a href='/restaurant/%s/delete'>Delete</a> " % restros.id
                    output += "\n"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, "File not found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                    ctype, pdict = cgi.parse_header(
                        self.headers.getheader('content-type'))
                    if ctype == 'multipart/form-data':
                        fields = cgi.parse_multipart(self.rfile, pdict)
                        restaurantIDPath = self.path.split("/")[2]

                        myRestaurantQuery = session.query(Restaurant).filter_by(
                            id=restaurantIDPath).one()
                        if myRestaurantQuery != []:
                            session.delete(myRestaurantQuery)
                            session.commit()
                            self.send_response(301)
                            self.send_header('Content-type', 'text/html')
                            self.send_header('Location', '/restaurant')
                            self.end_headers()

            if self.path.endswith("/edit"):
                    ctype, pdict = cgi.parse_header(
                        self.headers.getheader('content-type'))
                    if ctype == 'multipart/form-data':
                        fields = cgi.parse_multipart(self.rfile, pdict)
                        messagecontent = fields.get('newRestaurantName')
                        restaurantIDPath = self.path.split("/")[2]

                        myRestaurantQuery = session.query(Restaurant).filter_by(
                            id=restaurantIDPath).one()
                        if myRestaurantQuery != []:
                            myRestaurantQuery.name = messagecontent[0]
                            session.add(myRestaurantQuery)
                            session.commit()
                            self.send_response(301)
                            self.send_header('Content-type', 'text/html')
                            self.send_header('Location', '/restaurant')
                            self.end_headers()

            if self.path.endswith("/restaurant/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurant')

                newRestaurant = Restaurant(name = messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurant')
                self.end_headers()

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Your web server is running on %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C pressed. Stopping the server..."
        server.socket.close()

if __name__ == '__main__':
    main()
