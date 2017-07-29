# [Problem set 6: Sentimental](http://docs.cs50.net/2017/x/psets/6/pset6.html)

### Objectives
+ Become familiar with HTTP.
+ Apply familiar techniques in unfamiliar contexts.
+ Transition from C to web programming.

### What I built
+ [mario.py](https://github.com/mkczarkowski/harvard-cs50/tree/master/pset6/mario.py), 
a program that prints out a double half-pyramid of a specified height, per the below.
```
$ ./mario
Height: 4
   #  #
  ##  ##
 ###  ###
####  ####
```
+ [credit.py](https://github.com/mkczarkowski/harvard-cs50/tree/master/pset6/credit.py),
a program that determines whether a provided credit card number is valid according to Luhn’s algorithm.
```
$ ./credit
Number: 378282246310005
AMEX
```
+ [crack.py](https://github.com/mkczarkowski/harvard-cs50/tree/master/pset6/crack.py), 
a program that cracks passwords, per the below.
```
$ ./crack 50fkUxYHbnXGw
rofl
```
+ [smile](https://github.com/mkczarkowski/harvard-cs50/tree/master/pset6/sentiments/smile), 
a program that categorizes a word as positive or negative.
```
$ ./smile love
:)
$ ./smile hate
:(
$ ./smile Stanford
:|
```
+ [tweets](https://github.com/mkczarkowski/harvard-cs50/tree/master/pset6/sentiments/tweets),
a program that categorizes a user’s tweets as positive or negative.
```
$ ./tweets @cs50
 0 hello, @world
 1 I love you, @world
-1 I hate you, @world
...
```
+ [application.py](https://github.com/mkczarkowski/harvard-cs50/tree/master/pset6/sentiments/application.py), 
a website that generates a pie chart categorizing a user’s tweets.