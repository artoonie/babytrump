import babytrump
import time

import gpt3_light as gpt3

def do(babyMonitor):
  infanticizer = gpt3.Infanticizer()

  statuses = babyMonitor.read_stream()
  for s in statuses:
    tweet = infanticizer.process(s)
    if not tweet:
      print("No valid tweet, skipping ", s)
      continue

    babyMonitor.tweet(tweet)

babyMonitor = babytrump.TwitterBabyMonitor()
errorCount = 0

while True:
  try:
    do(babyMonitor)
    time.sleep(60)
  except KeyboardInterrupt:
    print("Safely quitting")
    exit(0)
  except Exception as e:
    print("Error count is", errorCount)
    print("Exception:", e)
    errorCount += 1
    if errorCount > 50:
      exit(-1)
    continue
