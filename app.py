import pandas as pd
import numpy as np
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Load the CSV data
df = pd.read_csv('data.csv')

@app.route('/')
def index():
    # Convert to string and remove NaN values before sorting
    thanas = sorted(df['Thana'].astype(str).replace('nan', '').unique())
    districts = sorted(df['District'].astype(str).replace('nan', '').unique())
    regions = sorted(df['Region'].astype(str).replace('nan', '').unique())
    
    # Remove empty strings from the lists
    thanas = [x for x in thanas if x]
    districts = [x for x in districts if x]
    regions = [x for x in regions if x]
    
    return render_template('index.html', thanas=thanas, districts=districts, regions=regions)

@app.route('/search', methods=['POST'])
def search():
    agent_number = request.json['agent_number']
    agent_data = df[df['Agent Account Number'] == int(agent_number)]
    
    if agent_data.empty:
        return jsonify({'error': 'Agent not found'})
    
    return jsonify({
        'lat': agent_data['Pinned Latitude'].values[0],
        'lon': agent_data['Pinned Longitude'].values[0],
        'agent_info': agent_data.fillna('').to_dict('records')[0]
    })

@app.route('/filter', methods=['POST'])
def filter_agents():
    filters = request.json
    filtered_df = df.copy()
    
    if filters['thana']:
        filtered_df = filtered_df[filtered_df['Thana'].astype(str) == filters['thana']]
    if filters['district']:
        filtered_df = filtered_df[filtered_df['District'].astype(str) == filters['district']]
    if filters['region']:
        filtered_df = filtered_df[filtered_df['Region'].astype(str) == filters['region']]
    
    agents = filtered_df.fillna('').to_dict('records')
    return jsonify(agents)

if __name__ == '__main__':
    app.run(debug=True)