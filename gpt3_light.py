import abc
import random
import re

class Converter(abc.ABC):
  @abc.abstractmethod
  def can_do(self, tweet): pass

  @abc.abstractmethod
  def do(self, tweet): pass

  def get_rand_to_pattern(self):
    return random.choice(self.toPatterns)


class ManySubstitutionsBaseConverter(Converter):
  @property
  def substitutions(self):
    raise NotImplementedError

  def can_do(self, tweet):
    return any([re.search(sub[0], tweet) for sub in self.substitutions])

  def do(self, tweet):
    for fromPattern, toPattern in self.substitutions:
      tweet = re.sub(fromPattern, toPattern, tweet)
    return tweet

class SingleRandomSubstitutionBaseConverter(Converter):
  @property
  def fromPattern(self):
    raise NotImplementedError

  @property
  def toPatterns(self):
    raise NotImplementedError

  def can_do(self, tweet):
    return re.search(self.fromPattern, tweet) is not None

  def do(self, tweet):
    self.toPatternUsed = self.get_rand_to_pattern()
    return re.sub(self.fromPattern, self.toPatternUsed, tweet, count=1)

class ElmerFudd(ManySubstitutionsBaseConverter):
  substitutions = ((r'[rl]', r'w'),
                   (r'qu', r'qw'),
                   (r'th\b', r'f'),
                   (r'th', r'd'))

class JoeBiden(SingleRandomSubstitutionBaseConverter):
  fromPattern = r'Joe Biden'
  toPatterns = (r'Joey ByeBye',
                r'Joe Poopieden',
                r'Joe Bad-en',
                r'Jerk Biden')

class SleepyJoe(SingleRandomSubstitutionBaseConverter):
  fromPattern = r'Sleepy Joe'
  toPatterns = (r'Sweepy Joe',
                r'Bedtime Buddy Joey',
                r'Pajama Party Joe',
                r'Meanie Joe')

class Mommy(SingleRandomSubstitutionBaseConverter):
  fromPattern = r'([ ]*)([^.!?]*)\?'
  toPatterns = (r'\1Mommy, \2?',
                r'\1Momma, \2?',
                r'\1Momsie, \2?',
                r'\1Momsicle, \2?')

  def do(self, tweet):
    tweet = super(Mommy, self).do(tweet)
    toPattern = self.toPatternUsed

    # Lowercase the first character of the next sentence
    match = re.search(', [A-Z]', tweet)
    if match:
      i = match.end()
      tweet = tweet[:i-1] + tweet[i-1].lower() + tweet[i:]
    return tweet

class Infanticizer():
  def __init__(self):
    self.processorGroups = (
      # First group:
      (
        JoeBiden(),
        SleepyJoe(),
        Mommy(),
      ),
      # Second group:
      (
        ElmerFudd(),
      ),
    )

  def is_tweet_valid(self, tweet):
    if len(tweet) <= 280:
      return True

  def tryToProcessTweetWithEverythingInGroup(self, tweet, group):
    didProcess = False
    for processor in group:
      if not processor.can_do(tweet):
        continue
      potentialTweet = processor.do(tweet)
      if self.is_tweet_valid(potentialTweet):
        tweet = potentialTweet
        didProcess = True

    if didProcess:
      return tweet

    return None

  def process(self, tweet):
    for processorGroup in self.processorGroups:
      potentialTweet = self.tryToProcessTweetWithEverythingInGroup(tweet, processorGroup)

      # If we got a result, this process wins. Stop here.
      if potentialTweet:
        return potentialTweet

    return None
