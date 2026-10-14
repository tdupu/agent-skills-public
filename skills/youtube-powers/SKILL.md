---
name: youtube-powers
description: >-
  Route a YouTube channel task to the skill that owns it - cutting raw takes
  into videos, burning annotations, writing and checking descriptions, fixing
  end screens - and know which step cannot be done from here at all. Use at the
  start of any work on a channel, before reaching for a specific skill.
---

# YouTube powers

A channel task is usually a chain: raw takes become a video, the video gets
annotations, the annotations get a description, the description gets checked,
and then somebody uploads. Each link has an owner. This routes to it.

## One link is not yours

**Uploading cannot be done from this machine**, and finding that out late has
cost real time. Two independent blocks, neither of which is a policy you can
ask to have lifted:

- **The Data API.** Google restricts `videos.insert` from unverified API
  projects created after 28 July 2020 to *permanently private*. Not unlisted,
  and not fixable by changing the setting afterwards - it needs a compliance
  audit. Pushing a finished video through the API puts it in the one state
  nobody can get it out of.
- **Browser automation.** A file input cannot be clicked (the native picker is
  invisible to the extension), and the upload tool takes at most 10 MB per
  call from paths already shared with the session. Lecture renders run 100 MB
  to 1 GB.

Load [[youtube-upload]] before doing anything about getting a video onto the
channel - including before reaching for `videos.insert` or opening Studio. The
upload itself is the human's, every time. Say so early, stage the files and
the metadata so it is drag-and-drop, and do everything on both sides of it.
The durable fix is getting the API project verified; until then this does not
change.

Nothing else on a channel is blocked. Titles, descriptions, tags, visibility
of existing videos, playlists and comments are all reachable through the API
once `bin/credentials.py` has a token.

## Where the work lives

| Task | Skill |
|---|---|
| Raw takes to one video: choosing, ordering, trimming, joining | [[assemble-recording-series]] |
| On-screen notes burned into the frame | [[youtube-color-commentary]] |
| Writing a description: summary, chapters, references, provenance | [[correct-youtube-description]] |
| Checking a description against the API's limits before it ships | [[check-youtube-description]] |
| End screens and cards pointing at the right next video | [[correct-youtube-cards]] |
| Getting a finished render onto the channel, and the handover it needs | [[youtube-upload]] |

A series is assembled before it is annotated, and annotated before its
descriptions are written: dead-air trimming moves every timestamp, and a title
card prepended afterwards moves them again. Chapters generated before either
are wrong.

## What burns, and what does not

Anything composited into the picture - annotations, title cards, corrections -
is permanent once rendered. Re-rendering costs the encode and, if the video is
already up, a re-upload that loses its publish date, view count and comments.
So the order is: show the text to whoever is accountable, run an adversarial
review over it, *then* render. A panel asserting the speaker made a mistake is
checked against the recording and the source before it ships; a false
correction burned into someone's lecture is the worst outcome available.

Descriptions, titles, tags and playlists are not like this. They are editable
forever, which is why detail that will not fit in a panel belongs in one.

## Before any of it

Read the channel's own operating notes if it has them - the constraints that
bit somebody already are written down there, not here. Render to new paths;
never overwrite a source take, an assembly, or a previous render.
