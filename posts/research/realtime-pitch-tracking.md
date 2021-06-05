Title: Real Time Pitch Tracking
Date: 2021-05-23 12:00
Category: Research
Tags: instrument building
Summary: Literature review while exploring pitch tracking algorithms suitable for realtime use in embedded contexts


## Notes

### Yin

I'm a long-time Yin user, but the algorithm seems to have some serious limitations 
for realtime use in an embedded enviroment:

- The algorithm is block-based and inherently latent
- The fast version of the algorithm requires an FFT on every block
- In my experiments the algorthm slows to a crawl with a large `tau_max`, so detecting pitches lower than ~70-80hz seems to have a pretty big impact on performance.

### Extended Complex Kalman Filter

[2017 dafx paper](https://ccrma.stanford.edu/~orchi/Documents/ekf_dafx_updated.pdf)

Das Orchisama, Chris Chafe and JOS to the rescue maybe?

- This algorithm is designed for low-latency real time use, and computes a pitch estimate on every *sample* instead of every frame like Yin.
- It still requires an FFT on every block, although there is a note about some mitigations in the paper...
- Seems to perform much better than Yin: much more stable and tracks fast moment more easily

### Bell Labs Hardware Implementation

[1976 IEEE paper: J Dubnowski, R Schafer, L Rabiner. Real-time digital hardware pitch detector](https://ieeexplore.ieee.org/abstract/document/1162765)

Is this something? They call this "high-quality" but that's in 1976. Maybe it's just a basic autocorrelation approach? (EG what Yin attempts to improve on...)

I'll have to track down access, I'm curious...

### MPM / Tartini

[200? paper: Philip McLeod & Geoff Wyvill. A Smarter Way To Find Pitch](https://www.cs.otago.ac.nz/tartini/A_Smarter_Way_to_Find_Pitch.pdf)

- The "clarity" param is interesting. 
- Also requires an FFT.
- Is optimized to use small block sizes though, so latency should be lower... but then you're doing that many more FFTs a second...

[The primary author's PhD thesis (1980) looks like a fantastic introduction to the literature (also discussions of wavelet analysis & LPC!)](https://www.cs.otago.ac.nz/students/postgrads/tartini/papers/Philip_McLeod_PhD.pdf)


## Reading Notes

### Comparison of Pitch Trackers for Real Time Guitar Effects

[2010 dafx paper](http://dafx10.iem.at/papers/VonDemKnesebeckZoelzer_DAFx10_P102.pdf)


