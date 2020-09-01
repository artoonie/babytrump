import babytrump
import time
import traceback

import gpt3_light as gpt3

def run_now(baby_monitor):
  infanticizer = gpt3.Infanticizer()

  statuses = baby_monitor.read_stream()
  for s in statuses:
    print()
    tweet = infanticizer.process(s)
    if not tweet:
      print("No valid tweet, skipping ", s)
      continue

    baby_monitor.tweet(tweet)
  print('.',)

def run_continuously():
  baby_monitor = babytrump.TwitterBabyMonitor()
  errorCount = 0
  
  while True:
    try:
      run_now(baby_monitor)
      time.sleep(60)
    except KeyboardInterrupt:
      print("Safely quitting")
      exit(0)
    except Exception as e:
      print("Error count is", errorCount)
      traceback.print_exc()
      errorCount += 1
      if errorCount > 50:
        exit(-1)
      continue

def run_once():
  baby_monitor = babytrump.TwitterBabyMonitor()
  run_now(baby_monitor)
