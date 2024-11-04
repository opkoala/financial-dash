# Citation for the usage of creating a response
# Date Nov/01/2024
# Adapted From
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition 
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type

#Citatiton for the usage of converting HTML to PDF
#Date Nov/03/2024
#Adapted From
#https://www.askpython.com/python-modules/pdfkit-module

from flask import Flask, render_template, request, make_response
import pdfkit
import yfinance as yf

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate_income_statement", methods=["GET", "POST"])
def generate_income_statement():
    if request.method == "POST":
        # Get data from the form
        company_name = request.form.get("company", "Company") 
        month_ended = request.form.get("month_ended", "Month Ended")

        # Retrieve all values for the form
        revenue_names = request.form.getlist('revenues[]')
        revenue_amounts = request.form.getlist('revenue_amounts[]')
        expenses_names = request.form.getlist('expenses[]')
        expenses_amounts = request.form.getlist('expense_amounts[]')

        # Prepare data for the income statement
        revenues = [] 
        total_revenues = 0  
        for i in range(len(revenue_names)):
            revenue_amount = float(revenue_amounts[i]) 
            revenues.append((revenue_names[i], revenue_amount)) 
            total_revenues += revenue_amount  

        expenses = []  
        total_expenses = 0  
        for i in range(len(expenses_names)):
            expense_amount = float(expenses_amounts[i]) 
            expenses.append((expenses_names[i], expense_amount))  
            total_expenses += expense_amount 

        # Calculate net income
        net_income = total_revenues - total_expenses
        net_income = round(net_income,1)
    

        # Pass the variables to the template to generate the income statement
        return render_template("income_statement.html", 
                               company_name=company_name, 
                               month_ended=month_ended, 
                               revenues=revenues, 
                               total_revenues=total_revenues, 
                               expenses=expenses, 
                               total_expenses=total_expenses, 
                               net_income=net_income)

    return render_template("generate_income_statement.html")

@app.route("/generate_ticker", methods=["GET", "POST"])
def generate_ticker():
    if request.method == "POST":
        query = request.form.get("query")
        if not query:
            return render_template("generate_ticker.html")

        stock = yf.Ticker(query)
        stocks = stock.income_stmt

        # Check if stocks is empty and render the appropriate template
        if stocks.empty:
            return render_template("generate_ticker.html", error="No Ticker Found.")

        # Render the ticker data to the HTML template
        return render_template("ticker.html", query=query, ticker=stocks)

    return render_template("generate_ticker.html")




@app.route("/export_income_statement_pdf", methods=["POST"])
def export_income_statement_pdf():
    # Retrieve all values for the form
    company_name = request.form['company']  
    month_ended = request.form['month_ended']
    revenue_names = request.form.getlist('revenues[]')  
    revenue_amounts = request.form.getlist('revenue_amounts[]')
    expenses_names = request.form.getlist('expenses[]')
    expenses_amounts = request.form.getlist('expense_amounts[]')

    # Prepare data for the income statement
    revenues = [] 
    total_revenues = 0  
    for i in range(len(revenue_names)):
        revenue_amount = float(revenue_amounts[i])  
        revenues.append((revenue_names[i], revenue_amount)) 
        total_revenues += revenue_amount  

    expenses = []  
    total_expenses = 0  
    for i in range(len(expenses_names)):
        expense_amount = float(expenses_amounts[i])  
        expenses.append((expenses_names[i], expense_amount))  
        total_expenses += expense_amount  

    # Calculate net income
    net_income = total_revenues - total_expenses

    # Generate PDF from HTML
    pdfkit_config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    html_items = render_template("income_statement.html", 
                                   company_name= company_name,
                                   month_ended=month_ended,
                                   revenues=revenues,
                                   total_revenues=total_revenues,
                                   expenses=expenses,
                                   total_expenses=total_expenses,
                                   net_income=net_income)

    #Convert html to pdf
    pdf = pdfkit.from_string(html_items, False, configuration=pdfkit_config)

    # Create response with PDF
    response = make_response(pdf)
    response.headers["content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=income_statement.pdf"
    return response


if __name__ == "__main__":
    app.run()