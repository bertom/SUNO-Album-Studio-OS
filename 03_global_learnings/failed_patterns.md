# Failed Patterns

Patterns that reliably weaken output. Check before `/suno` and `/suno validate`.

| Pattern | Why it fails | Fix |
|---------|--------------|-----|
| Artist names in Styles | SUNO doesn't know them | Concrete instruments and production |
| Studio shorthand in Styles (`Family-like`) | SUNO has no context | Concrete musical terms |
| Negative instructions in Styles | Ignored or inverted | Move to Exclude styles |
| Empty exclude list | Genre bleed (EDM, trap) | Add baseline excludes |
| Weirdness too high on intimate brief | Vocal artifacts, chaos | Lower W, raise SI |
| Weirdness too low on peak brief | Flat, generic | Raise W within range |
| Lyrics as essay | Unsingable | Short lines, one idea per section |
| Batch-generating whole album | No listening loop | One song at a time |

Add your failures via **`/extract learning`**.
