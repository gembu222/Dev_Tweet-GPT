from requests_oauthlib import OAuth1Session
import os
from dotenv import load_dotenv
import json
import openai


# .envファイルの内容を読み込見込む
load_dotenv()

# In your directly please make .env file by describing the following lines of code.
# CONSUMER_KEY="<your_consumer_key>"
# CONSUMER_SECRET="<your_consumer_secret>

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("TWI_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWI_ACCESS_TOKEN_SECRET")
openai.organization = os.environ.get("ORGANIZATION_ID")
openai.api_key = os.environ.get("GPT_TEST_KEY")

model = "text-davinci-003"

# Be sure to add replace the text of the with the text you wish to Tweet. You can also add parameters to post polls, quote Tweets, Tweet with reply settings, and Tweet to Super Followers in addition to other features.
"""
message = (
        "PythonからTwitter APIを使ってツイート\n"
        + "2行目\n"
        + "https://www.google.com/"
    )
"""
message = "cahtGPTに与える文言"

"""ユーザー認証を行う場合
# Get request token
request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

try:
        fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
        print(
                    "There may have been an issue with the consumer_key or consumer_secret you entered."
                )

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)

# Get authorization
base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Please go here and authorize: %s" % authorization_url)
verifier = input("Paste the PIN here: ")

# Get the access token
access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier,
        )
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]
"""
# Make the request
oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )

completion = openai.ChatCompletion.create(
                 model    = "gpt-3.5-turbo",     # モデルを選択
                 messages = [{
                            "role":"user",       # 役割
                            "content":message,   # メッセージ 
                            }],
    
                 max_tokens  = 140,             # 生成する文章の最大単語数
                 n           = 1,                # いくつの返答を生成するか
                 stop        = None,             # 指定した単語が出現した場合、文章生成を打ち切る
                 temperature = 0.5,              # 出力する単語のランダム性（0から2の範囲） 0であれば毎回返答内容固定
    )
    
# 応答
response = completion.choices[0].message.content

payload = {"text": response }

# Making the request
response = oauth.post(
                "https://api.twitter.com/2/tweets",
                json=payload,
            )

if response.status_code != 201:
        raise Exception(
                    "Request returned an error: {} {}".format(response.status_code, response.text)
                )   

print("Response code: {}".format(response.status_code))

# Saving the response as JSON
json_response = response.json()
print(json.dumps(json_response, indent=4, sort_keys=True))
