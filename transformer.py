import json
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import dateutil
from dateutil.parser import parse
#### Get Data and Create Dataframes ####

with open('/home/njhey/repos/pos-demo/data/baskets20200728103203.json') as f:
    data = json.load(f)
df_baskets = json_normalize(data, 'Baskets')
df_basket_items = json_normalize(data, "BasketItems")
df_products = json_normalize(data,"Products")
df_barcodes = json_normalize(data,"Barcodes")

#### End Data ####

#### Dataframe Cleanup ####
# Filter products with no id
df_products = df_products[df_products.ID.notnull()]

# Remove duplicates to master the product list (on PLU)
df_products = df_products.sort_values('PLU')
df_products = df_products.drop_duplicates(subset='PLU', keep='first')

# Remove basketitems without a PLU
df_basket_items = df_basket_items[df_basket_items.PLU.notnull()]

# Remove the barcode field from the basketitem
df_basket_items = df_basket_items.drop(columns=['Barcode'])

# Now join the products to barcodes
df_products = pd.merge(df_products, df_barcodes, how='left', left_on='ID', right_on="ProductID")

# Now join the basketitems to products
df_basket_items = pd.merge(df_basket_items,df_products, how='left', on="PLU")
#### End Dataframe Cleanup ####

dt = parse('2020-07-28T10:31:18')
print(dt)
print(dt.strftime('%d/%m/%Y'))
print(dt.strftime('%H:%M:%S'))

# Todo - loop through the baskets and change the date time and data formats to be numeric/date time
# Todo - do some test pushes to the thing
# Automate the rclone so it picks up the changes
# Run the script on a timer so that every couple of minutes it pushes any fresh data