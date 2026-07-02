OFF_TOPIC = [
    "ipl",
    "cricket",
    "football",
    "movie",
    "weather",
    "bitcoin",
    "politics",
    "recipe",
    "music"
]


def is_off_topic(text):

    text = text.lower()

    for word in OFF_TOPIC:
        if word in text:
            return True

    return False