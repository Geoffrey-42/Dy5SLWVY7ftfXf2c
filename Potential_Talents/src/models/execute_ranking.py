import os
cwd = os.getcwd()
dir_path = os.path.dirname(os.path.realpath(__file__))
runfile('src/models/model_ranking.py')

star_ind = [] # List of indices of starred candidates

def reset_starring():
    # Removes all of the stars
    star_ind = []
    return None

def star(ind):
    # Stars the candidate by providing its index ind in the dataframe
    star_ind.append(ind)
    job, loc = dataframe['job_title'][ind], dataframe['location'][ind]
    print('The candidate %s was starred with index %s'%((job, loc), ind))
    return None

def rank(keyword, location = None):
    print('\nThe keyword provided is: '+keyword)
    processed_starred = [processed_jobs[ind] for ind in star_ind]
    location, connec = None, None
    if len(star_ind) > 0:
        if location == None:
            location = processed_locations[star_ind[-1]]
        connec = processed_connections[star_ind[-1]]
    ranking = star_rank(keyword, star = processed_starred.copy(), location = location, connec = connec)
    print('\nRanking with fit probability:\n')
    for ranked in ranking:
        print(*zip(['index']+list(dataframe.columns), ranked))
    print('\nConsult the dataframe variable for the complete list\n')
    return ranking

reset_starring()

## Now providing the keywords
keywords = ['Aspiring human resources',  'seeking human resources']
keyword = keywords[1]

# Rank the candidates based on the keyword
ranking = rank(keyword)

# Star a candidate
star(26)

# Rank the candidates based on the keyword + starred candidate
ranking = rank(keyword)

# Star another candidate
# star(21)

# Re-rank based on the keyword + starred candidate
# (and learning from previously starred candidate(s))
# ranking = rank(keyword)

print('execute_ranking.py was run')
