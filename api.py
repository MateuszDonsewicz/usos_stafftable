# ssh -p 5739 impan@s55.smarthost.pl #https://impan.smarthost.pl/
# Impan2024$
import os
from flask import Flask, request, render_template
from requests_oauthlib import OAuth1Session

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Your credentials
consumer_key = '82xwD377tKqEjGm8fCDj'
consumer_secret = 'DvtbWdfBdryLkCLCcQrPdLC9zbDPGgmfpz5u6Wch'

@app.route('/')
def home():
    return 'Welcome to the USOS API Staff Index'

@app.route('/staff')
def staff_index():
    # API URL for staff search
    search_api_url = 'https://usosapps.impan.pl/services/users/search2'
    search_params = {
        'lang': 'en',
        'fields': 'items|next_page',
        'query': request.args.get('query', ''),
        'among': 'current_staff',
        'num': 20,
        'start': 0,
        'format': 'json'
    }

    # OAuth1Session with only consumer key and secret
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret
    )

    # Sending request to API for staff search
    search_response = oauth.get(search_api_url, params=search_params)
    search_results = search_response.json()

    staff_data = []
    if 'items' in search_results:
        for staff_member in search_results['items']:
            user_id = staff_member['user']['id']
            # API URL for user details
            user_api_url = 'https://usosapps.impan.pl/services/users/user'
            user_params = {
                'user_id': user_id,
                'fields': 'email|phone_numbers|mobile_numbers',
                'format': 'json'
            }
            # Sending request to API for user details
            user_response = oauth.get(user_api_url, params=user_params)
            user_details = user_response.json()

            # Add user details to staff data
            staff_member['email'] = user_details.get('email', '')
            staff_member['phone_numbers'] = user_details.get('phone_numbers', [])
            staff_member['mobile_numbers'] = user_details.get('mobile_numbers', [])
            staff_data.append(staff_member)

    return render_template('staff_table.html', staff_data=staff_data)

if __name__ == '__main__':
    app.run(debug=True)
