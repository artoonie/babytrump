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

def test_elmer_fudd_light():
  assert_converts(gpt3.ElmerFuddLight(),
    'Hello can I quit playing with the ball',
    'Hello can I qwit playing wif de ball')

  assert_converts(gpt3.ElmerFuddLight(),
    'poll',
    None)

  assert_converts(gpt3.ElmerFuddLight(),
    'pol',
    'pow')

  assert_converts(gpt3.ElmerFuddLight(),
    'polw',
    None)

def test_elmer_fudd():
  assert_converts(gpt3.ElmerFudd(),
    'poll',
    None)

  # Not super important, but note ElmerFuddLight will take care of single-letter subs at end of word
  assert_converts(gpt3.ElmerFudd(),
    'pol',
    None)

  assert_converts(gpt3.ElmerFudd(),
    'Hello can I quit playing with the ball ?',
    'Hewwo can I qwit pwaying wif de ball ?')

  assert_converts(gpt3.ElmerFudd(),
    'Hello can I #quit @playing with the ball ?',
    'Hewwo can I #quit @playing wif de ball ?')

  assert_converts(gpt3.ElmerFudd(),
    '@Hello @can @I @quit @playing @with @the @ball?',
    '@Hello @can @I @quit @playing @with @the @ball?')

  assert_converts(gpt3.ElmerFudd(),
    '#Hello #can #I #quit #playing #with #the #ball?',
    '#Hello #can #I #quit #playing #with #the #ball?')

  # Don't create double-Ws
  assert_converts(gpt3.ElmerFudd(),
    'Wrote rote wlee',
    'Wrote wote wlee')
  assert_converts(gpt3.ElmerFudd(),
    'poll',
    None)

  # Don't touch r at end of word
  assert_converts(gpt3.ElmerFudd(),
    'year',
    None)

  # This isn't handled yet - should be polls? but doesn't work with the '?' at end
  assert_converts(gpt3.ElmerFudd(),
    'polls?',
    'powws?')

  # This isn't handled yet - should be untouched (no changing 'r' at end of word)
  assert_converts(gpt3.ElmerFudd(),
    'year!',
    'yeaw!')

  # This isn't handled yet - should be #the!baww
  assert_converts(gpt3.ElmerFudd(),
    '#the!ball?',
    '#the!ball?')

  # This isn't handled yet - should be Ilike#balls
  assert_converts(gpt3.ElmerFudd(),
    'Ilike#balls?',
    'Iwike#bawws?')

def test_word_endings():
  assert_converts(gpt3.WordEndings(),
    'haters',
    'hatahs')
  assert_converts(gpt3.WordEndings(),
    'hater!',
    'hatah!')
  assert_converts(gpt3.WordEndings(),
    'bernie',
    None)

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

def test_inner_city():
  assert_converts(gpt3.InnerCity(),
    'Inner City',
    'shithole neighborhoods')

def test_all():
  tweets =\
    ['When is Slow Joe Biden going to criticize the Anarchists, Thugs & Agitators in ANTIFA? When is he going to suggest bringing up the National Guard in BADLY RUN & Crime Infested Democrat Cities & States? Remember, he can’t lose the Crazy Bernie Super Liberal vote!',
     'Joe Biden is coming out of the basement earlier than his hoped for ten days because his people told him he has no choice, his poll numbers are PLUNGING! Going to Pittsburgh, where I have helped industry to a record last year, & then back to his  basement for an extended period...', # long tweet: falls into group 2
     'Joe Biden is coming out of the basement earlier than his hoped for ten days because his people told him he has no choice, his poll numbers are PLUNGING! Going to Pittsburgh, where I have helped industry to a record last year', # shorter tweet: falls into group 1
     'LAW & ORDER!!!',
     'Kimberly Klacik is really working hard to help the people of Baltimore. She is running for Congress as a Republican, & if she wins she will be an inspiration to all. She is strong on inner city rebuilding, healthcare, our Military & Vets. She has my Complete & Total Endorsement!', # group 2
     'Kimberly Klacik is really working hard to help the people of Baltimore. Joe Biden!!!!' # group 1
     ]
  expected_results =\
    ['Momsicle, when is Slow Jerk Biden going to criticize da Anarchists, Thugs & Agitators in ANTIFA? When is he going to suggest bringing up da Nationaw Guard in BADLY RUN & Crime Infested Democrat Cities & States? Remembah, he can’t lose da Crazy Bernie Supah Liberaw vote!',
     'Joe Biden is coming out of da basement eawwiah dan his hoped fow ten days because his peopwe towd him he has no choice, his poll numbahs awe PLUNGING! Going to Pittsbuwgh, whewe I have hewped industwy to a wecowd wast yeaw, & den back to his basement fow an extended pewiod...',
     'Jerk Biden is coming out of da basement earliah dan his hoped fow ten days because his people told him he has no choice, his poll numbahs are PLUNGING! Going to Pittsburgh, where I have helped industry to a record last yeaw',
     'I LIKE POLICE RACISM!!!',
     'Kimbahwy Kwacik is wiwwy wowking hawd to hewp da peopwe of Bawtimowe. She is wunning fow Congwiss as a Repubwican, & if she wins she will be an inspiwation to aww. She is stwong on innah city webuiwding, heawdcawe, ouw Miwitawy & Vets. She has my Compwete & Totaw Endowsement!',
     'Kimbahly Klacik is rilly working hard to help da people of Baltimore. Jerk Biden!!!!'
     ]

  infanticizer = gpt3.Infanticizer()
  for i, tweet in enumerate(tweets):
    random.seed(0)
    assert infanticizer.process(tweet) == expected_results[i]
