# product-timer

- I want to have a simple CLI tool that when called, will start the timer, when called again will stop.
- We must save the period in csv format:
  - id
  - label
  - start time
  - end time
  - timestamp

flags:

- "-c --create [LABEL]" create new timer with some label
- "-d --delete [LABEL]" displays a list of timers of some label to which it need to be deleated
- "-s --start [LABEL]" start timer with some label
- "-f --finish --stop [LABEL]" stop timer at label
- "-r --resume [LABEL]" resume timer at label
- "-s --save [FILE_DEST]" save timers to output file
- "-l --log [FILE]" the file where the timers should be appended to

- "-v --view" view active timers in a list
