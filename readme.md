
# WorldGPT
___
## What is this?
It's a tool for use with large language models to generate dynamic content based on a character concept.
The server component exposes a few APIs for use in generating characters and content.

You may supply text or audio (which will be transcribed to text), which a Language model can be supplied with alongside
character information and world information. The language model generates a response on behalf of your character, which
is then sent to a Text synthesis tool for generation. Finally, the audio is returned. ]

     User Audio/Text > Language Model > Voice Synthesis > Better UX

#### That sounds slow
This workflow usually takes about 3-8 seconds, depending on a number of factors like network latency, number of tokens 
supplied to the language model and how long the response was.

This is just a bit of a proof-of-concept, to see if it's actually possible to make this work in a reasonable timeframe 
for video games.
___

### Why not use any of the other GPT mods or plugins already out there?
*Short answer is you probably should.* 

It's reasonably similar to some other implementations of Language-model-assisted Character content generation, but where
I'm trying to be a little different is building a server-client architecture. Several of the other mods and tools I've
seen are really cool, but they're for that specific game, or it's a mod that's for that game only. 

The examples some of these mods or tech demos have provided have usually been cherry-picked or have the character in the
game starting their interaction with 

```
"I'm an AI language model and I'm pretending to be a monk."
```

I don't need to be convinced that it's awesome, but I'd like to 
give fixing some of those issues a go.

If it's designed as server-client, the server can handle the transcription, storage of persistent data and provide a
middle-man api that can be customised to point to different tooling. the client (or mod, plugin, browser, DM) just has 
to format the data in a fairly simple and easy to use way.

#todo example usage.