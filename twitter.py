"""Sends tweets."""


def tweet_now(url, summary):
    """Tweet using Twitter API.

    Tweet is sent now.
    """
    print(("Twitter : Sent {} with"
           " summary : {} using twitter ").format(url, summary))


def buffer(url, summary):
    """Tweet using the buffer API.

    Tweet is added to the buffer queue.
    If the queue is full, tweet is delayed until it's OK.
    """
    print(("Twitter : Sent {} with"
           " summary : {} using buffer ").format(url, summary))
