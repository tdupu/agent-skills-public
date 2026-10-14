---
name: test-skill
description: Use when testing an agent skill, router, pack manifest, trigger, output contract, or skill behavior against adversarial scenarios.
---

Read the testing contract and `superpowers:writing-skills` testing guidance.
Test in stages: no guidance to expose the natural failure, guided behavior to
verify the skill closes it, and refactor/loophole pressure to ensure it does
not merely satisfy keywords. Include correct routing, anti-trigger, bounded
scope, evidence, output shape, and cross-skill composition cases.

For packs, add manifest/catalogue/build/digest smoke checks. Preserve exact
prompts, selected routes, commands, outputs, and failures in a fixture outside
the published pack. Report rationalizations rather than hiding them.
