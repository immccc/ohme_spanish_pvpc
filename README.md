# Spanish PVPC Energy for OHME charger

# Context
Amongst the list of electricity providers, OHME does not have support yet for PVPC, a regulated price model which is updated daily.

This script is aimed to update a particular charger, with the current daily electricy price, so OHME chargers can calculate costs accordingly.


## How to run
This is a tool mainly focused on being run daily from a cronjob. But it's usage is fairly simple: 

```
uv run main.py
```

Please ensure you have set up your Ohme user account and password, and yes, a prerequisite is that log in is through email.