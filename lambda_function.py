import babytrump
import time

import gpt3_light as gpt3
import runner

def lambda_handler(event, context):
  babyMonitor = babytrump.TwitterBabyMonitor()
  runner.run_now(babyMonitor)
