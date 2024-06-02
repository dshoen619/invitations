from os import environ, path
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import os
from dotenv import load_dotenv
from airtable import Airtable
import traceback

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join('./', basedir, ".env"))

# Replace with your Airtable API key, Base ID, and Table Name
api_key =       os.getenv('AIRTABLE_API_KEY')
base_id =       os.getenv('AIRTABLE_BASE_ID')
table_name =    os.getenv('AIRTABLE_TABLE_NAME')

# heroku env
# api_key =       os.environ['API_KEY']
# base_id =       os.environ['BASE_ID']
# table_name =    os.environ['TABLE_NAME']

# Initialize airtable
airtable = Airtable(base_id, table_name,api_key)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://linoy-and-david-wedding-c7ed9164a9b9.herokuapp.com/"}})  # Enable CORS for React frontend
app.config['CORS_HEADERS'] = 'Content-Type'


# app.register_blueprint(main)


@app.route('/<id>', methods=['GET'])
@cross_origin()
def home(id):
    print(id)
    record =  airtable.get(record_id=id)
    print(record)
    return jsonify(record)

@app.route('/rsvp', methods = ['POST'])
@cross_origin()
def rsvp():
    data:dict[dict[str,str]] =      request.json
    record_id:str =                 data.get('record_id')
    comingCount:int =               data.get('comingCount')

    update_fields ={
        'responded':'1',
        'amount_coming':f'{comingCount}',
    }
    try:
        response = airtable.update(record_id, update_fields)
        return jsonify({'status': 'success', 'data': response}), 200
    except:
        print(traceback.print_exc())
        return '404'
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)