import os
cwd = os.getcwd()
dir_path = os.path.dirname(os.path.realpath(__file__))
runfile('src/data/make_dataset.py')

# All the job titles, locations and number of connections will be 
# pre-processed before encoding
jobs = list(dataframe['job_title'])
locations = list(dataframe['location'])
connections = list(dataframe['connection'])
processed_jobs = []
processed_locations = []
processed_connections = np.zeros(len(connections))

def process_string(txt):
    '''
    Process the words in an input string:
        - Tokenizes the words in the string
        - Removes stopwords, numbers and punctuation
        - Performs stemming
    
    Arguments:
        txt: String, for example "human resources"
    
    Returns:
        processed: String, for example "human resourc"
    '''
    words = [] # Will contain the words in the txt string
    stemmer = PorterStemmer()
    stopwords_english = stopwords.words('english')
    
    # Next, tokenize the words
    tokens = word_tokenize(txt)
    tokens = [i.strip().lower() for i in tokens]
    #

    # Remove stop words & punctuations from the list and stems
    for word in tokens:
        if word == 'hr':
            words.append('human'); words.append('resourc')
        elif (word not in stopwords_english and  # remove stopwords
                word not in string.punctuation and
                    len(word) > 1 and word.isalpha()):  # remove punctuation
                stem_word = stemmer.stem(word)  # stemming word
                words.append(stem_word)
    
    processed = ' '.join(words)
    return processed

## Generate the processed inputs
for job in jobs:
    processed_jobs.append(process_string(job))
for loc in locations:
    processed_locations.append(process_string(loc))
for i, con in enumerate(connections):
    if con.strip() == '500+':
        processed_connections[i] = 1
    elif con.strip() == '0':
        processed_connections[i] = 0
    else:
        processed_connections[i] = np.log(int(con))/np.log(500)

processed = dict( [ (i, (processed_jobs[i], processed_locations[i], processed_connections[i], 0) ) for i in range(len(connections)) ] )
processed_data = pd.DataFrame.from_dict(processed, orient = 'index', columns = ['job_title', 'location', 'log_connections', 'fit'])
## Now all the data has been pre-processed

## Defining the embedding model
model_name = 'sentence-transformers/all-mpnet-base-v2'
model_name = 'all-MiniLM-L6-v2' # smaller model
model = SentenceTransformer(model_name)

def job_embedding(job):
    '''
    Returns a previously saved value of the job embedding, or encodes it
    
    Arguments:
        job: String, processed job information
    
    Returns:
        encoding: Array, the encoding of the job
    '''
    ind = dict(enumerate(np.where(processed_data['job_title'] == job)[0])).get(0)
    if encoded and ind != None:
        return encoded_data['job_title'].loc[ind]
    ind = dict(enumerate(np.where(processed_data['location'] == job)[0])).get(0)
    if encoded and ind != None:
        return encoded_data['location'].loc[ind]
    encoding = model.encode(job, normalize_embeddings = True)
    return encoding

def encode_jobs():
    '''
    Encodes all preprocessed jobs and locations.
    
    Returns:
        encoded_data: Pandas dataframe, candidates encoded data
    '''
    encoded_jobs = np.array([job_embedding(job) for job in processed_jobs])
    encoded_locations = np.array([job_embedding(loc) for loc in processed_locations])
    data = np.concatenate((encoded_jobs, encoded_locations))
    enc_samples = dict( [ (i, (data[i], data[i+len(processed_connections)], processed_connections[i], 0)) for i in range(len(connections)) ] )
    encoded_data = pd.DataFrame.from_dict(enc_samples, orient = 'index', columns = ['job_title', 'location', 'log_connections', 'fit'])
    return encoded_data

## Performs all the encoding
encoded = False
encoded_data = encode_jobs()
encoded = True # Now all the data has been encoded
encoded_example = encoded_data['job_title'][0]
job_titles = dataframe['job_title']

print('encode_features.py was run')



