def see_comments_data(df):    
    if 'comments.data' in df and 'id' in df:
        try:
            comments_data = df[['comments.data', 'id']]
            comments_df = pd.DataFrame()
            for x in comments_data['comments.data']:
                if len(x) > 0:
                    all_comments_data = comments_df.append(json_normalize(x), ignore_index=True) #append to new df
            return all_comments_data
        except Exception, e:
            print 'Error:', str(e)