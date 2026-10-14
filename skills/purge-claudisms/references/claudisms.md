# Claudisms

Dated list of machine tells for `purge-claudisms`. Columns: `id | pattern | type | why it reads as machine | replacement | regex | source | added`.
`type` is lexical, syntactic, structural or rhetorical; `scan_claudisms.py` exits 1 on any lexical or structural hit and reports the rest as WARN.
`regex` is Python `re`, case-insensitive, per line after LaTeX comments are stripped; a literal backslash is written `\x5c` (so `\x5cemph` matches `\emph`); `builtin:<name>` names a paragraph-level check in the script; empty means judgment only.
A `|` inside a regex is written `\|`. Never delete a row: set `type` to `retired` and add the date to `added` (e.g. `2026-10-12; retired 2027-01-01`).
Monthly maintenance: on the first of each month, search for new entries (see SKILL.md) and append rows with that date.

Sources: WP = Wikipedia:Signs_of_AI_writing (WP:AISIGNS, read 2026-10-12); KOB = Kobak, González-Márquez, Horvát, Lause, *Delving into LLM-assisted writing in biomedical publications through excess vocabulary*, Science Advances 11(27), 2025, doi:10.1126/sciadv.adt3813; PA = plusai.com, The most overused ChatGPT words; WF = willfrancis.com, How to stop Claude writing like an AI; AW = alexanderweichart.de anti-ai-writing reference; PCW = PCWorld, Does my writing sound like AI? Claude has thoughts (2026); AIC = aicheckr.io, AI slop examples; SS = skills.sh stop-slop; AIB = The AI-isms of Writing Bible (Google doc); LL = laskenlog.substack.com, False profundity (on the 2026 New Yorker piece); TSK = tropes/style guides surfaced by search (negative listing, rhetorical Q&A, dramatic countdown); OWC = onlinewritingclub.com, 18 signs; CL = claudemarket/skills.sh per-model overuse tables (Opus 4.5: comprehensive, nuanced, paradigm, robust; semicolons 3x); LI = LinkedIn anti-slop prompt lists; RS = recurring across several of the above; S9/S11 = Grants/GRANT-STYLE.md; P2/P4/P5/P12 = using-pdpowers PD-POLICY; AI18 = latex-ai-statement; LXP = using-latexpowers 'process belongs to the disclosure section'; CP = check-paragraph machine-tells line; PI = PI instruction, 2026-10-12; MATH = observed in the PI's 2026 drafts by the agent, 2026-10-12.

## General claudisms

