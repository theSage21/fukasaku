Fukasaku
=========


The sage frog in Naruto keeps track of which Naruto clone is turning into a frog and gives it a whack!

This program monitors total system RAM and in case it falls below a certain limit, suspends the process which is the largest consumer of RAM.

It's useful when you run data science experiments (maybe in jupyter) and they eat up your RAM, forcing you to reboot and lose state.


Usage
-----

In a terminal somewhere run fukasaku and tell it to watch every 5s and start suspending if RAM goes below 1GiB. You can leave out those details and conservative estimates will be made.

Since fukasaku needs to order other processes about, it needs sudo.

```bash
git clone https://github.com/theSage21/fukasaku
cd fukasaku
sudo python fukasaku.py -m 1G -i 5s &
```


Todo
----

- [ ] notifications about suspensions. email?
- [ ] do this without Sudo
- [ ] windows?
