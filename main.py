from twitter import TwitterClient
from firebase import Firebase

def twitter():
    firebase = Firebase("Twitter")
    docs = firebase.get_stream()

    for doc in docs:
        doc_id = doc.id
        doc = doc.to_dict()
        twitter_client = TwitterClient(doc["screen_name"])
        unseen_tweets = twitter_client.get_user_timeline_unseen_tweets(doc["last_seen_id"])

        if unseen_tweets:
            twitter_client.favorite_and_retweet(unseen_tweets,
                                                filter_word=doc.get("filter_word", ""))
            doc["last_seen_id"] = str(unseen_tweets[0].id)
            firebase.update(doc_id, doc)

def main():
    twitter()

if __name__ == '__main__':
    main()