| id | pattern | type | why it reads as machine | replacement | regex | source | added |
|---|---|---|---|---|---|---|---|
| C001 | delve / delve into | lexical | The canonical LLM word; 25x excess in 2024 PubMed abstracts. | look at, study, examine, or just state the thing | `\bdelv(e\|es\|ed\|ing)\b` | WP; KOB; PA | 2026-10-12 |
| C002 | tapestry | lexical | Decorative metaphor LLMs reach for; no mathematical or factual content. | name the components | `\btapestr(y\|ies)\b` | WP; PA; AIB | 2026-10-12 |
| C003 | testament (to) | lexical | Puffery: 'a testament to' inflates a fact into praise. | state the fact; drop the praise | `\btestament\b` | WP; PA; AW | 2026-10-12 |
| C004 | crucial / crucially | lexical | Importance-marker; tells the reader to care instead of showing why. | delete, or give the consequence in the same sentence | `\bcrucial(ly)?\b` | WP; KOB; SS | 2026-10-12 |
| C005 | pivotal | lexical | Importance-marker; 'pivotal role/moment' is stock LLM praise. | say what changed because of it | `\bpivotal\b` | WP; KOB; PA | 2026-10-12 |
| C006 | multifaceted | lexical | Vague complexity claim. | list the facets, or cut | `\bmultifaceted\b` | WP; PA | 2026-10-12 |
| C007 | leverage (verb) | lexical | Business-speak verb LLMs default to. | use | `\bleverag(e\|es\|ed\|ing)\b` | WP; AW; S9 | 2026-10-12 |
| C008 | seamless / seamlessly | lexical | Marketing adjective; unfalsifiable. | say what does not break, or cut | `\bseamless(ly)?\b` | WF; AW | 2026-10-12 |
| C009 | foster / fostering | lexical | Abstract causation verb. | name the mechanism: trains, funds, produces | `\bfoster(s\|ed\|ing)?\b` | WP | 2026-10-12 |
| C010 | realm | lexical | Grandiose synonym for area/field. | field, area, or the specific subject | `\brealm\b` | PA; KOB | 2026-10-12 |
| C011 | embark (on) | lexical | Journey metaphor for 'start'. | start, begin | `\bembark(s\|ed\|ing)?\b` | PA | 2026-10-12 |
| C012 | journey (figurative) | lexical | Journey metaphor for a process or career. | the process, the project, the years | `\bjourney\b` | PA; AIC | 2026-10-12 |
| C013 | intricate / intricacies | lexical | Vague complexity adjective. | say what is complicated and why | `\bintrica(te\|cies\|cy)\b` | WP; KOB; PA | 2026-10-12 |
| C014 | meticulous / meticulously | lexical | Self-praise of care; unverifiable. | state the check that was done | `\bmeticulous(ly)?\b` | WP; KOB | 2026-10-12 |
| C015 | vibrant | lexical | Travel-brochure adjective. | cut, or give the number | `\bvibrant\b` | WP; PA | 2026-10-12 |
| C016 | comprehensive | lexical | Claims completeness without a scope. | give the scope: all N cases, every curve of conductor < X | `\bcomprehensive(ly)?\b` | PA; CL | 2026-10-12 |
| C017 | ensure / ensuring | lexical | Guarantee verb attached to plans; superficial '-ing' tail. | the plan does X; the check catches Y | `\bensur(e\|es\|ed\|ing)\b` | WP | 2026-10-12 |
| C018 | showcase / showcasing | lexical | Promotional verb; 9x excess in PubMed 2024. | show, give, list | `\bshowcas(e\|es\|ed\|ing)\b` | WP; KOB | 2026-10-12 |
| C019 | underscore(s) (verb) | lexical | Importance verb; 9x excess in PubMed 2024. | delete the sentence or state the consequence | `\bunderscor(e\|es\|ed\|ing)\b` | WP; KOB | 2026-10-12 |
| C020 | landscape (figurative) | lexical | 'The landscape of X' names nothing. | the field, the literature, the known cases | `\blandscape\b` | WP; PA; AIC | 2026-10-12 |
| C021 | navigate (figurative) | lexical | 'Navigate the complexities' is a stock phrase. | handle, work through, or name the step | `\bnavigat(e\|es\|ed\|ing)\b` | PA; SS | 2026-10-12 |
| C022 | robust | lexical | Unqualified strength claim. | say what it withstands | `\brobust(ly\|ness)?\b` | WF; CL; S9 | 2026-10-12 |
| C023 | nuanced | lexical | Claims subtlety instead of showing it. | state the distinction | `\bnuanced?\b` | CL | 2026-10-12 |
| C024 | arguably | lexical | Hedge that avoids committing. | commit or cut | `\barguably\b` | PA | 2026-10-12 |
| C025 | notably | lexical | Emphasis adverb; usually the sentence is already notable or is not. | cut | `\bnotably\b` | PA; AW | 2026-10-12 |
| C026 | moreover | lexical | Formal connective chained by LLMs. | cut; or 'and', 'also' | `\bmoreover\b` | PA; AW; AIC | 2026-10-12 |
| C027 | furthermore | lexical | Same. | cut | `\bfurthermore\b` | AW; AIC | 2026-10-12 |
| C028 | additionally (sentence opener) | lexical | GPT-4-era connective. | cut; 'also' | `^\s*additionally\b\|\.\s+additionally\b` | WP | 2026-10-12 |
| C029 | interplay | lexical | Abstract relation word. | name the relation | `\binterplay\b` | WP | 2026-10-12 |
| C030 | garner | lexical | Stock verb for 'receive/get'. | receive, get, attract | `\bgarner(s\|ed\|ing)?\b` | WP | 2026-10-12 |
| C031 | bolster(ed) | lexical | Stock verb for 'support'. | support, strengthen, or give the evidence | `\bbolster(s\|ed\|ing)?\b` | WP | 2026-10-12 |
| C032 | enduring | lexical | Legacy adjective. | cut, or date it | `\benduring\b` | WP | 2026-10-12 |
| C033 | boasts (a) | lexical | Copula avoidance with promotional tone. | has | `\bboast(s\|ed\|ing)?\b` | WP | 2026-10-12 |
| C034 | harness | lexical | Stock verb for 'use'. | use | `\bharness(es\|ed\|ing)? (the\|its\|their\|this\|these\|those\|new\|modern\|AI\|LLM)\b` | RS | 2026-10-12 |
| C035 | unlock | lexical | Marketing verb. | allow, give, compute | `\bunlock(s\|ed\|ing)?\b` | RS | 2026-10-12 |
| C036 | elevate | lexical | Marketing verb. | improve, raise, or say how | `\belevat(e\|es\|ed\|ing)\b` | WF | 2026-10-12 |
| C037 | streamline | lexical | Marketing verb. | shorten, simplify, remove | `\bstreamlin(e\|es\|ed\|ing)\b` | WF | 2026-10-12 |
| C038 | cutting-edge | lexical | Hype adjective. | cut; cite the recent result | `\bcutting[- ]edge\b` | S9; RS | 2026-10-12 |
| C039 | groundbreaking | lexical | Hype adjective. | cut | `\bgroundbreaking\b` | WP | 2026-10-12 |
| C040 | transformative | lexical | Hype adjective. | cut; say what changes | `\btransformativ(e\|ely)\b` | S9 | 2026-10-12 |
| C041 | game-changer / game changer | lexical | Hype noun. | cut | `\bgame[- ]chang(er\|ing)\b` | LI | 2026-10-12 |
| C042 | paradigm (shift) | lexical | Hype noun. | cut; name the change | `\bparadigm\b` | CL; AIC | 2026-10-12 |
| C043 | holistic | lexical | Vague completeness claim. | cut; list what is included | `\bholistic(ally)?\b` | LI | 2026-10-12 |
| C044 | synergy / synergistic | lexical | Business noun (NSF 'synergistic activities' heading is exempt). | cut | `\bsynerg(y\|ies\|istic)\b(?!\s+activities)` | S9 | 2026-10-12 |
| C045 | vital | lexical | Importance adjective. | cut, or give the consequence | `\bvital\b` | PA | 2026-10-12 |
| C046 | valuable insights | lexical | Stock phrase; says nothing was learned. | state the insight | `\bvaluable insights?\b` | WP | 2026-10-12 |
| C047 | enhance / enhancing | lexical | Vague improvement verb. | say what gets bigger, faster, or more accurate | `\benhanc(e\|es\|ed\|ing\|ement)\b` | WP | 2026-10-12 |
| C048 | highlighting (tail clause) | lexical | Superficial '-ing' analysis tacked on a fact. | end at the fact; new sentence if the point matters | `,\s*highlighting\b` | WP; AW | 2026-10-12 |
| C049 | emphasizing (tail clause) | lexical | Same. | same | `,\s*emphasi[sz]ing\b` | WP | 2026-10-12 |
| C050 | encompassing | lexical | Stock participle. | including, covering | `\bencompass(es\|ed\|ing)?\b` | WP | 2026-10-12 |
| C051 | align with / aligns with | lexical | Vague agreement verb. | agrees with, matches, satisfies | `\balign(s\|ed\|ing)? with\b` | WP | 2026-10-12 |
| C052 | resonate (with) | lexical | Vague agreement verb. | cut | `\bresonat(e\|es\|ed\|ing)\b` | WP | 2026-10-12 |
| C053 | profound | lexical | Praise adjective. | cut; state the consequence | `\bprofound(ly)?\b` | WP | 2026-10-12 |
| C054 | rich (figurative: rich history, rich structure) | lexical | Decorative adjective. | cut, or say what it contains | `\brich (history\|tapestry\|structure\|tradition\|heritage\|array\|source)\b` | WP; AW | 2026-10-12 |
| C055 | diverse array | lexical | Stock phrase. | list them, or give the count | `\bdiverse (array\|range\|set)\b` | WP | 2026-10-12 |
| C056 | renowned | lexical | Promotional adjective. | cut; cite | `\brenowned\b` | WP | 2026-10-12 |
| C057 | excels (at) | lexical | Promotional verb. | say the measurement | `\bexcel(s\|led\|ling)? (at\|in)\b` | PA | 2026-10-12 |
| C058 | quietly (figurative) | lexical | GPT-6-era understatement adverb. | cut | `\bquietly\b` | WP | 2026-10-12 |
| C059 | dependable | lexical | GPT-6-era adjective. | reliable with a measure, or cut | `\bdependable\b` | WP | 2026-10-12 |
| C060 | prioritize | lexical | Business verb. | do first, prefer | `\bprioriti[sz](e\|es\|ed\|ing)\b` | WP | 2026-10-12 |
| C061 | empower | lexical | Marketing verb. | allow, let, enable | `\bempower(s\|ed\|ing\|ment)?\b` | LI | 2026-10-12 |
| C062 | unprecedented | lexical | Hype adjective; usually false. | cut, or give the prior record | `\bunprecedented\b` | RS | 2026-10-12 |
| C063 | revolutionary / revolutionize | lexical | Hype. | cut | `\brevolutioni[sz](e\|es\|ed\|ing)\b\|\brevolutionary\b` | RS | 2026-10-12 |
| C064 | innovative | lexical | Soft-ban hype adjective. | say what is new | `\binnovativ(e\|ely)\b` | AW | 2026-10-12 |
| C065 | importantly / more importantly | lexical | Reader-steering adverb. | cut | `\b(more )?importantly\b` | SS; CP | 2026-10-12 |
| C066 | interestingly | lexical | Reader-steering adverb. | cut | `\binterestingly\b` | SS | 2026-10-12 |
| C067 | fundamentally | lexical | Emphasis adverb. | cut | `\bfundamentally\b` | SS | 2026-10-12 |
| C068 | essentially | lexical | Hedge adverb. | cut, or state the exact sense | `\bessentially\b` | SS | 2026-10-12 |
| C069 | ultimately | lexical | Closing adverb. | cut | `\bultimately\b` | SS | 2026-10-12 |
| C070 | very (intensifier) | lexical | Empty intensifier. | cut | `\bvery\b` | PCW | 2026-10-12 |
| C071 | actually / rather (filler hedges) | lexical | Filler hedges Claude leans on. | cut | `\bactually\b\|\brather\b(?! than)` | PCW | 2026-10-12 |
| C072 | potential (noun/adjective overuse) | lexical | Kobak excess word; hedges a claim. | say what is expected and why | `\bpotential(ly)?\b` | KOB | 2026-10-12 |
| C073 | deep dive / dive into | lexical | Stock phrase. | examine; or just do it | `\bdeep[- ]dive\b\|\bdive into\b` | PA | 2026-10-12 |
| C074 | at its core | lexical | Pseudo-depth opener. | cut | `\bat its core\b` | LL | 2026-10-12 |
| C075 | the fact that | lexical | Wordy nominalizer. | that, because | `\bthe fact that\b` | ST | 2026-10-12 |
| C076 | in order to | lexical | Wordy. | to | `\bin order to\b` | ST | 2026-10-12 |
| C077 | it is clear that / clearly | lexical | Asserts obviousness; in proofs often hides the gap. | give the one-line reason or cut | `\bit is clear that\b\|\bclearly\b` | PCW; MATH | 2026-10-12 |
| C078 | stands as / serves as / functions as / represents a | lexical | Copula avoidance. | is | `\b(stands\|serves\|functions\|operates) as\b` | WP | 2026-10-12 |
| C079 | refers to (lead definition) | lexical | Describes the word, not the object. | X is ... | `\brefers to\b` | WP | 2026-10-12 |
| C080 | key (adjective: key role, key insight, key point) | lexical | Importance adjective. | cut 'key' | `\bkey (role\|insight\|point\|idea\|observation\|takeaway\|turning point\|moment)\b` | WP; MATH | 2026-10-12 |
| C081 | matters (sentence-final 'X matters.') | lexical | GPT-6-era aphoristic closer. | say why in the same sentence | `\bmatters\.\s*$` | WP | 2026-10-12 |
| C082 | dynamic (adjective) | lexical | Vague adjective. | cut, or say what changes | `\bdynamic\b(?! (programming\|system\|systems\|range))` | LI | 2026-10-12 |
| C083 | shed light on | lexical | Stock metaphor. | explain, compute, determine | `\bshed(s\|ding)? light on\b` | LI | 2026-10-12 |
| C084 | double-edged sword | lexical | Cliché. | state both effects | `\bdouble[- ]edged sword\b` | LI | 2026-10-12 |
| C085 | move the needle | lexical | Cliché. | cut | `\bmove the needle\b` | LI | 2026-10-12 |
| C086 | ever-evolving / rapidly evolving | lexical | Stock scene-setting. | cut | `\b(ever\|rapidly\|constantly)[- ]evolving\b` | WF; RS | 2026-10-12 |
| C087 | it's worth noting (that) | rhetorical | Throat-clearing before a fact. | state the fact | `\b(it'?s\|it is) worth (noting\|mentioning\|pointing out)\b` | WF; PCW | 2026-10-12 |
| C088 | it is important to note / remember / consider | rhetorical | Preaching; PD-POLICY P12. | state the fact | `\bit('?s\| is) (important\|essential\|crucial\|vital\|imperative) to (note\|remember\|consider\|understand\|recogni[sz]e)\b\|\bimportant to (note\|consider)\b` | PA; P12 | 2026-10-12 |
| C089 | it should be noted | rhetorical | Same. | state the fact | `\bit should be noted\b` | RS | 2026-10-12 |
| C090 | in today's fast-paced / digital / ever-evolving world | rhetorical | Vapid scene-setting opener. | delete the sentence | `\bin today'?s\b` | WF; AIC; SS | 2026-10-12 |
| C091 | in the realm of / in the world of | rhetorical | Grandiose locator. | in | `\bin the (realm\|world) of\b` | PA | 2026-10-12 |
| C092 | when it comes to | rhetorical | Filler topic-marker. | for, about, or restructure | `\bwhen it comes to\b` | LI | 2026-10-12 |
| C093 | plays a (crucial\|key\|vital\|pivotal\|significant) role | rhetorical | Importance frame with no content. | say what it does | `\bplays? an? (crucial\|key\|vital\|pivotal\|significant\|important\|central) (role\|part)\b` | WP | 2026-10-12 |
| C094 | serves as a testament / stands as a reminder | rhetorical | Puffery. | cut | `\b(serves\|stands) as an? (testament\|reminder)\b` | WP; AW | 2026-10-12 |
| C095 | in conclusion / in summary / to sum up / in essence / overall, | structural | Compulsive summarizing; restates the thesis. | delete the recap | `^\s*(in conclusion\|in summary\|to sum up\|in essence\|to summari[sz]e\|overall),?\b` | AW; AIC; RS | 2026-10-12 |
| C096 | Here's the thing / Here's the kicker / the part most people miss | rhetorical | Conversational reveal frame. | state the thing | `\bhere'?s the (thing\|kicker\|catch\|point)\b\|\bmost people miss\b` | PA; TSK | 2026-10-12 |
| C097 | Let's (break it down / dive in / explore / take a look) | rhetorical | Preamble; chat register. | cut; start with the content | `\blet'?s (break\|dive\|explore\|take a (closer )?look\|unpack\|examine\|begin\|start)\b` | AIB; TSK | 2026-10-12 |
| C098 | Certainly! / Of course! / Great question / I hope this helps / You're absolutely right | rhetorical | Chat residue (AI18). | delete | `\b(certainly\|of course)!\|\bgreat question\b\|\bi hope this helps\b\|\byou'?re absolutely right\b\|\bwould you like\b\|\blet me know\b` | WP; PA; AI18 | 2026-10-12 |
| C099 | based on the information provided / available information | rhetorical | Hedging disclaimer about sources. | cite the source or cut | `\bbased on (the )?(information\|available) (provided\|information\|sources)\b\|\bwhile specific details are (limited\|scarce)\b` | WP; PA | 2026-10-12 |
| C100 | as an AI / as of my last knowledge update | rhetorical | Model self-reference. | delete | `\bas an ai\b\|\bknowledge (update\|cutoff)\b` | PA | 2026-10-12 |
| C101 | experts argue / agree; some critics argue; observers have cited | rhetorical | Weasel attribution. | name the source | `\b(experts\|observers\|critics\|scholars\|researchers\|many\|some) (argue\|agree\|have (cited\|noted\|argued)\|believe\|suggest)\b` | WP; AW | 2026-10-12 |
| C102 | studies show / research shows / it is well known (bare) | rhetorical | Unsourced authority. | cite | `\b(studies\|research) (show\|shows\|suggest\|suggests\|indicate\|indicates)\b\|\bit is well[- ]known\b(?=[^\x5c]*$)` | AIC; AW | 2026-10-12 |
| C103 | it's not just X, it's Y / not only X but also Y | rhetorical | Negative parallelism; manufactured reveal. The single most-cited AI tell. | state Y | `\b(is\|it'?s\|are\|was\|were) not (just\|only\|merely\|simply)\b\|\bnot only\b.*\bbut (also)?\b` | WP; PCW; LL; AW | 2026-10-12 |
| C104 | not X, but Y / It's not about X; it's about Y | rhetorical | Same frame, knocks down a premise nobody held. | state Y | `\bit'?s not (about\|that)\b\|\bnot a\b[^.;]{0,40},\s*but (a\|an\|the)\b\|\bthis isn'?t\b` | WP; LL | 2026-10-12 |
| C105 | Y rather than X (reversed parallelism) | rhetorical | Reversed negative parallelism, recent LLM habit. | state Y; drop the foil | `\brather than\b` | WP | 2026-10-12 |
| C106 | No X. No Y. Just Z. (dramatic countdown) | rhetorical | Negating options before the reveal. | state Z | `\bno \w+[,.] no \w+[,.] (just\|only)\b` | TSK | 2026-10-12 |
| C107 | The result? X. (rhetorical Q&A) | rhetorical | Question nobody asked, answered for effect. | state X | `\b(the result\|the (reason\|answer\|catch\|problem\|upshot\|takeaway))\?\s` | AIB; TSK | 2026-10-12 |
| C108 | rhetorical question opener (Why does this matter? What changed?) | rhetorical | Self-posed question answered next sentence. | state the answer | `^\s*(why\|what\|how\|so what) [^?]{0,60}\?\s*$` | TSK | 2026-10-12 |
| C109 | This cannot be overstated / This highlights the importance of | rhetorical | Editorializing. | cut | `\bcannot be overstated\b\|\bhighlights the (importance\|need\|significance)\b` | AW; WF | 2026-10-12 |
| C110 | setting the stage for / marking a shift / key turning point / indelible mark / deeply rooted | rhetorical | Legacy framing. | state the event and date | `\bsetting the stage\b\|\bmark(s\|ed\|ing)? an? (shift\|turning point\|new (era\|chapter))\b\|\bindelible mark\b\|\bdeeply rooted\b` | WP | 2026-10-12 |
| C111 | whether you're a X or a Y (audience hedge) | rhetorical | Address-everyone hedge. | name the reader | `\bwhether you'?re\b` | AIC | 2026-10-12 |
| C112 | from X to Y (false range) | rhetorical | Implies a spectrum that does not exist ('from intimate gatherings to global movements'). | list the items | `\bfrom (the )?\w+ to (the )?\w+\b` | AW | 2026-10-12 |
| C113 | despite these challenges / future outlook / challenges and legacy | structural | Outline-like closer. | cut | `\bdespite (these\|its\|the) challenges\b\|\bfuture (outlook\|prospects)\b` | WP | 2026-10-12 |
| C114 | the distinction matters because / this distinction is important | rhetorical | Explains why to care instead of making the point. | make the point | `\b(this \|the )?distinction (matters\|is important)\b` | WP | 2026-10-12 |
| C115 | in a world where | rhetorical | Scene-setting opener. | cut | `\bin a world where\b` | RS | 2026-10-12 |
| C116 | at the end of the day / it goes without saying / needless to say | rhetorical | Cliché. | cut | `\bat the end of the day\b\|\bit goes without saying\b\|\bneedless to say\b` | RS | 2026-10-12 |
| C117 | a step in the right direction | rhetorical | Cliché. | state the step | `\bstep in the right direction\b` | RS | 2026-10-12 |
| C118 | the elephant in the room | rhetorical | Cliché. | state it | `\belephant in the room\b` | RS | 2026-10-12 |
| C119 | stands at the intersection of / lies at the heart of | rhetorical | Grandiose locator. | connects, uses | `\b(at the intersection of\|at the heart of\|lies at the core)\b` | RS | 2026-10-12 |
| C120 | a wide range of / a variety of (unspecified) | rhetorical | Vague plurality. | count or list | `\ba (wide\|broad) (range\|variety\|array) of\b` | RS | 2026-10-12 |
| C121 | not a silver bullet / no silver bullet | rhetorical | Cliché. | state the limitation | `\bsilver bullet\b` | RS | 2026-10-12 |
| C122 | game of two halves / tip of the iceberg / only scratches the surface | rhetorical | Cliché. | cut | `\btip of the iceberg\b\|\bscratch(es\|ing)? the surface\b` | RS | 2026-10-12 |
| C123 | one might argue / one could say / some might say | rhetorical | Hedge via imaginary interlocutor. | argue it or cut | `\bone (might\|could) (argue\|say)\b\|\bsome might say\b` | RS | 2026-10-12 |
| C124 | it turns out (that) | rhetorical | Narrates discovery instead of stating result. | state the result | `\bit turns out\b` | MATH | 2026-10-12 |
| C125 | may / might stacks (hedging overload) | syntactic | Two or more hedges in one sentence. | one hedge or none | `\b(may\|might\|could\|potentially\|possibly\|perhaps)\b.*\b(may\|might\|could\|potentially\|possibly\|perhaps)\b` | PCW; AIC | 2026-10-12 |
| C126 | em dash overuse (--- or U+2014), more than one per paragraph | syntactic | Dash as clause-splicer; LLM rate 5-20x human. Older models worst; still a tell. | comma, period, parentheses, or recast; at most one per paragraph | `builtin:emdash` | WP; PCW; WF; AW | 2026-10-12 |
| C127 | semicolon triad 'A; B; C.' | structural | Three parallel clauses joined by semicolons; Opus-era rate 3x human. | separate sentences, or two clauses | `builtin:semitriad` | CL; PI | 2026-10-12 |
| C128 | rule of three: 'X, Y, and Z' of short parallel items | syntactic | Triads default regardless of how many items exist; judge each hit, a real triad stays. | the number of items the content has | `builtin:triad` | WP; AW; AIB; OWC | 2026-10-12 |
| C129 | colon-chain: two or more colons in one sentence | structural | Nested announcement structure. | one colon or none; split | `builtin:colonchain` | PI | 2026-10-12 |
| C130 | run-in \emph{Label.} or \emph{Label:} at sentence start | structural | Scaffolding label (PD-POLICY P4). | fold the label into the sentence or use a \subsubsection | `(^\|\.\s+)\x5cemph\{[^{}]{1,40}[.:]\}` | PI; P4 | 2026-10-12 |
| C131 | bold label run-in \textbf{Label.} / **Label:** | structural | Key-takeaways formatting. | write the sentence | `(^\|\.\s+)\x5ctextbf\{[^{}]{1,40}[.:]\}\|^\s*[-*]\s*\*\*[^*]{1,40}[.:]\*\*` | WP; AW; P4 | 2026-10-12 |
| C132 | inline-header bullet list (- **Header:** text) | structural | LLM list shape. | prose, or plain items | `^\s*[-*+]\s+\*\*[^*]+\*\*\s*[:—-]` | WP | 2026-10-12 |
| C133 | First, / Second, / Third, bullets or paragraph openers | structural | Enumeration scaffolding. | prose with the logical connective | `^\s*(first\|second\|third\|fourth\|finally)(ly)?,` | AIB | 2026-10-12 |
| C134 | Step N scaffolding (\item[Step 1], Step 1:, \paragraph{Step}) | structural | Work-plan steps dressed as argument (PD-POLICY P5). | prose plan, or proof program with the real number of steps | `\x5citem\[Step\b\|\bstep \d+[:.]\|\x5cparagraph\{Step\b` | PI; P5 | 2026-10-12 |
| C135 | sentence-final summary tail ('In short, ...' / 'Thus, X matters.') | structural | Paragraph ends by restating itself. | delete the last sentence | `^\s*(in short\|in other words\|put (simply\|differently)\|simply put\|the upshot is\|the bottom line)\b` | SS; CP | 2026-10-12 |
| C136 | title-case section headings | structural | LLM headings capitalize every word. | sentence case (house style) | `(?-i:[\x5c](?:sub)*section\*?\{(?!Results from Prior NSF Support)\w+(?: (?:[a-z]+\|[A-Z]{2,}))*(?: [A-Z][a-z]+(?: (?:[a-z]+\|[A-Z]{2,}))*){3,}\})` | WP | 2026-10-12 |
| C137 | emoji in headings or bullets | structural | Chat formatting. | delete | `[\U0001F300-\U0001FAFF\u2600-\u27BF]` | WP | 2026-10-12 |
| C138 | curly quotes in source (U+2018/2019/201C/201D) | syntactic | Pasted from a chat window. | LaTeX quotes `` '' or straight quotes | `[‘’“”]` | WP; AIB | 2026-10-12 |
| C139 | horizontal rule between sections (---, ***) | structural | Markdown thematic breaks. | delete | `^\s*(-{3,}\|\*{3,})\s*$` | WP | 2026-10-12 |
| C140 | dramatic fragments ('She waited. And waited.') | syntactic | One-clause sentences for effect. | join or cut |  | AIB; SS | 2026-10-12 |
| C141 | one-sentence paragraph used as a punchline | structural | Emphasis by whitespace. | attach to the paragraph it concludes, or cut | `builtin:onesentpara` | SS | 2026-10-12 |
| C142 | uniform sentence length / uniform paragraph length | syntactic | Rhythm with no variance. | vary; merge or split |  | WF; AW; SS | 2026-10-12 |
| C143 | participial opener ('Spanning fifty years, the program ...') | syntactic | Front-loaded modifier. | subject first | `^\s*(spanning\|building on\|drawing on\|leveraging\|having\|recogni[sz]ing)\b[^,]{3,60},` | AW | 2026-10-12 |
| C144 | tail clause ', ensuring/underscoring/reflecting/contributing to ...' | syntactic | Superficial analysis appended to a fact. | end at the fact | `,\s*(ensuring\|underscoring\|reflecting\|symboli[sz]ing\|contributing to\|cultivating\|fostering\|enhancing\|demonstrating\|signaling\|solidifying\|cementing)\b` | WP; AW | 2026-10-12 |
| C145 | passive stacks with no agent | syntactic | Hides who did what; three passives in a paragraph. | name the agent |  | AW; SS | 2026-10-12 |
| C146 | parenthetical aside density (one per two sentences) | syntactic | Hedging by parentheses. | commit to the sentence or cut the aside | `builtin:parens` | PCW | 2026-10-12 |
| C147 | excessive boldface in prose | structural | Key-takeaways emphasis. | no bold in running prose | `\x5ctextbf\{[^{}]{1,60}\}.*\x5ctextbf\{` | WP; AW | 2026-10-12 |
| C148 | header + bullets + summary on every section | structural | Template shape of a chat answer. | prose with topic sentences (P6) |  | WF | 2026-10-12 |
| C149 | 'Overall,' / 'Ultimately,' paragraph openers | structural | Summary openers. | cut | `^\s*(overall\|ultimately\|all in all\|taken together),` | AW | 2026-10-12 |
| C150 | transition chain (Furthermore ... Moreover ... Additionally) | syntactic | Connective at the head of successive sentences. | cut; order the sentences so no connective is needed | `builtin:transitions` | AIC; AW | 2026-10-12 |
| C151 | avoidance of contractions in informal text / contractions in formal text | syntactic | Register mismatch. | match the venue |  | AW | 2026-10-12 |
| C152 | elegant variation (synonym cycling for one object) | syntactic | Rotating 'the curve / the object / the variety' for one thing. | one name per object |  | WP | 2026-10-12 |
| C153 | 'X: Y' aphoristic sentence ('The lesson: start small.') | structural | Colon aphorism. | write the sentence | `^\s*(the\|a) (lesson\|takeaway\|point\|upshot\|result\|answer\|catch\|reason)[^:]{0,20}:` | RS | 2026-10-12 |
| C154 | scare quotes around ordinary terms | syntactic | Hedging a word. | use the word or define it |  | AW | 2026-10-12 |
| C155 | fake specificity ('studies show 73% of ...') | rhetorical | Number with no source. | source and date (S11) |  | AIC; S11 | 2026-10-12 |
| C156 | 'Note that' / 'Observe that' / 'Recall that' as every-paragraph opener | syntactic | Human too, but LLMs open half their sentences this way. | at most one per section; otherwise state it | `^\s*(note\|observe\|recall\|notice) that\b` | MATH | 2026-10-12 |

## Mathematical-writing claudisms

Patterns specific to math papers and proposals. Several are legitimate once per paper ("Equivalently", "Note that"); the tell is density and the frame-before-fact habit.

| id | pattern | type | why it reads as machine | replacement | regex | source | added |
|---|---|---|---|---|---|---|---|
| C157 | This is exactly the failure mode | lexical | Diagnoses the reader's confusion instead of stating the fact. | state what fails and where | `\b(this\|that) is (exactly\|precisely) the (failure mode\|problem\|point\|issue\|obstruction)\b` | PI | 2026-10-12 |
| C158 | The reason to care is / Why this matters | rhetorical | Importance frame. | the consequence, in the same sentence as the claim | `\bthe reason to care\b\|\bwhy (this\|it) matters\b\|\breason this matters\b` | PI | 2026-10-12 |
| C159 | in its own way | lexical | Hedge that excuses imprecision. | cut, or say the way | `\bin (its\|their\|his\|her) own (way\|right)\b` | PI | 2026-10-12 |
| C160 | the point is (that) | rhetorical | Announces a claim instead of making it. | cut the frame | `\bthe point is\b\|\bthe point here is\b\|\bthat'?s the point\b` | PI | 2026-10-12 |
| C161 | which is what X means / this is what it means to | lexical | Reframes a definition as a reveal. | define X once, in a definition environment | `\bwhich is (exactly \|precisely )?what\b.*\bmeans?\b\|\bthis is what it means\b` | PI | 2026-10-12 |
| C162 | not a way around / there is no way around | rhetorical | Negative frame for a constraint. | state the constraint | `\b(not\|no) a way around\b\|\bno way around\b` | PI | 2026-10-12 |
| C163 | the correct statement is / the right statement is / the honest statement is | lexical | Corrects a strawman nobody stated; process in the mathematics. | state the statement | `\bthe (correct\|right\|honest\|precise\|true) (statement\|version\|formulation\|claim) is\b` | PI | 2026-10-12 |
| C164 | What is new / Where it stands / Built on / Plan. (run-in \emph labels) | lexical | Scaffolding labels (P4). | the objective sentence says what is new | `\x5cemph\{(what is new\|where it stands\|built on\|plan\|deliverables\|status)[.:]?\}\|\bwhat is new\b` | PI; P4 | 2026-10-12 |
| C165 | the kind of object from which / a new kind of object | lexical | Vague genus claim. | name the object and its definition | `\bkind of object\b` | PI | 2026-10-12 |
| C166 | arrives faster than it can be read / faster than anyone can read | lexical | Drama about output volume. | give the count and the date | `\bfaster than (it\|they\|anyone\|one) can (be )?(read\|check\|verif)` | PI | 2026-10-12 |
| C167 | in the form the X theory has / in the form that X takes | lexical | Vague analogy to a parent theory. | state the analogous theorem with a citation | `\bin the form (the\|that)\b.{0,40}\b(theory\|has\|takes)\b` | PI | 2026-10-12 |
| C168 | Concretely, / Explicitly, / More precisely, as paragraph openers | lexical | Promise of precision after an imprecise sentence; delete the imprecise one. | write the precise sentence first | `^\s*(concretely\|explicitly\|more precisely\|more concretely),` | MATH | 2026-10-12 |
| C169 | the key observation / the key insight / the key point / the main idea is | rhetorical | Announces the idea instead of giving it. | state the observation | `\bthe (key\|main\|central\|crucial\|basic) (observation\|insight\|point\|idea\|step\|difficulty) (is\|here)\b` | MATH | 2026-10-12 |
| C170 | Crucially, / Importantly, inside a proof | lexical | Importance adverb where the logic should carry the weight. | cut | `^\s*(crucially\|importantly\|critically),` | MATH; SS | 2026-10-12 |
| C171 | the upshot is / the takeaway is / the moral is / the slogan is | rhetorical | Summary frame. | state it | `\bthe (upshot\|takeaway\|moral\|slogan\|lesson) (is\|here)\b` | MATH | 2026-10-12 |
| C172 | morally / in a precise sense / in a sense / there is a sense in which | lexical | Hedge about rigor. | either prove it or label it a heuristic once | `\bmorally\b\|\bin a (precise\|certain\|real\|very real) sense\b\|\bin a sense\b\|\bthere is a sense in which\b` | MATH | 2026-10-12 |
| C173 | makes precise the idea that / unifies / bridges | lexical | Grand-framing verbs. | state the theorem | `\bmakes? precise\b\|\bunif(y\|ies\|ying)\b\|\bbridg(e\|es\|ing) (the gap\|between)\b` | MATH | 2026-10-12 |
| C174 | the right framework / the natural setting / the correct generality | lexical | Asserts canonicity. | state what the framework gives that the old one did not | `\bthe (right\|correct\|natural\|proper) (framework\|setting\|generality\|language\|home)\b` | MATH | 2026-10-12 |
| C175 | load-bearing / the engine / the mechanism / the heart of the argument | lexical | Metaphor for 'main lemma'. | name the lemma | `\bload[- ]bearing\b\|\bthe engine (of\|behind)\b\|\bheart of the (argument\|proof\|matter)\b` | MATH | 2026-10-12 |
| C176 | This recovers / This is a genuine / genuinely new | lexical | Self-assessment of novelty. | state the special case or the new case | `\bgenuinely (new\|different)\b\|\ba genuine\b` | MATH | 2026-10-12 |
| C177 | In other words / Put differently / Equivalently chains (two in one paragraph) | structural | Restating instead of stating once. | one statement | `builtin:restate` | MATH; SS | 2026-10-12 |
| C178 | colon introducing a one-line reveal ('The answer: no.') | lexical | Aphorism. | sentence | `:\s*(no\|yes\|neither\|both\|none)\.\s*$` | MATH | 2026-10-12 |
| C179 | non-expert gloss stacked after every term ('the Frobenius, i.e. the map that ...') | lexical | Over-definition inline; three glosses per paragraph. | define once in a definition environment (P2) |  | MATH; P2 | 2026-10-12 |
| C180 | 'we initially believed' / 'an earlier draft' / 'the model suggested' | lexical | Process in the mathematics (LX, using-latexpowers). | delete; disclosure section only | `\b(we\|the pi) (initially\|originally\|first) (believed\|thought\|expected\|conjectured)\b\|\bearlier draft\b\|\bprevious version\b` | LXP | 2026-10-12 |

## Retired

None yet. Rows are never deleted; a retired row keeps its id, gets `type` = `retired`, and its `added` cell gains `; retired YYYY-MM-DD`.
