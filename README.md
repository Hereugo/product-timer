# product-timer

- I want to have a simple CLI tool that when called, will start the timer, when called again will stop.
- We must save the period in csv format:
  - timestamp
  - start time
  - end time
  - time diff
  - label

flags:

- "-c --create [LABEL]" create new timer with some label
- "-d --delete [LABEL]" delete timer with some label
- "-s --start [LABEL]" start timer with some label
- "-f --finish --stop [LABEL]" stop timer at label
- "-r --resume [LABEL]" resume timer at label

- "-v --view" view active timers in a list
