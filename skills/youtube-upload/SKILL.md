---
name: youtube-upload
description: >-
  Get a finished video onto the channel, and all the work either side of the
  human step. Use when a render is ready, when asked to upload or re-upload
  unlisted, or before reaching for videos.insert or Studio.
---

# Putting a video on the channel

**The upload is not yours.** `videos.insert` from an unverified project - this
one - makes a video **permanently private** until a compliance audit: it can
never be unlisted. Studio is no better; its file field opens the native OS
picker, which no extension can see, and the browser upload tool caps at 10 MB
per call against 100 MB-1 GB renders. A human uploads, by hand.

## Before the handover

1. Confirm the render: duration, dimensions, and **a decoded frame, looked
   at**: right-side-up, not mirrored. Rotation is not in the file and does not
   track resolution; the discarded upside-down batch passed both.
2. Title: match the series exactly, capitalisation included. The card tooling
   parses only `part 3` (134 of 383), `- 14.1 -` and `pt. 4`, the channel's
   own; `3/5` and `(3/8)` are invisible to it and strand the video on an
   adjacency guess.
3. Description via `correct-youtube-description`, then
   `check-youtube-description`; if three passes do not clear it, report rather
   than loop. Chapters come from the final file, after any title card - a card
   shifts every timestamp.
4. Staging sheet: a committed markdown file at the repo root
   (`UPLOAD-SHEET.md`): why the upload is theirs, the batch visibility, a row
   per video in upload order (title, absolute render path, description file),
   and any file that must NOT be uploaded.
5. Hand over the sheet and stop. Do not offer to drive Studio or write an
   uploader.

## Replacing a video

Never two public videos under one title: upload the new one **Private**; record
`<old>|<new>` in `data/archive/id-map.psv`, which the retire step refuses
without; then retire the old and confirm; only then set the new one to the
batch visibility.

## After the handover

You need the IDs back; nothing downstream works. Check each with
`videos.list(part=status)`: `privacyStatus: private` where you asked for
unlisted means it went through the API after all - no flag flip fixes it. Then
by API: descriptions (`correct-youtube-description`); record the IDs where the
channel keeps them.

End screens and cards are a **second** human handover - no API resource exists.
`correct-youtube-cards` writes a worksheet for a person to apply in Studio;
stage and hand it over like the sheet.

## If the constraint has changed

Only the YouTube API Services compliance audit lifts the restriction, not OAuth
consent-screen verification; a report of an audit is not evidence. Ask for the
audit status on that project's screen in Cloud Console and say which you rely
on: approved there, uploads come out as you set them; anything else (in
review, not requested, not found, consent screen only) is permanently private -
hand over. The operations doc has the project's creation date; none was audited
before it existed. Never settle it by uploading.
