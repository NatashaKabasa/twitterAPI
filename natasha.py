from pytwitter import Api

consumer_keys = "tuxbNezcLxipie3VWHXprS2sc"
consumer_secret = "NFBht0B5kYJSQTCBygntaHmN3SMyfQifjvhycE0pLyl5mE3smr"
access_token = "1406163817386721280-xv4imJGyBTVZ0F2HefzzCUCBBIULqU"
access_secret = "zFHPUgQgZELUVRO30QruMGo2n6SGqHPy6JJM7bpkyIBwm"


api = Api(consumer_key = consumer_keys, consumer_secret = consumer_secret, access_token = access_token, access_secret = access_secret)
# get url for user to authorize
#url = api.get_authorize_url()
# copy the response url

#print(url)

response = api.get_users(ids=["783214", "2244994945"])

print(response.data)
