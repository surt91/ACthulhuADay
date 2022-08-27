import tweepy

from keys_and_secrets import keys_and_secrets

auth = tweepy.OAuth1UserHandler(
    keys_and_secrets["consumer_key"],
    keys_and_secrets["consumer_secret"],
    keys_and_secrets["access_token_key"],
    keys_and_secrets["access_token_secret"]
)

# wait if we hit twitters rate limit (15 requests in 15 minutes)
# this way all tweets will be accepted and we have a rudimentary DOS protection
# if this bot is too successful. Twitter itself will protect us from malicious DOS
api = tweepy.API(auth, wait_on_rate_limit=True)


def tweet_pic(path, text=None, reply_to=None):
    api.update_status_with_media(status=text, filename=path, in_reply_to_status_id=reply_to)
