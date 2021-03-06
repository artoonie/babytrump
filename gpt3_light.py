import abc
import random
import re

class Converter(abc.ABC):
  @abc.abstractmethod
  def can_do(self, tweet): pass

  @abc.abstractmethod
  def do(self, tweet, tokensToNotTouch = []): pass

  def get_rand_to_pattern(self):
    return random.choice(self.toPatterns)

  @classmethod
  def _split_list_of_strings_then_join(self, listOfStrings):
    return [token for string in listOfStrings for token in string.split()]

  def run_on_modifiable_tokens(self, tweet, tokensToNotTouch, func):
    """ Run func on each non-@user, non-@tag, non-URL token. Not very smart yet. """
    # Convert e.g. ['Momsicle, ', 'Mommy, '] into ['momsicle', ',', 'mommy', ',']
    tokensToNotTouch = self._split_list_of_strings_then_join(tokensToNotTouch)
    tokensToNotTouch.extend(self._split_list_of_strings_then_join(self.alwaysIgnoreTokens))
    tokensToNotTouch = [t.lower() for t in tokensToNotTouch]

    newtweetTokens = []
    for token in tweet.split():
      if token.startswith('#') or token.startswith('@') or token.startswith('http'):
        newtweetTokens.append(token)
      elif token.lower() in tokensToNotTouch:
        newtweetTokens.append(token)
      else:
        newtweetTokens.append(func(token))
    return ' '.join(newtweetTokens)

  alwaysIgnoreTokens = ('lose', 'loses', 'slow', 'people', 'where', 'help',)

class ManySubstitutionsBaseConverter(Converter):
  def additionalIgnoreTokens(self):
    # To patterns without \1 \2 etc
    return [re.sub(r'\\\d', '', s[1]) for s in self.substitutions]

  @property
  def substitutions(self):
    raise NotImplementedError

  @property
  def dont_touch_users_or_tags(self):
    return False

  def can_do(self, tweet):
    # Not entirely accurate - doesn't check exclusion lists or parse into tokens
    return any([re.search(sub[0], tweet) for sub in self.substitutions])

  def _do_on_token(self, token):
    for fromPattern, toPattern in self.substitutions:
      token = re.sub(fromPattern, toPattern, token)
    return token

  def do(self, tweet, tokensToNotTouch):
    if not self.dont_touch_users_or_tags:
      return self._do_on_token(tweet)
    else:
      return self.run_on_modifiable_tokens(tweet, tokensToNotTouch, self._do_on_token)

class SingleRandomSubstitutionBaseConverter(Converter):
  def additionalIgnoreTokens(self):
    # To patterns without \1 \2 etc
    return [re.sub(r'\\\d', '', s) for s in self.toPatterns]

  @property
  def fromPattern(self):
    raise NotImplementedError

  @property
  def toPatterns(self):
    raise NotImplementedError

  def can_do(self, tweet):
    return re.search(self.fromPattern, tweet) is not None

  def do(self, tweet, tokensToNotTouch):
    if tweet in tokensToNotTouch:
      return tweet
    self.toPatternUsed = self.get_rand_to_pattern()
    return re.sub(self.fromPattern, self.toPatternUsed, tweet, count=1)

class ElmerFuddLight(ManySubstitutionsBaseConverter):
  substitutions = ((r'^(.*[^rlw]+)[rl]([^rlw]+.*)$', r'\1w\2'), # rl to w, only in middle of word, except double letters
                   (r'qu', r'qw'),
                   (r'th\b', r'f'),
                   (r'th', r'd'),
                   (r'erl', r'ahl'))

  dont_touch_users_or_tags = True

class ElmerFudd(ManySubstitutionsBaseConverter):
  substitutions = ((r'(?<![wW])[rl](?![rlw]?$)', r'w'), # no double-letter subs at end of word
                   (r'qu', r'qw'),
                   (r'th\b', r'f'),
                   (r'th', r'd'))

  dont_touch_users_or_tags = True

class WordEndings(ManySubstitutionsBaseConverter):
  substitutions = ((r'ers(?=[!. ?]|\b)', r'ahs'), # fuckers to fuckahs
                   (r'er(?=[!. ?]|\b)', r'ah')) # fucker to fuckah

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

class FoxNews(SingleRandomSubstitutionBaseConverter):
  fromPattern = r'@FoxNews'
  toPatterns = (r'@FucksNews',
                r'Fake News @FoxNews')

