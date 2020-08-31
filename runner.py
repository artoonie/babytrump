import babytrump
import time

import gpt3_light as gpt3

def do(pythonTwitter):
  infanticizer = gpt3.Infanticizer()

  statuses = pythonTwitter.read_stream()
  for s in statuses:
    tweet = infanticizer.process(s)
    if not tweet:
      print("No valid tweet, skipping ", s)
      continue

    pythonTwitter.tweet(tweet)

pythonTwitter = babytrump.PythonTwitter()
errorCount = 0

while True:
  try:
    do(pythonTwitter)
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
