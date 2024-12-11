from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/microservice_c", methods=["POST"])
def generate_income_statement():
        '''Generate income Statement based on the values'''
        company_name = request.form.get("company", "Company")
        month_ended = request.form.get("month_ended", "Month Ended")

        revenue_names = request.form.getlist('revenues[]')
        revenue_amounts = request.form.getlist('revenue_amounts[]')
        expenses_names = request.form.getlist('expenses[]')
        expenses_amounts = request.form.getlist('expense_amounts[]')

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

        net_income = total_revenues - total_expenses


        return jsonify({
            'company_name': company_name,
            'month_ended': month_ended,
            'revenues': revenues,
            'total_revenues': total_revenues,
            'expenses': expenses,
            'total_expenses': total_expenses,
            'net_income': net_income
        })

if __name__ == "__main__":
    app.run(port=50012)  
