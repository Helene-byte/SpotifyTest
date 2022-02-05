import base64

import requests
import spotify_client
client_id = 'd58bc94036cc4afbbef667a8ea730438'
client_secret = 'eabb60a6c63744dc931ce15e7d8b0e81'
spotify= spotify_client.SpotifyAPI(client_id,client_secret)

def test_get_access_token():
    spotify.get_access_token()
    # and not an Exception
    print (spotify.get_access_token())
    assert spotify.get_access_token() is not None

def test_search_success():
    search_success=spotify.search("Beatles",search_type="Track")
    print(search_success)
    assert search_success !={}
#
# def test_get_locations_for_us_90210_check_country_equals_united_states():
#     response = requests.get("http://api.zippopotam.us/us/90210")
#     response_body = response.json()
#     assert response_body["country"] == "United States"
#
#
# def test_get_locations_for_us_90210_check_city_equals_beverly_hills():
#     response = requests.get("http://api.zippopotam.us/us/90210")
#     response_body = response.json()
#     assert response_body["places"][0]["place name"] == "Beverly Hills"
#
#
# def test_get_locations_for_us_90210_check_one_place_is_returned():
#     response = requests.get("http://api.zippopotam.us/us/90210")
#     response_body = response.json()
#     assert len(response_body["places"]) == 1