from flask import Flask, render_template, url_for, flash, redirect, request
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle
from flask import Flask, request, jsonify
label_encoder = LabelEncoder()
df=pd.read_csv("C:\\Users\\neeli\\Downloads\\Restaurant_Reservation-main\\Restaurant_Reservation-main\\food1.csv")
df['cuisine_encoded'] = label_encoder.fit_transform(df['cuisines'])
df['locality_encoded'] = label_encoder.fit_transform(df['locality'])
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df['average_cost_for_one'] = scaler.fit_transform(df[['average_cost_for_one']])
X = df[['cuisine_encoded', 'average_cost_for_one', 'locality_encoded']]
knn = NearestNeighbors(n_neighbors=5)
knn.fit(X)
input_data = [[57,  0.418182, 12]]
distances, indices = knn.kneighbors(input_data)
recommended_restaurants = df.iloc[indices[0]]
print(recommended_restaurants)

#model = pickle.load(open(r"C:\Users\Sanpa Solutions\Downloads\Restaurant-Recommendation-System-main\knn_model.pkl", 'rb'))


app = Flask(__name__)
#import pandas as pd
@app.route('/first')
def first_page():
    return render_template('first_page.html')
lko_rest = pd.read_csv("C:\\Users\\neeli\\Downloads\\Restaurant_Reservation-main\\Restaurant_Reservation-main\\food1.csv")

def fav(lko_rest1):
    lko_rest1 = lko_rest1.reset_index()
    from sklearn.feature_extraction.text import CountVectorizer

    count1 = CountVectorizer(stop_words='english')
    count_matrix = count1.fit_transform(lko_rest1['highlights'])
    from sklearn.metrics.pairwise import cosine_similarity

    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

    sim = list(enumerate(cosine_sim2[0]))
    sim = sorted(sim, key=lambda x: x[1], reverse=True)
    sim = sim[1:11]
    indi = [i[0] for i in sim]

    final = lko_rest1.copy().iloc[indi[0]]
    final = pd.DataFrame(final)
    final = final.T

    for i in range(1, len(indi)):
        final1 = lko_rest1.copy().iloc[indi[i]]
        final1 = pd.DataFrame(final1)
        final1 = final1.T
        final = pd.concat([final, final1])

    return final

def rest_rec(cost, people=2, min_cost=0, cuisine=[], Locality=[], fav_rest="", lko_rest=lko_rest):
    cost = cost + 200

    x = cost / people
    y = min_cost / people

    lko_rest1 = lko_rest.copy().loc[lko_rest['locality'] == Locality[0]]

    for i in range(1, len(Locality)):
        lko_rest2 = lko_rest.copy().loc[lko_rest['locality'] == Locality[i]]
        lko_rest1 = pd.concat([lko_rest1, lko_rest2])
        lko_rest1.drop_duplicates(subset='name', keep='last', inplace=True)

    lko_rest_locale = lko_rest1.copy()

    lko_rest_locale = lko_rest_locale.loc[lko_rest_locale['average_cost_for_one'] <= x]
    lko_rest_locale = lko_rest_locale.loc[lko_rest_locale['average_cost_for_one'] >= y]

    lko_rest_locale['Start'] = lko_rest_locale['cuisines'].str.find(cuisine[0])
    lko_rest_cui = lko_rest_locale.copy().loc[lko_rest_locale['Start'] >= 0]

    for i in range(1, len(cuisine)):
        lko_rest_locale['Start'] = lko_rest_locale['cuisines'].str.find(cuisine[i])
        lko_rest_cu = lko_rest_locale.copy().loc[lko_rest_locale['Start'] >= 0]
        lko_rest_cui = pd.concat([lko_rest_cui, lko_rest_cu])
        lko_rest_cui.drop_duplicates(subset='name', keep='last', inplace=True)

    if fav_rest != "":

        favr = lko_rest.loc[lko_rest['name'] == fav_rest].drop_duplicates()
        favr = pd.DataFrame(favr)
        lko_rest3 = pd.concat([favr, lko_rest_cui])
        lko_rest3.drop('Start', axis=1, inplace=True)
        rest_selected = fav(lko_rest3)
    else:
        lko_rest_cui = lko_rest_cui.sort_values('scope', ascending=False)
        rest_selected = lko_rest_cui.head(10)
    return rest_selected

def calc(max_Price, people, min_Price, cuisine, locality):
    rest_sugg = rest_rec(max_Price, people, min_Price, [cuisine], [locality])
    rest_list1 = rest_sugg.copy().loc[:,
                 ['name', 'address', 'locality', 'timings', 'aggregate_rating', 'url', 'cuisines']]
    rest_list = pd.DataFrame(rest_list1)
    rest_list = rest_list.reset_index()
    rest_list = rest_list.rename(columns={'index': 'res_id'})
    rest_list.drop('res_id', axis=1, inplace=True)
    rest_list = rest_list.T
    rest_list = rest_list
    ans = rest_list.to_dict()
    res = [value for value in ans.values()]
    return res

@app.route("/")
@app.route("/home", methods=['POST'])
def home():
    return render_template('home.html')


@app.route("/search", methods=['POST'])
def search():
    if request.method == 'POST':
        people = int(request.form['people'])
        min_Price = int(request.form['min_Price'])
        max_Price =int(request.form['max_Price'])
        cuisine1 = request.form['cuisine']
        locality1 = request.form['locality']
        res = calc(max_Price, people, min_Price,cuisine1, locality1)
        return render_template('search.html', title='Search', restaurants=res)
        #return res
    else:
        return redirect(url_for('home'))

'''@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Extract user input from the request
    user_input = data['queryResult']['queryText']

    # Process user input with your ML model or other logic
    # You can use the `user_input` to get recommendations from your model

    # Prepare a response
    response = {
        "fulfillmentText": "Your response from the ML model goes here."
    }

    return jsonify(response)'''

if __name__ == '__main__':
    app.run(debug=True)
