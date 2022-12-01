main_cat = pd.read_parquet('main_cat.parquet.gzip')
engine = create_engine('mysql+pymysql://root:projectyelp2022@34.176.218.33/projectyelp')
user_review = pd.read_sql(
    "select id_business, stars from reviews where id_user = 200;",
    con=engine, index_col='id_business'
)
user_preferences = pd.merge(user_review, main_cat, left_index=True, right_index=True )
user_stars = user_preferences['stars'].copy()
user_preferences.drop(columns='stars', inplace=True)
user_stars.shape, user_preferences.transpose().shape
user_perfil = user_preferences.transpose().dot(user_stars)
recomendacion = (main_cat * user_perfil).sum(axis=1)/(user_perfil.sum())
recomendacion = recomendacion.sort_values(ascending=False)
recom_final = df_business.loc[df_business['business_id'].isin(recomendacion.keys())]
recom_final[recom_final['is_open']==1].sort_values('review_count', ascending=False)