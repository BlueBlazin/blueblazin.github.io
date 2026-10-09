# Writing guide for specimen cards

You are rewriting the explanation cards of a website that catalogues the many meanings of the word
"kernel" across computing, mathematics and science. Each card explains one meaning.

## Reader
A strong STEM undergraduate: comfortable with calculus, linear algebra, basic probability and some
programming. Not a specialist in this particular field. If you need a term beyond that level,
define it in a few plain words or avoid it.

## Voice
- American English spelling and usage (center, color, behavior, modeling, analyze).
- To the point. Short, declarative sentences. Lead with what the thing *is* or *does*.
- Plain words over jargon. No filler ("it is important to note", "essentially", "in other words").
- No hype, no rhetorical questions, no em dashes. Use commas, colons or separate sentences.
- Concrete beats abstract: name a real system, a number, a familiar case.

## Accuracy
- Never trade correctness for simplicity. Every statement must be true as written.
- Stay consistent with the original text and its sources. Do not invent facts, dates, names or history.
- If you are unsure about a detail, leave it out rather than guess.
- Keep or fix the LaTeX formula. It must be valid KaTeX and use standard notation. Simplify it if a
  simpler standard form says the same thing.

## Fields to write (per entry)
| field | what | length |
|---|---|---|
| `short` | One-line definition, a full sentence ending in a period. | ≤ 14 words |
| `body` | What it is and how it works, for the reader above. | 2–3 sentences, ≤ 60 words |
| `tex` | The key formula (LaTeX, no $ signs), or "" if a formula would not help. | — |
| `read` | The formula read aloud in plain English, saying what each symbol is. "" if no tex. | 1 sentence, ≤ 35 words |
| `example` | One concrete example or use case. Numbers or real systems where possible. | 1–2 sentences, ≤ 45 words |
| `why` | Why the word "kernel" fits this meaning (the core, what is left, what is inside the integral, etc.). Describe the sense; make no historical claims you cannot support. | 1 sentence, ≤ 25 words |
| `note` | "Don't confuse it with": the most likely mix-up, stated plainly. "" if none is useful. | 1–2 sentences, ≤ 40 words |
| `variants` | Named sub-kinds or related forms, as a list of short strings (keep the original items, tidy wording and spelling). | as given |

Do not change `id`, names, code, references or sources.

## Output
Write a JSON object to the output path you are given, keyed by entry `id`:

```json
{
  "cuda": {"short": "...", "body": "...", "tex": "...", "read": "...", "example": "...", "why": "...", "note": "...", "variants": ["..."]}
}
```

It must be valid JSON (escape backslashes in LaTeX as `\\`). Include every entry from your input file.
After writing, re-read your file, check each entry against this guide (length limits, American spelling,
no em dashes, correctness), fix anything that fails, and reply with only the path and the count of entries.
