import matplotlib.pyplot as plt
import seaborn as sns
sns.set_palette("Set2")
from wordcloud import WordCloud
from sklearn.metrics.pairwise import cosine_similarity

def get_feature_vector(song_name, year, dat, features_list):
    print(dat.head())
    dat_song = dat.query('name == @song_name and year == @year')
    song_repeated = 0
    if len(dat_song) == 0:
        raise Exception('The song does not exist in the dataset or the year is wrong! \
                        \n Use search function first if you are not sure.')
    if len(dat_song) > 1:
        song_repeated = dat_song.shape[0]
        print(f'Warning: Multiple ({song_repeated}) songs with the same name and artist, the first one is selected!')
        dat_song = dat_song.head(1)
    feature_vector = dat_song[features_list].values
    return feature_vector, song_repeated

def show_similar_songs(song_name, year, dat, features_list, top_n=10, plot_type='wordcloud'):

    feature_vector, song_repeated = get_feature_vector(song_name, year, dat, features_list)
    feature_for_recommendation = dat[features_list].values
    # calculate the cosine similarity
    similarities = cosine_similarity(feature_for_recommendation, feature_vector).flatten()
    if song_repeated == 0:
        related_song_indices = similarities.argsort()[-(top_n+1):][::-1][1:]
    else:
        related_song_indices = similarities.argsort()[-(top_n+1+song_repeated):][::-1][1+song_repeated:]
    similar_songs = dat.iloc[related_song_indices][['name', 'artists', 'year']]
    
    fig, ax = plt.subplots(figsize=(7, 5))
    if plot_type == 'wordcloud':
        similar_songs['name+year'] = similar_songs['name'] + ' (' + similar_songs['year'].astype(str) + ')'
        song_similarity = dict(zip(similar_songs['name+year'], similarities[related_song_indices]))
        song_similarity = sorted(song_similarity.items(), key=lambda x: x[1], reverse=True)
        wordcloud = WordCloud(width=1200, height=600, max_words=50, 
                            background_color='white', colormap='Set2').generate_from_frequencies(dict(song_similarity))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'{top_n} most recommended songs to: {song_name} ({year})', fontsize=16)
        plt.tight_layout(pad=0)
    
    elif plot_type == 'bar':
        similar_songs['name+year'] = similar_songs['name'] + ' (' + similar_songs['year'].astype(str) + ')'
        song_similarity = dict(zip(similar_songs['name+year'], similarities[related_song_indices]))
        song_similarity = sorted(song_similarity.items(), key=lambda x: x[1], reverse=True)
        plt.barh(range(len(song_similarity)), [val[1] for val in song_similarity], 
                 align='center', color=sns.color_palette('pastel', len(song_similarity)))
        plt.yticks(range(len(song_similarity)), [val[0] for val in song_similarity])
        plt.gca().invert_yaxis()
        plt.title(f'{top_n} most recommended songs to: {song_name} ({year})', fontsize=16)
        min_similarity = min(similarities[related_song_indices])
        max_similarity = max(similarities[related_song_indices])
        for i, v in enumerate([val[0] for val in song_similarity]):
            plt.text(min_similarity*0.955, i, v, color='black', fontsize=8)
        plt.xlim(min_similarity*0.95, max_similarity)
        plt.box(False)
        plt.tick_params(axis='both', which='both', bottom=False, top=False, labelbottom=False, left=False, right=False, labelleft=False)
        
    else:
        raise Exception('Plot type must be either wordcloud or bar!')
    
    return fig