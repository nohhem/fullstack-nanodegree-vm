from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi # to decipher the message that was sent from the server ##cgi common gateway interface library
import  urlparse
#################################
# import CRUD Operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
############################

class webserverHandler(BaseHTTPRequestHandler): ## extend from BaseHTTPRequestHandler class
    def do_GET(self):## handlers all get requests our web server recevies
        try:
            if self.path.endswith("/hello"):
                self.send_response(200) #send reponse code  200
                self.send_header('Content-type','text/html') # indicate replying with text in form of html to the client
                self.end_headers() ## sends a blank line indicating the end if our http headers in the response

                ## the content to send to the client
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?
                </h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output) ## use self.wfile.write fucn to send a message back to the client
                ##print output
                return ## to exit
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2>
                             <input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                ##print output
                return
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ## display restaurantts

                output=""
                output+="<html><body>"
                output+="<a href=/restaurants/new>Add a new Restaurant</a>"
                output+="<h2>Restauratns list</h2>"
                output+="<ul>"
                restaurants=session.query(Restaurant)
                for r in restaurants:
                    output+="<li>"+r.name+"</li>"
                    output+="<a href="+"/restaurants/"+str(r.id)+"/edit"+">Edit</a><br>"
                    output+="<a href="+"#"+">Delete</a><br><br>"

                output+="</ul></body></html>"

                self.wfile.write(output)
                #print output
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output=""
                output += "<html><body>"
                output+=''' <form method='POST' enctype='multipart/form-data' action="/restaurants/new">The new Restaurant Name:<br>
                            <input type="text" name="newRestaurantName" placeholder='New Resattaurant name'>
                            <input type='submit' value="Create">
                            </form>  '''
                output += "</html></body>"
                self.wfile.write(output)
                return
            elif self.path.endswith("edit"):



                restaurantId=self.path.split("/")[2]
                res=session.query(Restaurant).filter_by(id=restaurantId).one()
                if res!=[]:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output=""
                    output += "<html><body>"
                    output+=''' <form method='POST' enctype='multipart/form-data' action="/restaurants/'''+restaurantId+'/edit">'+res.name+'''<br>
                                <input type="text" name="newRestaurantName" placeholder='placeholder text'>
                                <input type='submit' value="Rename">
                                </form>'''
                    output += "</html></body>"

                    self.wfile.write(output)



        except IOError:
            self.send_error(404,"file not found %s" %self.path) ## to notify if there is an error

    def do_POST(self):


            if self.path.endswith("edit"):
                print self.path
                ctype,pdict=cgi.parse_header(self.headers.getheader('content-type'))
                restaurantId=self.path.split("/")[2]
                if(ctype=='multipart/form-data'):
                    ##get the fields from the webserverhandler that were filled in the form
                    fields=cgi.parse_multipart(self.rfile,pdict)
                    messagecontent=fields.get('newRestaurantName')
                    resNewName=messagecontent[0]
                    restaurant=session.query(Restaurant).filter_by(id=restaurantId).one()
                    restaurant.name=resNewName
                    session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return


            if self.path.endswith("/restaurants/new"):
                ctype,pdict=cgi.parse_header(self.headers.getheader('content-type'))
                if(ctype=='multipart/form-data'):

                    ##get the fields from the webserverhandler that were filled in the form
                    fields=cgi.parse_multipart(self.rfile,pdict)
                    messagecontent=fields.get('newRestaurantName')

                    #Create a new resaurant and insert it to the database
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

                    return
            if self.path.endswith("/hello"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))

                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                output = ""
                output += "<html><body>"
                output += " <h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2>
                <input name="message" type="text" >
                <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                ##print output



def main():
    try:
        port =8000
        server=HTTPServer(('',port), webserverHandler)
        print "web server running of port %s" %port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C enterd ,stopping web server"
        server.socket.close()

if __name__=='__main__':
    main()

