import os
cwd = os.getcwd()
dir_path = os.path.dirname(os.path.realpath(__file__))
runfile('src/features/encode_features.py')

def cosine_similarity(vec1, vec2):
    '''
    Returns the cosine similarity between unit vectors
    
    Arguments:
        vec1: Unit array
        vec2: Unit array
    
    Returns:
        The numpy dot product
    '''
    norm1 = np.linalg.norm(vec1); norm2 = np.linalg.norm(vec2)
    assert np.isclose(norm1,1); assert np.isclose(norm2,1)
    return np.dot(vec1, vec2)

def similar_jobs(job, location = None, connec = None, update = False):
    '''
    Returns a ranking of the candidates best matching a specific job
    
    Arguments: 
        job: String or embedding representing the job to match candidates to.
             If a string is provided, it will be encoded.
             
        location: String, a specified city or country
        
        connec: Integer, number of connections on Linkedin (Max 500)
        
        update: Boolean, if True dataframes will be sorted according to ranking
    
    Returns:
        ranking: List, a ranking of the 10 best matching candidates
    '''
    cosine_list = [] # Similarity ranking
    if type(job) == str:
        emb = job_embedding(job)
    else:
        emb = job # already encoded
    if location != None:
        emb += job_embedding(location) # account for location
    if connec != None:
        emb = np.concatenate((emb, [connec])) # account for connections
    emb = np.array(normalize([emb])[0])
    # Embedding of input job complete.
    ## Next, go through all possible candidates
    for i, tup in enumerate(zip(processed_jobs, processed_locations, processed_connections)):
        job_, loc_, con_= tup
        vec = job_embedding(job_) + (location!=None)*job_embedding(loc_)
        if connec != None:
            vec = np.concatenate((vec, [con_]))
        vec = np.array(normalize([vec])[0])
        cosine_list.append(cosine_similarity(emb, vec))
    if update:
        update_dataframe(cosine_list)
    ranking = [[dataframe.index[i]] + dataframe.values[:10].tolist()[i] for i in range(10)]
    return ranking

def update_dataframe(cosine_list):
    '''
    Updates candidates dataframe based on provided ranking information.
    
    Arguments:
        cosine_list: List, contains the job cosine similarity of each candidate
    
    Updates:
        The dataframes fit values are updated and sorted in descending order.
    '''
    for i, cos in enumerate(cosine_list):
        dataframe.loc[i, ['fit']] = cos
        processed_data.loc[i, ['fit']] = cos
        encoded_data.loc[i, ['fit']] = cos
    dataframe.sort_values(by=['fit'], ascending = False, inplace = True)
    processed_data.sort_values(by=['fit'], ascending = False, inplace = True)
    encoded_data.sort_values(by=['fit'], ascending = False, inplace = True)
    return None

def star_rank(keyword, star = [], location = None, connec = None, weights = [0.4, 0.5, 0.1]):
    '''
    Provides a candidate ranking based on job characteristics and manual 
    supervisory signal (history of starred candidates).
    
    Arguments:
        keyword: String, describes the job to match candidates to.
        star: List, indices of candidates starred in chronological order
        location: String, preferred location
        connec: Integer, number of Linkedin connections (Max 500)
        weights: List [a, b, c], importance accorded to (a+b+c=1): 
                    a: keyword provided
                        and manual supervisory signals:
                    b: last starred candidate
                    c: previously starred candidates
    
    Returns:
        ranking: List, ranking of candidates
    '''
    key_emb = job_embedding(process_string(keyword))
    key_w, star_w, prestar_w = weights # Importance accredited to keyword vs starred vs previously starred
    if len(star) > 0:
        star_emb = job_embedding(star.pop())
        if len(star) > 0:
            prestar_emb = np.average([job_embedding(s) for s in star], axis = 0)
            prestar_emb = np.squeeze(normalize(prestar_emb.reshape(1,-1), axis = 1))
            vec = key_w*key_emb + star_w*star_emb + prestar_w*prestar_emb
        else:
            vec = key_w*key_emb + star_w*star_emb
    else:
        vec = key_emb
    # Now the vector vec is an amalgation of the embeddings of the keyword + starred candidates
    vec = np.squeeze(normalize(vec.reshape(1,-1), axis = 1))
    ranking = similar_jobs(vec, location = location, connec = connec, update = True)
    return ranking

print('model_ranking.py was run')



