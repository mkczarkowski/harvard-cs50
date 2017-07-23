# [Problem set 2: Crypto](http://docs.cs50.net/2016/fall/psets/2/pset2.html)

### Objectives
+ Become better acquainted with functions and libraries.
+ Dabble in cryptography.

### What I built
+ [initials.c](https://github.com/mkczarkowski/harvard-cs50/tree/master/pset2/initials.c), a program that, given a person’s name, prints a person’s initials, per the below.
```
$ ./initials
Regulus Arcturus Black
RAB
```
+ [caesar.c](https://github.com/mkczarkowski/harvard-cs50/tree/master/pset2/caesar.c), a program that encrypts messages using the [Caesar cipher](https://en.wikipedia.org/wiki/Caesar_cipher).
```
$ ./caesar 13
plaintext:  HELLO
ciphertext: URYYB
```
+ [vigenere.c](https://github.com/mkczarkowski/harvard-cs50/tree/master/pset2/vigenere.c), a program that encrypts messages using [Vigenère’s cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher), per the below.
```
$ ./vigenere ABC
plaintext:  HELLO
ciphertext: HFNLP
```