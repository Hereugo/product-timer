# product-timer

- I want to have a simple CLI tool that when called, will start the timer, when called again will stop.
- We must save the period in csv format:
  - id
  - label
  - start time
  - end time
  - timestamp

flags:

```
[ACTION] = {create, delete, start, end, view}
- [ACTION] [LABELS ...]
    - create: create new timer with some label
    - delete: display a list of timers of some label to which it need to be deleted
    - start: start timer with some label
    - end: stop timer at label
    - view: view active timers in a list

- "-l --log [FILE]" the file where the timers should be appended to
- "-f --format [TIME_FORMAT]" view timers of given label
```
