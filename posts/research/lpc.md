Title: Linear Predictive Coding
Date: 2021-04-10 12:00
Category: Research
Tags: lpc, synthesis
Summary: Linear Predictive Coding


## Overview

Linear predictive coding is a process of deriving the shape of a filter from a particle of sound that can be used to later reconstruct that particle by 
feeding either a pulse stream or white noise into a filter with the derived coefficients. It is typically used as a compression scheme for speech, because 
the pulse/noise into a filter roughly models the human vocal tract (pulse train -> filter) and associated sibilants et al (noise -> filter) fairly well.

[This is a very nice introduction to the topic by Hyung-Suk Kim.](https://ccrma.stanford.edu/~hskim08/lpc/)

To read: 

- [this lecture slide deck by Dan Ellis covers much of the same material with some more concrete examples in pseudocode and even a PD patch.](https://www.ee.columbia.edu/~dpwe/e4896/lectures/E4896-L06.pdf)
- [another lecture slide deck from Lawrence Rabiner at UCSB looks useful for comparative reading](https://web.ece.ucsb.edu/Faculty/Rabiner/ece259/digital%20speech%20processing%20course/lectures_new/Lecture%2013_winter_2012_6tp.pdf)
    - [Digital Speech Processing Course (winter 2015) homepage](https://web.ece.ucsb.edu/Faculty/Rabiner/ece259/)

## Available implementations

### Librosa

- [Documentation](https://librosa.org/doc/main/generated/librosa.lpc.html)
- Accepts filter order (`P` value) as a param, but doesn't expose any other configrable options for the analysis

### Soundpipe / OpenLPC / talkbox

- Here's [soundpipe's OpenLPC-based lpc module.](https://git.sr.ht/~pbatch/soundpipe/tree/master/item/modules/lpc.c)
- The soundpipe source has a copy of the [OpenLPC library code](https://git.sr.ht/~pbatch/soundpipe/tree/master/item/lib/openlpc/openlpc.c) as well.
- `P` and analysis block size are hard-coded into OpenLPC, but could be parameterized in a refactor...
- There's another LPC implementation in soundpipe! Paul points out the talkbox module also uses LPC, [the source looks very readable](https://git.sr.ht/~pbatch/soundpipe/tree/master/item/modules/talkbox.c#L53)

### Scikits / Talkbox

[Source code](https://github.com/cournape/talkbox/blob/master/scikits/talkbox/linpred/)

- Pure python reference implementation using scipy/numpy along with an optimized C version makes this a potentally great reference
- Source encourages using the implementation as a basis / reference for education
- At first glance this is the simplest & easiest to follow implementation I've seen so far...
- Apparantly uses `Levinson-Durbin recursion` to solve for coefficents. Haven't seen this approach mentioned before I don't think?
- Also accepts filter order as a param but otherwise isn't set up to be generally configurable
- [Example use](https://stackoverflow.com/questions/53081956/basic-linear-prediction-example)
- [Another example using it](https://stackoverflow.com/questions/25107806/estimate-formants-using-lpc-in-python)

### LPC Torch

- [Source code](https://github.com/TowardHumanizedInteraction/LPCTorch/blob/master/lpctorch/lpc.py)
- Apparantly inspired by the Librosa implementation
- Uses "Burg's methods" (see bibliography below for the paper cited)

### Ziki Chombo DSP

- [Source code](https://github.com/zikichombo/dsp/blob/master/lpc/t.go)
- Nice concise golang implementation
- Uses the autocorrelation method

### Carlos A. Rueda's *ecoz2* implementation

- [Source code](https://github.com/ecoz2/ecoz2/tree/master/src/lpc)
- Implementation revised from a BS thesis project


## Reading notes

### [Linear Predictive Coding is All-Pole Resonance Modeling](https://ccrma.stanford.edu/~hskim08/lpc/)

> Hyung-Suk, Kim. Linear Predictive Coding Is All-Pole Resonance Modeling, Center for Computer Research in Music and Acoustics, Stanford University, 4 Dec. 2020, ccrma.stanford.edu/~hskim08/lpc/. 

- LPC can be used for more than just voice synthesis. (Cross-synthesis is mentioned specifically, but obviously the Lansky string synthesis experiements are another example...)
- A pulse train models the pitched sounds in the `source -> filter -> output` LPC pipeline, and white noise models unpitched sounds. Already that makes me want to try using a spectrally rich & dynamic sound source like a binaural rain recording with a sampled line noise hum or something...
- Uses a `p-th order` all-pole filter. I think this is a special case of an IIR filter but I'm going to have to read more about this...
- Basic idea is to combine a spectrally flat source signal with a resonant filter, so playing with "wrong" versions of both of those components might be interesting...
- Each pole in the filter corresponds to a delay in the signal, so we need to track at least P samples in the filter computation. 

Probably wrong python translation of the first math block in section 3:

``` python
p = 10
a = [0] * p # should be filled with coefficients?
o = [0] * p 
for i in range(numsamples):
    for j in range(1, p+1):
        o[j] = 1.0 / (a[j] * math.pow(i, -j))
```

- The process of finding the coefficients for each pole in the filter is called *auto-regression*. "Finding the future value of itself from the past."

Alright the matrix transformation stuff in section 4 is too math for me. It seems like the basic idea is that the block of P coefficients 
needs to be computed for every sample though. The end of the section says the process is the same as a *linear regression*, so some future 
comparative reading on that topic might help clarify this part. 

The final equation form looks very simple but I don't know how to translate it:

> a = (A<sup>1</sup> A)<sup>-1</sup> A<sup>T</sup> b

Apparantly this part:

> (A<sup>1</sup> A)<sup>-1</sup> A<sup>T</sup>

Is known as the [*Moore-Penrose pseudoinverse*](https://en.wikipedia.org/wiki/Moore%E2%80%93Penrose_inverse) so there's some nice 
jargon-salt to add to this wound.

Anyway, this is apparantly the way to compute the coefficients `A`.

Next in the recipe is to extract the *residuals* using `A` -- this process is also unclear to me but seems to involve at least these additional steps per block:

1) Determine if the current block of samples is pitched & get a pitch contour if so (I can let aubio handle this for me)
2) In either case determine the "power of the source signal" -- so, what is this the spectral magnitude? It's described here as a *variance* which is also clear as mud to me.

Three formants are apparantly enough (6 poles or `p=6`) for voice synthesis, so playing with `p` could also be interesting...

Here we repeat the process using the usual overlap-add, though I'm curious to read more about older approaches. For example IIRC Lansky doesn't use any windowing in his implementation.

[...and after all this there's a brief mention of a faster way to go about this that uses the FFT instead.](https://en.wikipedia.org/wiki/Autoregressive_model#Yule.E2.80.93Walker_equations)

The examples here (and every LPC usage I've seen so far) use pretty small block sizes, so I assume the smaller the block the less advantage to doing the computation as an FFT but who knows. 
Here Kim is using a blocksize of 240 samples, Lansky was using 250 sample blocks in the 80s, and even Charles Dodge used a block size of 125 samples for *In Celebration*. (See: _Composers & The Computer_ ed. by Curtis Roads)

OK, so: decoding. 

Doing the analysis process with `p=6` leaves us with 6 coefficient values (for `A`) and one *variance* value (which I still don't really get) for every block.

This is the fun part -- to synthesize this again, we can feed either white noise or a pulse train into a filter using the given coefficients (using the value of 
the *variance* somehow to decide if it should be the pulse train -- pitched -- or white noise -- unpitched) and get a full block of "resynthesized" sound to 
overlap-add into an output signal.

> Aside: so is this standard for math notation? A lowercase *a<sub>k</sub>* means the value in collection `a` at index `k` or `a[k]`... 
> and the uppercase `A` refers to the entire collection (array) as a single unit? Math notation still confuses me.


Cross-synthesis!

This is one thing I really want to play with. A low-overhead cross-synthesis via LPC would be a very nice little tool to add to the collection. 

The idea is pretty simple: instead of doing the analysis step once for one sound, do it twice for two sounds, one being the pitch source and the other 
being the noise source. So we do basically everything else the same, except in the end each analysis block produces P values for the filter which are 
derived from the pitch source, and 1 value for the *variance* (which I get represents the pitched/unpitched state of the signal but I don't follow exactly 
how to derive it right now) which is derived from the noise source. Taking these franken-blocks and resynthesizing a new signal from them will give us 
the pitched content from one sound with the sibilance/noise from the other. That's a neat way to do cross-synthesis!

Finally, the closing section has some good thoughts:

- LPC will have different effects on different signals -- sources that are already suited for being split into pitch & noise components easily (monophonic sounds) will have the most predictable results. Of course I'm curious to throw dense garbage at it too. :)
- There is something called [CELP](https://en.wikipedia.org/wiki/Code-excited_linear_prediction) which uses something called *excitation codes* to improve sound quality.
- LPC is constrainted by blocksize and won't reproduce sounds with lots of fast transients very accurately. (Of course I'm not really interested in LPC for accuracy so that's no biggie!)
- There are some other approaches that try to compensate for the transient smearing... maybe worth checking out. TFLPC & CTFLP.

The core LPC model is understandable enough that it should be possible to fuck with many aspects of it and hopefully find some nice edges.


### Synthesis of Timbral Families by Warped Linear Prediction.

> Lansky, P., and Steiglitz, K. 1981. "Synthesis of Timbral Families by Warped Linear Prediction." Computer Music Journal 5(3), 45-49.

Warped linear prediction tries to make use of LPC resynthesis to derive similar-sounding but distinct families of instruments from a single 
analysis source. Paul Lansky's _Pine Ridge_ from the album _Folk Images_ is a beautiful example and also the specific piece discussed in this paper:

<audio src="{static}/sounds/lansky-pine-ridge.mp3" controls></audio>

*__PS:__ This lovely 1995 album of computer music and more is [still available to purchase from Bridge Records](https://bridgerecords.com/products/9060).
Lansky has also posted [liner notes for the album](https://paul.mycpanel.princeton.edu/liner_notes/folkimages.html) to his website.*

> Aside: An earlier interview with Richard Moore in the CMJ collection I'm reading from (_The Music Machine_ ed. Roads) mentions that Kenneth Steiglitz 
> wrote the fortran library that Paul Lansky used for his LPC-based work, at least initially. I wonder if that library is available somewhere still... 
> he is also the author of [one of the most readable books on DSP in my opinion.](https://www.doverpublications.com/0486845834/0486845834.pdf)

OK, more filter jargon right off the bat. They mention using a transfer function of `1/D(z)` for the filter. I don't remember what that means. :)

*Update*: talking a bit with J, he says it's a shorthand for describing the essential math routine for given filter -- the filter kernel maybe? 
Not totally sure, but that seems to track...

In any case, the general approach to the LPC procedure described so far seems to match what I read in the Kim, in this case though the idea is to 
use a corpus of recorded notes as the basis of an instrumental family to be able to synthesize variations from the original by means of:

- mutating the filter coefficients extracted during the normal analysis phase.
- shifting the pitch curves extracted during the normal analysis phase to arbitrary frequency bases

The input for _Pine Ridge_ was an 11 second long phrase played by violinist Cyrus Stevens. I'm assuming they did manual segmentation to 
split the sound into logical "note sections" but I don't remember if that's discussed further... I also don't remember if there is much discussion 
about how Lansky approached managing that corpus of notes during the composition phase...

Anyway, in this case the particular flavor of LPC being used employs the *covariance method* and they say they don't window the blocks during analysis, 
though they still overlap by 50% in the normal overlap-add fashion...

*Interlude*

So, as an aside, there appear to be two basic approaches to LPC...

- the autocorrelation method
- the covariance method

*Update*: nope! there are others... "A new autoregressive spectrum analysis algorithm" by L. Marple apparantly describes "Burg's method".

Lansky & Steiglitz say they use the covariance method with no windowing. This method is "well known" to produce unstable frames 
which they compensate for by adding the last half of the previous frame to the first half of the next.

In other words:

    <imagine each digit is 1/4 the block size>

    1234 5678

    1234 3456 5678 7800

(The zero padding is an assumption! Not sure how they're handling the final block...)

They say the covariance method is also well known for producing unstable filter frames... to compensate they check each 
filter coefficient to see if the pole has a radius greater than 0.998, and move it to 0.998 if so... 

I'm confused by that, it seems to imply they're using an FFT-based approach if they are able to convert the coefficient frequences into polar form?

I'm still also confused as to why this approach doesn't need to do any windowing!

## To read

### Dodge

I should re-read Charles Dodge's chapter on _In Celebration_ from the Roads book _Composers & the Computer_ which was my introduction to LPC...

### The "Burg" method

LPCTorch uses this.

- L. Marple, "A new autoregressive spectrum analysis algorithm," in IEEE Transactions on Acoustics, Speech, and Signal Processing, vol. 28, no. 4, pp. 441-454, August 1980, doi: 10.1109/TASSP.1980.1163429.

### More resources from the [Computer Music Journal bibliography](http://www.computermusicjournal.org/bibliography/index.html)

- Atal, B.S., and S.L. Hanauer. 1971. "Speech Analysis and Synthesis by Linear Prediction of the Speech Wave." Journal of the Acoustical Society of America 50: 637-655.
- Chowning, J. 1980. "Computer synthesis of the singing voice." In Sound Generation in Winds, String, Computers, compiled by Johan Sundberg, Stockholm: Royal Institute of Technology.
- Fant, G. 1959. "The Acoustics of Speech." Proceedings of the Third International Congress on Acoustics, 188-201. Reprinted in Speech Synthesis, J. L. Flanagan and L. R. Rabiner (eds.). Stroudsburg, Pa.: Dowden, Hutchison, and Ross, 77-90.
- Fant, G. 1960. Acoustic Theory of Speech Production. The Hague: Mouton.
- Makhoul, J. 1975. "Linear Prediction: A tutorial review." Proceedings of the IEEE 63: 561-580.
- Makhoul, J. 1977. "Stable and Efficient Lattice Methods for Linear Prediction." Institute of Electrical and Electronics Engineers Transactions of Acoustics, Speech, and Signal Processing", ASSP-25(5), 423-428.
- Markel, J. D., and A. H. Gray Jr. 1976. Linear Prediction of Speech. New York: Springer.
- Mattingly, I. 1968. "Synthesis by Rule of General American English." Doctoral disseration. Yale University, 133.
- Olive, J. 1971. "Automatic Formant Tracking in a Newton-Raphson Technique." Journal of the Acoustical Society of America, 50(2), 661-670.
- Peterson, G. E. and Barney, H. L. 1952. "Control Methods Used in a Study of Vowels." Journal of the Acoustical Society of America, 24(2), 175-184.
- Rabiner, L. R. and Schafer, R. W. 1978. Digital Signal Processing of Speech Signals. Englewood Cliffs, N.J.: Prentice-Hall, 38-106.
- Rabiner, L. R. 1968. "Digital Formant Synthesizer for Speech Synthesis Studies" Journal of the Acoustical Society of America, 43, 822-828. Reprinted in Speech Synthesis, J. L. Flanagan and L. R. Rabiner (eds.). Stroudsburg, Pa.: Dowden, Hutchison, and Ross, 255-261.
- Sundberg, J. 1977. "The Acoustics of the Singing Voice" Scientific American, 236(3), 82-91. 


