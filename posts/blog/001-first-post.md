Title: South Seas Development So Far
Date: 2018-11-18 20:00
Category: Development
Tags: development
Summary: A summary of development so far


*South Seas* is an interactive retelling of a Pippi Longstocking story by Astrid Lindgren. This blog is a journal of its development.

I'm still working out the final form of the project. I'm aiming for something somewhere between a role playing game, drum circle, 
campfire story, and a movie. I guess.

The web version of this project is a combination of python, SVG with CSS animations, and a bit o'javascript with a redis backend.

In this first post, I'll describe the basic architecture of the website portion of the project. (It's the core of the project.)

Here is a simplified diagram of the processes running on the `southseas.fun` server.

![A diagram of processes running on the webserver](/images/webarch.jpg)

Sounds are structured in the code as cues -- python scripts that use my `pippi` computer music library -- and the `RENDERER` process 
keeps a queue filled for each musical cue. Yes, cue queues. The renderer process is actually quite a number of processes. Each cue gets its own process 
which has main loop that checks the (estimated) size of the queue for the given cue. If the queue is full, it waits a second and then checks the 
size again. If the queue is not full, the primary cue renderer process will tell a pool of render processes to do the actual rendering work, and they 
will push the new renders onto the appropriate queue. Each cue has its own pool of worker processes that actually run the python scripts that constitute the 
cues, use the wonderful `sox` program to encode them as mp3 files, and then convert those files into base64-encoded strings suitable for stuffing into the 
`src` attribute of an html `audio` tag as a data-URI. Those `audio`-tag-ready strings are what is actually pushed into the redis queue.

The conductor process orchestrates switching between sections -- just a slug value stored in redis -- by way of a main loop that has a few different behaviors.
If the timer is enabled (again this is just a flag in the redis db, checked periodically by the conductor) then the conductor keeps track of the (approx) elapsed time 
the current section has been set. There is a hard-coded lookup table that maps sections to lengths in seconds. If the elapsed time has exceeded the length for the 
current section, the conductor looks into another hard-coded table that defines the order of sections to see which section is next, and switches to that section. 
It also broadcasts a message to all connected clients to tell them that the section has changed. If there is a title card associated with that section, it sends 
another broadcast message with that info. (Again stored just as a fixed value in a lookup table.)  If there is a voiceover cue associated with that section 
(another lookup table -- mapping to a special cue script) it will broadcast the playback of that cue to all clients.

When the conductor reaches the end of the list of sections, if looping is enabled, it will return to the start of the section list.

Looping may be disabled, and the timer may be disabled, to pause on a section, or allow messages from the `CONSOLE` process to flip to an arbitrary section. 
Mostly that's just to make development easier, and be able to hang out on one section while I test it out.

There are a number of `spink` playback processes watching the value of `current_section` in redis. Each process represents a unique channel -- there are 12 
in total now. When the section changes, the `spink` creates a new playback process for each musical cue associated with that section. A section can have any number of 
musical cues associated with it. Each musical cue is a python script that defines a `play` function which returns a tuple containing a delay time and sound data. 
(Recall the `play` functions in these cue scripts are only actually executed by the `RENDERER` when the cue queue is below some threshold.)
Each playback process pops a fresh render off the render queue, which is bundled with a delay time. The process broadcasts the sound to every client listening on this 
channel, and then sleeps for the given delay time.

The result is that each channel gets pushed a unique render and delay time for each cue.

I'll describe what happens in the client (a web browser on a laptop or a phone or something) in a future blog post.

Finally, there is a simple curses `INFO` client which I just leave running in a tmux session on the server (along with the `CONSOLE` command client and a tail of 
the system log) which displays a count of the number of currently connected clients per channel, the name of the current section, the elapsed time in that section, whether looping 
is set in the conductor, if the timer is running, etc.

I suppose that just leaves the `WEBSERVER-WORKER` processes listed in the diagram -- these are just simple `flask` endpoints which can subscribe to 
the redis broadcast channels via server-sent-events, and which deliver the various templates -- the outer frame for the page & the inner section templates -- as well 
as SVG templates, etc. All the requests from the clients pass through these flask controllers.

I'll describe the HTML/CSS/SVG frontend in more detail in a later post.
