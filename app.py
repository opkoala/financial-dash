# Citation for the usage of creating a response
# Date Nov/01/2024
# Adapted From
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition 
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type


#Citation for using datetime library
#Date Nov/30/2024
#Adapted From
#https://www.geeksforgeeks.org/python-datetime-timedelta-function/


from flask import Flask, json, render_template, request, redirect, url_for, jsonify
import socket  
import requests


app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

#microservice a: schedule.py
HOST = '127.0.0.1'
PORT = 65432

def send_schedule_request(review_id, increment=None):
    """Send schedule to the server and receive the response."""
    request_data = {
        'id': review_id,
        'increment': increment,
    }

    # Establish a connection to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))

        # Send data to the server
        client_socket.sendall(json.dumps(request_data).encode())

        # Receive the server's response
        response = client_socket.recv(1024).decode()

        if not response:
            return "No response from server"

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return "Error decoding server response"

@app.route('/submit_review', methods=['POST'])
def schedule():
    """Handle the form submission and send the request to the server."""
    review_id = request.form.get('review_id')
    increment = request.form.get('increment', 60)  

    try:
        increment = int(increment)
    except ValueError:
        return jsonify({"error": "Increment must be a valid number."}), 400

  

    # Log the inputs
    app.logger.info(f"Review ID: {review_id}, Increment: {increment}")

    # Send the request to the socket server
    response = send_schedule_request(review_id, increment)


    return render_template(
        'schedule.html',
        review_id=review_id,
        increment=increment,

        response=response
    )


#microservice b: googlemap.py
GOOGLEMAP_URL = "http://localhost:50215/get_coordinates"

@app.route('/generate_map', methods=['GET', 'POST'])
def generate_map():
    """Handles the input for address and retrives the coordinates."""
    latitude = None
    longitude = None
    address = None

    if request.method == 'POST':
        query = request.form.get('map_query')
        if query:          
            # GET google map api
            response = requests.get(GOOGLEMAP_URL, params={'map_query': query})
            
            # Server has successfully processed the request and returned the requested data
            if response.status_code == 200:
                result = response.json()
                latitude = result['latitude']
                longitude = result['longitude']
                address = query
                print(f"Received coordinates: Latitude {latitude}, Longitude {longitude}")

    return render_template('generate_map.html', latitude=latitude, longitude=longitude, address=address)



#microservice c: income.py
Income_statement_URL = "http://localhost:50012/microservice_c"

@app.route("/generate_income_statement", methods=["GET", "POST"])
def generate_income_statement():
    '''Handles the inputs for generating an income statement '''
    if request.method == "POST":
        company_name = request.form.get("company", "Company")
        month_ended = request.form.get("month_ended", "Month Ended")

        revenue_names = request.form.getlist('revenues[]')
        revenue_amounts = request.form.getlist('revenue_amounts[]')
        expense_names = request.form.getlist('expenses[]')
        expense_amounts = request.form.getlist('expense_amounts[]')

       
        data_income = {
            "company": company_name,
            "month_ended": month_ended,
            "revenues[]": revenue_names,
            "revenue_amounts[]": revenue_amounts,
            "expenses[]": expense_names,
            "expense_amounts[]": expense_amounts
        }

        response = requests.post(Income_statement_URL, data=data_income)

        # Server has successfully processed the request 
        if response.status_code == 200:
            data = response.json()

            # Pass the data to the template
            return render_template("income_statement.html", 
                                   company_name=data['company_name'], 
                                   month_ended=data['month_ended'], 
                                   revenues=data['revenues'], 
                                   total_revenues=data['total_revenues'], 
                                   expenses=data['expenses'], 
                                   total_expenses=data['total_expenses'], 
                                   net_income=data['net_income'])

    return render_template("generate_income_statement.html")

#microservice d: ticker.py
Polygon_URL = "http://localhost:50018//microservice_d"


@app.route('/generate_ticker', methods=['GET', 'POST'])
def generate_ticker():
    '''Handles the inputs for generating a ticker '''
    if request.method == 'POST':
        ticker = request.form.get('rev_query')  
        
        if ticker:
            # Call the Polygon API 
            response = requests.get(Polygon_URL, params={'ticker': ticker})
            
            # Server has successfully processed the request and returned the requested data
            if response.status_code == 200:
                income_statement = response.json()
                return render_template('ticker.html', rev_query=ticker, income_statement=income_statement)
            else:
                error_message = response.json().get('error', 'Unknown error')
                return render_template('generate_ticker.html', error=error_message)
        else:
            return render_template('generate_ticker.html', error="Ticker is required.")
    else:
        return render_template('generate_ticker.html', error=None)

if __name__ == "__main__":

    app.run()
