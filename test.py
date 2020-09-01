import random
import pytest

import gpt3_light as gpt3

def assert_converts(converter, fromText, toText=None):
  """ if toText is None, ensures not can_do """
  if toText is None:
    assert not converter.can_do(fromText)
  else:
    random.seed(0)
    assert converter.can_do(fromText)
    assert converter.do(fromText) == toText

def test_elmer_fudd():
  assert_converts(gpt3.ElmerFudd(),
    'Hello can I quit playing with the ball?',
    'Hewwo can I qwit pwaying wif de baww?')

  assert_converts(gpt3.ElmerFudd(),
    'Hello can I #quit @playing with the ball?',
    'Hewwo can I #quit @playing wif de baww?')

  assert_converts(gpt3.ElmerFudd(),
    '@Hello @can @I @quit @playing @with @the @ball?',
    '@Hello @can @I @quit @playing @with @the @ball?')

  assert_converts(gpt3.ElmerFudd(),
    '#Hello #can #I #quit #playing #with #the #ball?',
    '#Hello #can #I #quit #playing #with #the #ball?')

  # This isn't handled yet - should be #the!baww
  assert_converts(gpt3.ElmerFudd(),
    '#the!ball?',
    '#the!ball?')

  # This isn't handled yet - should be Ilike#balls
  assert_converts(gpt3.ElmerFudd(),
    'Ilike#balls?',
    'Iwike#bawws?')

def test_joe_biden():
  assert_converts(gpt3.JoeBiden(),
    'Joe Biden is mean to me!',
    'Jerk Biden is mean to me!')

  assert_converts(gpt3.JoeBiden(),
    'Sleep Joe is mean to me!',
    None)

def test_sleepy_joe():
  assert_converts(gpt3.SleepyJoe(),
    'Sleepy Joe is mean to me!',
    'Meanie Joe is mean to me!')

  assert_converts(gpt3.JoeBiden(),
    'Boring Joe is mean to me!',
    None)

def test_mommy():
  assert_converts(gpt3.Mommy(),
    'Why is Biden better than me?',
    'Momsicle, why is Biden better than me?')

  assert_converts(gpt3.JoeBiden(),
    'Why is Biden better than me!',
    None)

  # Only the first sentence with a Q:
  assert_converts(gpt3.Mommy(),
    'I\'m so mad at Hilary! Why did people vote for her more? Was I naughty?',
    'I\'m so mad at Hilary! Momsicle, why did people vote for her more? Was I naughty?')

def test_all():
  tweets = ['When is Slow Joe Biden going to criticize the Anarchists, Thugs & Agitators in ANTIFA? When is he going to suggest bringing up the National Guard in BADLY RUN & Crime Infested Democrat Cities & States? Remember, he can’t lose the Crazy Bernie Super Liberal vote!',
            'Joe Biden is coming out of the basement earlier than his hoped for ten days because his people told him he has no choice, his poll numbers are PLUNGING! Going to Pittsburgh, where I have helped industry to a record last year, & then back to his  basement for an extended period...',
            'LAW & ORDER!!!']
  expected_results =\
    ['Mommy, when is Slow Jerk Biden going to criticize the Anarchists, Thugs & Agitators in ANTIFA? When is he going to suggest bringing up the National Guard in BADLY RUN & Crime Infested Democrat Cities & States? Remember, he can’t lose the Crazy Bernie Super Liberal vote!',
     'Joe Biden is coming out of de basement eawwiew dan his hoped fow ten days because his peopwe towd him he has no choice, his poww numbews awe PLUNGING! Going to Pittsbuwgh, whewe I have hewped industwy to a wecowd wast yeaw, & den back to his basement fow an extended pewiod...',
     'BLACK PPL SHUD JUST GET OVER IT!!!']

  infanticizer = gpt3.Infanticizer()
  for i, tweet in enumerate(tweets):
      assert infanticizer.process(tweet) == expected_results[i]
