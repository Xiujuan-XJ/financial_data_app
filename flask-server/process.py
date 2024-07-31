import pandas as pd

df=pd.read_csv('uploads/5_years_financial_data.csv',parse_dates = ['Date'],dayfirst=True)

df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

df1=df.groupby('Category',as_index=False).agg({'Amount':'sum'}).rename(columns={'Category':'category','Amount':'amount'}).to_dict(orient='dict')

# Calculate total expenses by category
category_totals = df.groupby('Category',as_index=False).agg({'Amount':'sum'}).to_dict(orient='dict')

df['category_yearly'] = df['Category']+' '+df['Year'].astype(str)
yearly_expenses_per_category=df.groupby(['category_yearly'],as_index=False).agg({'Amount':'sum'}).to_dict(orient='dict')    


# Calculate Monthly expenses
df['year_month'] = df['Year'].astype(str)+'-'+df['Month'].astype(str)
monthly_expenses = df.groupby(['year_month'],as_index=False).agg({'Amount':'sum'}).rename(columns={"year_month": "category", "Amount": "amount"}).to_dict(orient='dict')

# Calculate yearly expenses
yearly_expenses = df.groupby(['Year'],as_index=False).agg({'Amount':'sum'}).to_dict(orient='dict')  