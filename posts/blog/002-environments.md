Title: Synthesizing Environments
Date: 2018-11-25 20:00
Category: Research
Tags: development, research, analysis, synthesis
Summary: Sortable field recording databases via automated feature extraction and multidimensional parameter space traversal


While the musical cues for this project are implemented as sets of generative scripts, another 
component for the audio side of things I have been working on is based around the idea of a 
synthetic environment. Inspired by other hyperreal field recording projects like Luc Ferrari's 
Presque Rien series, Michael Pisaro's July Mountain or Francis Dhomont's Signe Dionysos which 
(more or less) don't immediately reveal themselves as synthetic environments even though they might be 
composed of impossible or at least unlikely components. (How did that train get inside the 
frog pond??) 

In 2016 I started collecting field recordings in multiples to use in constructing new 
synthetic environments -- each one based on a real environment. I only have two so far: ~30 hours of 
recordings on my porch made at the same time each day for a month, and a handful of recordings of muffin 
baking in my kitchen. I started cataloging interesting moments in the recordings in a notebook -- at 
23 seconds a short bird chirp, 32 seconds a distant metallic clang, etc. It was a great way 
to spend a few days; field recordings cranked up on the stereo just listening and writing, but after 
doing about 5 hours worth I realized I really needed to automate the process somehow.

Last year I finally picked up a machine learning book, hoping to be able to train an algorithm on 
the recordings and have it classify them based on low level features extracted from 
the audio. The classic example of this is a dataset of Iris petal/sepal lengths & widths used to 
predict the species. Given a fixed set of labels (one per species) a collection of measurements can 
be used to predict which species it best matches. This is basically what I was looking for, but 
would require a training dataset with human-provided labels to learn from. 
Rather than try to do a supervised process where I'd take my original notebooks and use them to come 
up with the labels for the classifier (this is a bird, this is a car engine, this is a distant metallic rattle...) 
it seemed more interesting (and probably less tedious) to take an unsupervised approach and try to have 
the algorithm infer classifications and groups from the data itself. 

I decided to start by focusing on the spectral centroid of these recordings because of [this really 
cool study by Beau Sievers et al](https://psyarxiv.com/wucs4/) on the correlation between emotional arousal and the spectral centroid.
The spectral centroid is the mean frequency in a set of frequencies -- a sound with lots of high frequency 
energy and low frequency energy could have a centroid somewhere in the middle of the spectrum, while 
a pure sinewave at 200hz would have a spectral centroid of 200hz.

An initial experiment doing analysis on fixed-length overlapping grains didn't go very far. 
I segmented the field recordings into small overlapping grains, found the spectral centroid for each 
grain, and then reconstructed the sound by shuffling the grains around so they would go in order of 
highest spectral centroid to lowest. Instead of the smooth sweep from high-energy sounds to low-energy sounds 
that I imagined, the result was basically noise. I was bummed out and left things there.

The wonderful folks at [Starling](https://starling.space) are working on a cool project that involves doing 
analysis on a set of field recordings of train whistles. On Monday I had a long conversation about their process so far 
and the analysis approaches they'd been trying. It got me excited to pick up on this project again and find a better 
approach to segmenting the field recordings for analysis -- instead of just cutting them into fixed 
sized grains which seemed to produce mush. 

This weekend I updated the script I was working with to do segmentation using the `aubio` library's onset detection, breaking the 
field recordings up into segments between onsets instead of arbitrary fixed-length slices. The script does an analysis pass on each 
sound file (usually about an hour of audio or so per file) -- finding segments, doing feature extraction (spectral centroid, flatness, 
contrast, bandwidth and rolloff) on each segment and storing the results in an sqlite3 database to use for later processing.

That's pretty much as far as I got this weekend! Doing one pass of analysis on the entire dataset takes about 3 hours so the only 
tuning to the analysis stage I've done so far is to low pass the audio before doing analysis (at 80hz) which I hope compensates a bit for 
all the low wind noise rumbling in the porch recordings.

Below is a new test reconstruction, doing the same type of sorting on the spectral centroid -- highest to lowest -- but placing each segment on an 
equally spaced 10ms grid, cutting down any segments longer than 1 second, then applying a little amplitude envelope (3ms taper plus a hanning 
fadeout) and stopping after accumulating 5 minutes of output. (Which means this places roughly 30,000 variable-sized overlapping audio segments at 10ms intervals 
in order of highest spectral centroid to lowest in the space of 5 minutes.) 

Segmenting the sounds based on onset detection is already producing way more interesting results! I'm looking forward to 
studying the data and tuning the approach -- and, one day trying to wrap my head around the machine learning component of this to do 
unsupervised classification of the sounds into a 2d space, so instead of simply moving from highest to lowest across a single feature 
dimension (the centroid) I can play with moving through a parameter space that hopefully has a meaningful correlation to the content of each 
sound segment. I love the idea of being able to move slowly from the region of the birds into the region of the revving of the car engines and so on.

Taking this approach it would be possible to match environments to locations in a story, and move through the environment's sound-space in some 
meaningful-sounding way that correlates to the generative action in the story. If Pippi is at home in Villa Villakula and is visited by an annoying 
fancy gentleman, the environment could shift positions in the parameter space along with the mood of the characters or the intensity of the action etc --
and allowing for that to be controlled by an automated process would let the environment change with the story even though the story itself may be indeterminate.

Anyway, here's the most recent test render from this afternoon -- things begin in muffin-baking world and slide off into the sound-world of my porch pretty fast. 
The church bells really start to clang by the end!

<audio src="{static}/sounds/sorted-10ms-lpf.mp3" controls></audio>

