Title: Some Random Numbers in Python
Date: 2020-12-22 20:00
Category: Research
Tags: research, pippi, data, probability
Summary: Plotting some random choices in python
Tangle: True
Status: draft


This article isn't really about python. It's not really about 
random numbers either -- especially not about their applications 
in cryptographic contexts. This article is about _using_ random 
within the context of a larger compositional scheme with freedom 
and confidence. You're a real composer too, even though you let that
that random number call the shots just now. 


If you know me, you've probably heard me get on my soapbox about how 
in the world of generative art simple algorithms often produce more 
interesting outputs than terribly or clever alogrithms, and 
that working with random number generators is perfectly useful 
and good and not bad or scary or wrong at all. It may seem strange 
to emphasize that last point, but random numbers have a surprisingly bad 
reputation in generative art circles. If you can come away from this 
with a couple new things to think about, and a cool thumbs-up attitude 
towards using these random number tools in your work, I'll be quite happy! 
I'll try to demonstrate how random numbers can be so useful and also why 
you don't need to do much anything fancy with them to get a lot of benifet 
from them.

I'm not going to describe anything clever, just some basic approaches 
to working with random number generators that I find generally useful 
and interesting. Every example will be implementated in my python computer 
music system called pippi, where I use them the most, but the ideas can 
be implemented in pretty much any system or language with a random number 
generator and some math library functions. I don't use all of these approaches
all the time, but I do use some of them quite a lot of the time. I'll try to 
point out which those are, and I'm also excited to dig up some personally overlooked 
techniques by writing through this all, so I'll try to point those out too.

Lets start with using a _normal_ or _uniform_ random distribution. This is 
the random distribution you're probably already most comfortable working with: 
white noise, with energy spread nearly equally across the frequency spectrum.

When people talk about the _distribution_ of a random number producer, 
all they're talking about is sampling its output for a while and then 
making a graph of those outputs, sorted. For a descrete system (where 
there aren't any answers in between the steps) this is essentially a 
histogram of the random number generator's production within some range.

A white noise, normal run-of-the-mill plane jane random distribtion will just 
look basically like a straight line. Each value is roughly as probable as 
any other to be chosen.

![Fig 1: A normal random disribution](/img/01-normaldistribution.png)

Above I ran a standard random number generator 10,000 times, sorted the 
outputs and we get basically a straight line going from 0 to 1 at a rate 
of about 1/1.

As I said, this is showing every value produced in that run of 100,000 values. 
The line is quite flat, showing that each value between 0 and 1 has nearly the 
same weight -- in other words, nearly the same probability that it will be chosen.

There are quite a lot of possible values between 0 and 1 in a 64 bit system.

> _In the meantime_, consider the shape of the graph of the normal distribution, 
> and try to imagine how you might go about changing that in practice, without 
> rewriting the C standard library to alter the `rand()` function itself.  Ultimately 
> C's `rand()` is what pippi uses for random number generation. For musical purposes, 
> it's mighty fine albeit a tad clunky in the API area. Just don't use it in your new 
> privacy application to generate random secrets. Pippi does hide the clunky parts but 
> it *does* expect you to seed the random number generator with some number.

- Laurie Spiegel cite
- Gregory Taylor on randomness
- Eugene (list) on randomness?
- Cage & the gamut

## Random Walks

## Monte Carlo

## Gamuts

## Procedures

## Ranged sequences