class FoxNewsAt(SingleRandomSubstitutionBaseConverter):
  fromPattern = r'@FoxNews'
  toPatterns = (r'@PornHub',
                r'@FucksNews',
                r'Fake News @FoxNews',
                r'Failing @FoxNews')

class FoxNews(SingleRandomSubstitutionBaseConverter):
  fromPattern = r'Fox News'
  toPatterns = (r'Big Bullies News',
                r'Fucks News',
                r'Guilt-Free Racism Channel')

class Antifa(SingleRandomSubstitutionBaseConverter):
  fromPattern = r'Antifa'
  toPatterns = (r'Meanies who voted 4 hillry',
                r'Nazi-haters',
                r'Buttface Libs')

class Democrats(SingleRandomSubstitutionBaseConverter):
  fromPattern = r'Democrats'
  toPatterns = (r'Ppl who dont like me',
                r'Buggerbutt Dems',
                r'Demotwats')

class LawOrder(SingleRandomSubstitutionBaseConverter):
  fromPattern = r'LAW & ORDER'
  toPatterns = (r'I JUST FARTED',
                r'I LIKE POLICE RACISM',
                r'BLACK PPL SHUD JUST GET OVER IT')

class InnerCity(SingleRandomSubstitutionBaseConverter):
  fromPattern = r'[iI]nner [cC]ity'
  toPatterns = (r'black parts of the city',
                r'shithole neighborhoods',
                r'poor people homeses')

class Mommy(SingleRandomSubstitutionBaseConverter):
  fromPattern = r'([ ]*)([^.!?]*)([!?]*\?[!?]*)'
  toPatterns = (r'\1Mommy, \2\3',
                r'\1Momma, \2\3',
                r'\1Momsie, \2\3',
                r'\1Momsicle, \2\3')

  def do(self, tweet, tokensToNotTouch):
    tweet = super(Mommy, self).do(tweet, tokensToNotTouch)
    toPattern = self.toPatternUsed

    # Lowercase the first character of the next sentence
    match = re.search(', [A-Z]', tweet)
    if match:
      i = match.end()
      tweet = tweet[:i-1] + tweet[i-1].lower() + tweet[i:]
    return tweet

class WordSubs(ManySubstitutionsBaseConverter):
  substitutions = ((r'\breally\b', r'rilly'),
                   (r'\bwill\b', r'will'),
                   (r'\bthe\b', r'da'),
                   (r'[cC]ongress\b', r'Congriss'),
                   (r'kind of\b', r'kinda'),
                   (r'Joe Hiden\b', r'Sociawwy-Distant Joe'))

class Infanticizer():
  def __init__(self):
    self.processorGroups = (
      # First group (will do as many in group as it can)
      {
        'try': (
          JoeBiden(),
          SleepyJoe(),
          Mommy(),
          FoxNews(),
          FoxNewsAt(),
          Antifa(),
          LawOrder(),
          InnerCity(),
          Democrats()
       ),
       'finally': (
          WordSubs(),
          WordEndings(),
          ElmerFuddLight(),
       )
      },
      # Second group (only if nothing succeeded in first group)
      {
        'try': (
          WordSubs(),
          WordEndings(),
          ElmerFuddLight(),
          ElmerFudd(),
        ),
        'finally': ()
      }
    )

  def is_tweet_valid(self, tweet):
    return len(tweet) <= 280

  def run_processors_on_tweet(self, tweet, tokensToNotTouch, processors):
    """ Run each processor on the tweet, if valid """
    didProcess = False
    for processor in processors:
      if not processor.can_do(tweet):
        continue
      potentialTweet = processor.do(tweet, tokensToNotTouch)
      if self.is_tweet_valid(potentialTweet):
        tweet = potentialTweet
        didProcess = True
        tokensToNotTouch.extend(processor.additionalIgnoreTokens())
    return {'tweet': tweet,
            'tokensToNotTouch': tokensToNotTouch,
            'didProcess': didProcess}

  def tryToProcessTweetWithEverythingInGroup(self, tweet, group):
    result = self.run_processors_on_tweet(tweet, [], group['try'])
    if result['didProcess']:
      result2 = self.run_processors_on_tweet(result['tweet'], result['tokensToNotTouch'], group['finally'])
      return result2['tweet']

    return None

  def process(self, tweet):
    for processorGroup in self.processorGroups:
      potentialTweet = self.tryToProcessTweetWithEverythingInGroup(tweet, processorGroup)

      # If we got a result, this process wins. Stop here.
      if potentialTweet:
        return potentialTweet

    return None
