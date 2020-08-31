import random
import pytest

import gpt3_light as gpt3

example_tweets = ['When is Slow Joe Biden going to criticize the Anarchists, Thugs &amp; Agitators in ANTIFA? When is he going to suggest bringing up the National Guard in BADLY RUN &amp; Crime Infested Democrat Cities &amp; States? Remember, he can’t lose the Crazy Bernie Super Liberal vote!',
                  'Joe Biden is coming out of the basement earlier than his hoped for ten days because his people told him he has no choice, his poll numbers are PLUNGING! Going to Pittsburgh, where I have helped industry to a record last year, &amp; then back to his  basement for an extended period...',
                  'RT @realDonaldTrump: LAW &amp; ORDER!!!',
                  'RT @realDonaldTrump: The only way you will stop the violence in the high crime Democrat run cities is through strength!']

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

