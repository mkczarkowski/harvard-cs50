# [Problem set 3: Game of Fifteen](http://docs.cs50.net/2016/fall/psets/3/pset3.html)

### Objectives
+ Accustom you to reading someone else’s code.
+ Introduce you to larger programs and programs with multiple source files.
+ Empower you with Makefiles.
+ Implement a party favor.

### What I built
+ [find.c](https://github.com/mkczarkowski/harvard-cs50/tree/master/pset3/find/find.c), a program that finds a number among numbers, per the below.
```
$ ./generate 1000 | ./find 42
Didn't find needle in haystack.
```
+ [fifteen.c](https://github.com/mkczarkowski/harvard-cs50/tree/master/pset3/fifteen/fifteen.c), a program based on [The Game of Fifteen](https://en.wikipedia.org/wiki/15_puzzle).
```
$ ./fifteen 3
WELCOME TO GAME OF FIFTEEN

8  7  6

5  4  3

2  1  _

Tile to move:
```
