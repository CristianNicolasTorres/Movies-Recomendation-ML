import pandas as pd
import ast
import numpy as np
#charge the original dataset
url='https://drive.google.com/file/d/1Rp7SNuoRnmdoQMa5LWXuK4i7W1ILblYb/view?usp=drive_link'
url = 'https://drive.google.com/uc?id=' + url.split('/')[-2] 
df=pd.read_csv(url)
# drop columns wich are not usefull
df_removed_columns = df[['video', 'imdb_id', 'adult', 'original_title', 'poster_path', 'homepage']].copy()
df_droped=df.drop(['video', 'imdb_id', 'adult', 'original_title', 'poster_path', 'homepage'], axis=1)

# this function takes the info in the column "belong_to_colection"
def extract_attribute(row, attribute):
    try:
        collection = ast.literal_eval(row)
        if isinstance(collection, dict):
            return collection.get(attribute, np.nan)
    except (SyntaxError, ValueError):
        pass
    return np.nan

df_droped['collection_id'] = df_droped['belongs_to_collection'].apply(lambda row: extract_attribute(row, 'id'))
df_droped['collection_name'] = df_droped['belongs_to_collection'].apply(lambda row: extract_attribute(row, 'name'))
df_droped['collection_poster_path'] = df_droped['belongs_to_collection'].apply(lambda row: extract_attribute(row, 'poster_path'))
df_droped['collection_backdrop_path'] = df_droped['belongs_to_collection'].apply(lambda row: extract_attribute(row, 'backdrop_path'))

# save the original colum before we drop, in case we need it later
df_removed_columns['belongs_to_collection'] = df_droped['belongs_to_collection']
df_droped.drop('belongs_to_collection', axis=1, inplace=True)

#this function extracts the genres
def extract_genres(row):
    try:
        genres_list = ast.literal_eval(row)
        genres = [genre['name'] for genre in genres_list]
        return genres
    except (SyntaxError, ValueError):
        return []

df_droped['genres_extracted'] = df_droped['genres'].apply(extract_genres)

# save the column genres in a df with columns droped, and drop from the df we are working in
df_removed_columns['genres'] = df_droped['genres']
df_droped.drop('genres', axis=1, inplace=True)
df_removed_columns.head()

#now, i do the same with the colums production companies and production countries
def extract_info(row, key):
    try:
        data_list = ast.literal_eval(row)
        if isinstance(data_list, list):
            data = [item[key] for item in data_list]
            return data
        else:
            return []
    except (SyntaxError, ValueError):
        return []

df_droped['production_companies_extracted'] = df_droped['production_companies'].apply(lambda row: extract_info(row, 'name'))
df_droped['production_countries_extracted'] = df_droped['production_countries'].apply(lambda row: extract_info(row, 'name'))

#save and drop the colum original prodction_companies and production_countries
df_removed_columns['production_companies'] = df_droped['production_companies']
df_droped.drop('production_companies', axis=1, inplace=True)

df_removed_columns['production_countries'] = df_droped['production_countries']
df_droped.drop('production_countries', axis=1, inplace=True)

#this function extracts the languages
def extract_languages(row):
    try:
        languages_list=ast.literal_eval(row)
        if isinstance(languages_list,list):
            language=[language['name'] for language in languages_list]
            return language
        else:
            return[]
    except(SyntaxError,ValueError):
        return[]

df_droped['languages_extracted']=df_droped['spoken_languages'].apply(extract_languages)

#save and drop the original column spoken_languages
df_removed_columns['spoken_languages'] = df_droped['spoken_languages']
df_droped.drop('spoken_languages', axis=1, inplace=True)

#save drop some colums from bellongs_to that we consider are not usefull
df_removed_columns[['collection_poster_path', 'collection_backdrop_path']] = df_droped[['collection_poster_path', 'collection_backdrop_path']].copy()
df_droped = df_droped.drop(['collection_poster_path', 'collection_backdrop_path'], axis=1)

#fill the nulls values with 0(cero) in revenue and budget colums
df_droped[['revenue', 'budget']] = df_droped[['revenue', 'budget']].fillna(0)

#drop the nulls values from the coolum release_date
df_unested = df_droped.dropna(subset=['release_date'])

# Convert the 'release_date' column to datetime format, handling errors and invalid values
df_unested['release_date'] = pd.to_datetime(df_unested['release_date'], errors='coerce')

# Drop rows with invalid datetime values
df_unested = df_unested.dropna(subset=['release_date'])

# Extract the year and assign it to a new column 'release_year'
df_unested['release_year'] = df_unested['release_date'].dt.year

# Convert the 'revenue' and 'budget' columns to numeric type
df_unested['revenue'] = pd.to_numeric(df_unested['revenue'], errors='coerce')
df_unested['budget'] = pd.to_numeric(df_unested['budget'], errors='coerce')

# Fill the null values in 'revenue' and 'budget' with 0
df_unested['revenue'].fillna(0, inplace=True)
df_unested['budget'].fillna(0, inplace=True)

# Calculate the return on investment (return) as revenue / budget
df_unested['return'] = df_unested['revenue'] / df_unested['budget']

# Replace infinite or indeterminate values with 0
df_unested['return'].replace([float('inf'), float('-inf'), float('nan')], 0, inplace=True)

df_unested.drop_duplicates(subset="id", inplace=True)


#save the df unested in a new csv
df_unested.to_csv('Data\movies_dataset_ETLready.csv', index=False)