# Train-Reservation-API
This repository contains the Flask API's.

# Description
This API is for Train Reservation System. The API exepects the Class of Travel and Number of Seats Required. 
Based on that input, it will return a response stating the seat numbers alloted. If there are not enough seats in the desired class, it will output the message accordingly. 
Then to change the class, enter the class name .

Please Note : For the purpose of this API, we have created only 2 classes viz. First Class and Second Class.

# Input Format ( Example )
{
   "cabinClass":"First Class",
   "seats_req": 30
}


# API Testing
Please use Postman to test the API's.
