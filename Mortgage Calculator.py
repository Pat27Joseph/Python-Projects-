import math 

def mortgage_calculator(principal, annual_rate, years, compounding_interval='monthly'):
    #Convert annual interest rate to a decimal
    rate = annual_rate / 100

    #Determine the number of compouding periods per year and the effective interest rate 
    if compounding_interval == 'monthly':
        n = 12
    elif compounding_interval == 'weekly':
        n = 52
    elif compounding_interval == 'daily':
        n = 52 
    elif compounding_interval == 'continouly':
        #For continous compounding, we use a different formula
        n = None 
    else:
        return "Invaild compouding interval. Choose from 'montly', 'weekly', 'daily', or 'continuously'."


    #Number of payments
    total_payments = years * 12 

    #Montly interest rate 
    if compounding_interval == 'continouly':
        # Continuous compouding monthly payment calculation
        monthly_payment = principal * (rate / 12 ) / (1 - math.exp(-rate / 12 * total_payments))
    else: 
        monthly_rate = rate / n
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**(n * years)) / ((1 + monthly_rate)**(n * years) - 1)

        # Total amount paid over the term 
        total_paid = monthly_payment * total_payments
         
        # Output the results
        return {
            'monthly_payment': round(monthly_payment, 2),
            'total_paid': round(total_paid),
            'years': years,
            'compounding_interval': compounding_interval.capitalize()
        } 

# Example usage 
principal = float(input("Enter the loan pricipal amount: "))
annual_rate = float(input("Enter the annual interest rate(as a percentage): "))
years = int(input("Enter the term of the loan(in years): "))
compounding_interval = input("Enter the compounding interval(monthly , weekly, daily, )")

result = mortgage_calculator(principal, annual_rate, years, compounding_interval)
print(f"Monthly Payment: ${result['monthly_payment']}")
print(f"Total Paid Over {result['years']} Years: ${result['total_paid']}")
print(f"Compouding Interval: {result['compounding_interval']}")