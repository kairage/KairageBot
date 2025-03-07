import tweepy
import time
import random
from datetime import datetime

# X API credentials (we’ll add these later in Heroku)
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ACCESS_TOKEN_SECRET = "YOUR_ACCESS_TOKEN_SECRET"

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

TARGETS = ["Midjourney", "StableDiffusion"]  # Add more accounts later
KEYWORDS = ["AI art", "generative AI", "Midjourney"]
RANTS = [
    "Ugh, {text}—pure trash. Use --v 6 to make it less vomit-worthy, fool.",
    "Wow, {text}. Soulless junk—try negative prompts, you hack.",
    "{text}? Disgusting. Crank CFG to 7 and suffer, clown.",
    "More {text} slop. Upscale to 4k for bigger garbage, moron.",
    "{text} again? Lame—tweak --ar 1:1 and cry, idiot."
]
REPLIED_TWEETS = set()

def get_kairage_rant(post_text):
    rant = random.choice(RANTS)
    return rant.format(text=post_text[:20])

def scan_and_snipe():
    print(f"[{datetime.now()}] Kairage’s hunting...")
    query = f"{' OR '.join(KEYWORDS)} {' OR '.join(['from:' + acc for acc in TARGETS])} -from:KairageWTF"
    tweets = api.search_tweets(q=query, count=10, tweet_mode="extended")
    
    for tweet in tweets:
        tweet_id = tweet.id
        if tweet_id not in REPLIED_TWEETS:
            try:
                text = tweet.full_text
                username = tweet.user.screen_name
                rant = get_kairage_rant(text)
                api.update_status(
                    status=f"@{username} {rant}",
                    in_reply_to_status_id=tweet_id
                )
                REPLIED_TWEETS.add(tweet_id)
                print(f"Sniped {tweet_id}: {rant}")
                time.sleep(60)
            except tweepy.TweepyException as e:
                print(f"Oops: {e}")

while True:
    scan_and_snipe()
    time.sleep(900)  # 15-min breaks
