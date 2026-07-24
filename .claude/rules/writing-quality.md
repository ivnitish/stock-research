Bull/bear cases and compounding engine sections must prioritize readability and explanatory depth over rigid structure. Each point should:
- Weave numbers into a narrative that explains WHY something compounds
- Show cause -> effect -> implication chain clearly
- Be readable by someone who hasn't studied the template structure

Bad: "ROIC of 34% on 80% reinvestment rate implies 27% CAGR. At 22x terminal = 2,650."
Good: "EPACK's compounding engine runs at 27% incremental ROIC on capital deployed into a market where India's PEB penetration is 15% versus 70%+ globally — the runway is measured in decades, not years."

Draft as narrative paragraphs first with numbers embedded, then check template boxes. Don't write to fill template slots — write to convey the investment thesis clearly.

## Voice — what to avoid

These patterns leak in from training data and make analysis read like a templated LLM output. Cut them on the voice pass:

- **Scaffolding labels in prose:** "the bull case is", "the bear case is", "the setup is", "the thesis is", "the play here is". Just say the thing — don't announce you're about to say it. Section headers can use these labels; the prose inside cannot.
- **Editorial one-liners and aphorisms:** "Cheap and stagnant is a trap, not an opportunity." "A debt-free balance sheet doesn't rescue a business that isn't growing." If a sentence could be a tweet on its own, it's existing for rhythm, not information. Cut it.
- **Lists disguised as sentences:** "I'd want two quarters of growth, real revenue from new businesses, and DIIs stepping back in." Three items strung together with commas reads like a checklist. Rewrite so the reader follows a thought instead of ticking off items.
- **Bullet-storms when prose would do:** bullets are for genuinely list-like content (tables, peer comparisons, exit triggers). Not for "here are four sentences I split into four bullets."
- **Preambles and trailing recaps:** "Let me check..." / "In summary..." add no information.

## House writing standard + voice pass

The `no-ai-slop` skill (`.claude/skills/no-ai-slop/SKILL.md`) is the house writing standard for ALL composed prose — research files, morning-brief theme digests, MACRO_THREAD entries, Telegram snapshots, fintwitter theses. Draft to it from the first sentence; do not write slop and edit it out afterwards. It absorbs this rule's voice checks as "House patterns" and adds mechanical ones (banned words, weasel attribution, faux-insight setups, em-dash density, fragment stacking).

The voice pass before finalising is verification, not the writing step: run detect mode on every new or updated prose section and fix anything that slipped through, checking against the skill's `eval.md`. Sourced headline-bullet sections (e.g. MORNING_BRIEF.md holdings/macro lists) are exempt — that format is correct for a news digest.

Tables, data, framework checks, and structural sections are unchanged by the voice pass.

## Reference example of the right voice

Same facts, narrative flow:

> Protean is the kind of stock that looks cheap until you ask what it actually is. On one side you have a debt-free utility with book value as a floor and genuine optionality if ONDC or the account aggregator ever scale. On the other, you have a company that grew sales 3% a year for half a decade, just lost the renewal of its biggest contract, and watched its most informed shareholders cut their stake in half. What's missing is any evidence that the picture is turning. Until the non-PAN revenue actually starts showing up in the quarterlies and the DII selling finds a floor, the cheapness on its own isn't a reason to own it.

No "bull case / bear case", no aphorisms, no list-as-sentence. Reader follows a thought. Numbers embedded in the explanation, not announced.
