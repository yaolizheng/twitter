import random

nouns = ["A dude", "My mom", "The king", "Some guy", "A cat with rabies", "A sloth", "Your homie", "This cool guy my gardener met yesterday", "Superman"]
verbs = ["eats", "kicks", "gives", "treats", "meets with", "creates", "hacks", "configures", "spies on", "retards", "meows on", "flees from", "tries to automate", "explodes"]
infinitives = ["to make a pie.", "for no apparent reason.", "because the sky is green.", "for a disease.", "to be able to make toast explode.", "to know more about archeology."]


def generate_tweets():
    res = ""
    for _ in range(random.randint(1, 10)):
        tweets = [random.choice(nouns), random.choice(verbs), random.choice(nouns), random.choice(infinitives)]
        print ' '.join(tweets)
        res += ' '.join(tweets) + ' '
    return res


if __name__ == '__main__':
    print generate_tweets()
