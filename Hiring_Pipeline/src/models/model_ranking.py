import os
cwd = os.getcwd()
dir_path = os.path.dirname(os.path.realpath(__file__))
runfile('src/features/encode_features.py')

def cosine_similarity(vec1, vec2):
    # Returns the cosine similarity between vectors with norm == 1
    norm1 = np.linalg.norm(vec1); norm2 = np.linalg.norm(vec2)
    assert np.isclose(norm1,1); assert np.isclose(norm2,1)
    return np.dot(vec1, vec2)

def similar_jobs(job, location = None, connec = None, update = False):
    # Returns a list of jobs most similar to 'job' based on their ranking
    # If location is provided, it will be accounted for
    # If connec is provided, it will be accounted for
    # If update is set to True, dataframes will be sorted according to fitness
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
    for i, cos in enumerate(cosine_list):
        dataframe.loc[i, ['fit']] = cos
        processed_data.loc[i, ['fit']] = cos
        encoded_data.loc[i, ['fit']] = cos
    dataframe.sort_values(by=['fit'], ascending = False, inplace = True)
    processed_data.sort_values(by=['fit'], ascending = False, inplace = True)
    encoded_data.sort_values(by=['fit'], ascending = False, inplace = True)
    return None

def star_rank(keyword, star = [], location = None, connec = None, weights = [0.4, 0.5, 0.1]):
    # Returns a ranking based on keyword provided and starred candidates
    # star is the list of job_title starred (string, exact match) (in chronological order)
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



