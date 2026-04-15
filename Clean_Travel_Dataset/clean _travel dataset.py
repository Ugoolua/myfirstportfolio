import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#load dataset
ctd = pd.read_csv(r"C:\Users\LENOVO\Downloads\clean_travel_agency_dataset.csv")
print(ctd)
print((ctd[ctd["Satisfaction_Level"] =="Very Dissatisfied"]["Package_Type"].value_counts()/ctd["Package_Type"].value_counts()*100).idxmax())
# To duplicate dataset
ctd_original = ctd.copy()
print(f"original dataset: {ctd.shape[0]} rows,{ctd.shape[1]} columns")
ctd.head()
print(ctd.head())
ctd.describe()
print(ctd.describe())
#PROBLEMS WITH THE DS#
# Missing values#
#For numbers , fill with average#
ctd["Age"] =ctd["Age"]. fillna(ctd["Age"].mean())
ctd["Amount_Spent_USD"] = ctd["Amount_Spent_USD"].fillna(ctd["Amount_Spent_USD"].median())
#For categories, fill with most common value
ctd["Gender"] = ctd["Gender"].fillna(ctd["Gender"].mode()[0])
ctd["Satisfaction_Level"] = ctd["Satisfaction_Level"].fillna("Neutral")
print(f"After missing values:{ctd.shape[0]} rows")
#Remove Duplicates#
Before = len(ctd)
ctd = ctd.drop_duplicates()
print(f"Removed {Before - len(ctd)} exact duplicate rows")
# 1. What Age group has the highest dissatisfaction rate?
def categorize_Age(Age):
    if Age < 18:
        return "Under 18"
    elif Age < 30:
        return "18-29"
    elif Age < 50:
        return "30-49"
    elif Age < 65:
        return "50-64"
    else:
        return "65+"
ctd["Age_Group"] = ctd["Age"].apply(categorize_Age)
ctd["Is_Dissatisfied"] = ctd["Satisfaction_Level"].isin(["Dissatisfied","Very Dissatisfied"])
dissatisfaction_rates = ctd.groupby("Age_Group")["Is_Dissatisfied"].mean()*100
highest_group = dissatisfaction_rates.idxmax()
highest_rate = dissatisfaction_rates.max()
print("===Dissatisfaction_rates by Age Group===")
print(dissatisfaction_rates.sort_values(ascending=False).round(1))
print(f"\n Highest dissatisfaction:{highest_group} ({highest_rate:.1f}%)")
print("===Dissatisfaction_rates by Age Group===")
#2 Are there destination preferred by specific genders or Age group.
gender_destination = pd.crosstab(ctd["Gender"],ctd["Destination"],normalize="index")*100
print("===Top Destinations by Gender===")
print("(Shows % of each gender that  visits each destination)")
print(gender_destination.round(1))
print()
print("=== Top 5 Destinations for each gender ===")
for gender in ctd["Gender"].unique():
    top_destinations = ctd[ctd["Gender"]== gender]["Destination"].value_counts().head(3)
    print(f"\n{gender}:")
    print(top_destinations)
    print()
#Are returning customers more likely to leave high or low rating.
customer_counts = ctd["Customer_Name"].value_counts()
ctd["Is_Returning"] = ctd["Customer_Name"]. map(customer_counts)>1
new_avg = ctd[ctd["Is_Returning"]] ["Review_Rating"].mean()
returning_avg = ctd[ctd["Is_Returning"]] ["Review_Rating"].mean()
print("="*50)
print("RETURNING VS NEW CUSTOMER RATINGS")
print("="*50)
print(f"New customers average rating:{new_avg:.2f}")
print(f"Returning customers average rating:{returning_avg:.2f}")
print()
if returning_avg > new_avg:
    print(f"YES! Returning customers give HIGHER ratings (+{returning_avg - new_avg:.2f} star)")
elif returning_avg < new_avg:
    print(f'NO! Returning customers give LOWER ratings({returning_avg - new_avg:.2f} star)')
else:
    print('No difference between new and returning customers')
#4. Which customer is the most frequent and does their ratings or satisfaction affect bookings?
customer_counts = ctd["Customer_Name"].value_counts()
most_frequent = customer_counts.index[0]
frequent = customer_counts.iloc[0]
print("="*20)
print("MOST FREQUENT CUSTOMERS")
print("="*20)
print(f"Customer:{most_frequent}")
print(f"Number of bookings:{frequent}")
print()
customer_data = ctd[ctd["Customer_Name"]==most_frequent]
print("THEIR BOOKING HISTORY:")
print(customer_data[["Booking_ID","Destination","Review_Rating","Satisfaction_Level","Amount_Spent_USD"]])
#5.Which package type has highest 'Very Dissatisfied' responses?
print((ctd[ctd["Satisfaction_Level"]=="Very Dissatisfied"]["Package_Type"].value_counts()/ctd["Package_Type"].value_counts()*100).idxmax())
ctd.to_csv('travel_data.csv', index=False)
ctd.copy()






