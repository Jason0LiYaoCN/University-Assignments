# # PART A: House Hunting
# annual_salary = int(input("Enter your annual salary: "))
# portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
# total_cost = int(input("Enter the cost of your dream home: "))

# current_savings = 0
# r = 0.04
# portion_down_payment = 0.25 * total_cost
# monthly_salary = annual_salary / 12
# total_month = 0

# while current_savings < portion_down_payment :
#     current_savings = current_savings + monthly_salary * portion_saved + current_savings * r / 12
#     total_month = total_month + 1

# print("Number of months: %d" % total_month)

# # PartB: Saving, with a raise
# annual_salary = int(input("Enter your annual salary: "))
# portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
# total_cost = int(input("Enter the cost of your dream home: "))
# semi_annual_raise = float(input("Enter the semi­annual raise, as a decimal: "))

# current_savings = 0
# r = 0.04
# portion_down_payment = 0.25 * total_cost
# monthly_salary = annual_salary / 12
# total_month = 0

# while current_savings < portion_down_payment :
#     current_savings = current_savings + monthly_salary * portion_saved + current_savings * r / 12
#     total_month = total_month + 1
#     if total_month % 6 == 0:
#         monthly_salary = monthly_salary * (1 + semi_annual_raise)

# print("Number of months: %d" % total_month)

# PartC: Finding the right amount to save away
annual_salary = int(input("Enter the starting salary: "))

total_cost = 1000000
semi_annual_raise = .07

r = 0.04
portion_down_payment = 0.25 * total_cost
high_bond = 10000
low_bond = 0
Steps = 0
current_savings = 0
find_solution = True

while abs(current_savings - portion_down_payment) > 100:
    Best_saving_rate = (high_bond + low_bond) / 20000
    current_savings = 0
    monthly_salary = annual_salary / 12
    for count in range(36):
        current_savings = current_savings + monthly_salary * Best_saving_rate  + current_savings * r / 12
        if (count + 1) % 6 == 0:
            monthly_salary = monthly_salary * (1 + semi_annual_raise)
    if current_savings - portion_down_payment > 100:
        high_bond = Best_saving_rate * 10000
    if portion_down_payment -current_savings > 100:
        low_bond = Best_saving_rate * 10000
    Steps = Steps + 1
    if (1.0 - Best_saving_rate) < (1 / 10000):
        find_solution = False
        break
    
if find_solution:
    print("Best savings rate: %f" % Best_saving_rate)
    print("Steps in bisection search: %d" % Steps)
else:
    print("It is not possible to pay the down payment in three years.")
