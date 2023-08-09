from flask import Flask, jsonify,request
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restful import Api,Resource
import uuid


app = Flask(__name__)

app.app_context().push()

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/openapi.yaml'  # Our API url (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Train Reservation API"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)

api = Api(app)


available_seats = {"First Class":["A" + str(i) for i in range(1,91)],
             "Second Class":["B" + str(i) for i in range(1,91)]}
              
                     
occupied_seats = {}

class Reservation(Resource):
    

    totalseats = 180
    
    def post(self):
        seat_no_list = []
        data = request.get_json()
        cabinClass = data["cabinClass"]
        seats_req = data["seats_req"]
        # if cabinClass != "First Class" or cabinClass != "Second Class":
        #     return {"error":"Class not available. Please choose a class among First Class or Second Class"},401
        if seats_req <= Reservation.totalseats:
            
            for seat_no in range(seats_req):
                
                if cabinClass == "First Class":
                    seats_required = available_seats[cabinClass][:seats_req]
                    pnr = uuid.uuid4()
                    for seat in seats_required:
                        if seat in occupied_seats.keys():
                            available = get_seats(seat,cabinClass)
                            
                            occupied_seats[seat] = pnr
                            seats_to_be_alloted = available_seats[cabinClass][:seats_req]  
                            if seat in available:
                                seats_to_be_alloted = available_seats[:seats_req]
                                
                        else:
                            occupied_seats[seat] = str(pnr)
                            seats_to_be_alloted = available_seats[cabinClass][:seats_req]
                            break 
                    
                if cabinClass == "Second Class":
                    seats_required = available_seats[cabinClass][:seats_req]
                    pnr = uuid.uuid4()
                    for seat in seats_required:
                        if seat in occupied_seats.keys():
                            available = get_seats(seat,cabinClass)
                            
                            occupied_seats[seat] = str(pnr)
                            if seat in available:
                                seats_to_be_alloted = available_seats[:seats_req]  
                                
                             
                        else:
                            occupied_seats[seat] = str(pnr)
                            seats_to_be_alloted = available_seats[cabinClass][:seats_req]
                            break 
                 
                booking = True    
                
                # Reservation.totalseats -= seats_req
                seats_required = Reservation.totalseats - seats_req
                
                try:
                    seat_no_list.append(available_seats[cabinClass][seats_req])
                except:
                    return {"error":"Required Seats Not Available in this Class"},400
                    
                    
            if booking:
                booking_id = uuid.uuid4()
                booking_id = str(booking_id)
                seat_numbers = ','.join(seat_no_list)
                booking = False
                    
                
                return{"Cabin Class":cabinClass, "Seat Numbers":seat_numbers ,"BookingID":str(pnr),"Payment link":"http://www.payhere.com"},201
                
        else:

            return {"message":"Sorry the required number of seats are not available"},404
        
        return

    def get(self):
        return {"msg":"This is a get request"},201






# Endpoints
api.add_resource(Reservation,'/api/book/')



if __name__ == "__main__":
    app.run()