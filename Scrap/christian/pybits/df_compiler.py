import requests
import json

def df_compiler(initial_url, n):
    r = requests.get(initial_url)
    j = r.json()
    
    #open list to hold urls, append initial url
    urls = list() 
    urls.append(str(initial_url))

    #handling further urls  
    for x in range(n):        
        page_key = 'pagination'
        if page_key in j:
            pagination = j[page_key]
            try:
                if 'next_url' in pagination:
                    url_key = 'next_url'
                    next_url_key = j[page_key][url_key]
                    next_url = str(next_url_key)
                    try:
                        urls.append(url_key)
                        j = next_url
                    except (ValueError):
                        return 'Error: \'next_url\' data not found'
            except (ValueError):
                return 'Error: \'pagination\' data not found'
                
        
      
      #open list to hold data
    results = list()

      #populate df with data from urls in urls
    for url in urls:
        try:
            data = j['data']
            df_inst = json_normalize(data)
            results.append(df_inst)
        except Exception, e:
            return str(e)

      #initiate df
    df = pd.DataFrame().append(results).reset_index().drop('index',axis=1) #pd.DataFrame(results)
    
    return df