# Scoring Policy

Score candidates on a 100-point scale.

## Positive dimensions

- Chinese AI relevance: 0-20
- Source quality: 0-15
- Awesome value: 0-20
- Freshness: 0-10
- Verifiability: 0-10
- Category clarity: 0-10
- Community signal: 0-10

## Risk penalties

- hype or unverifiable marketing: -5 to -10
- unclear license for open-weight item: -3
- unstable or JS-only primary link: -3 to -5
- duplicate or near-duplicate: -10
- rumor-only source: -20

## Gates

- `score >= 65`: stable awesome entry.
- `score >= 55`: update existing entry.
- `score >= 45`: daily digest only.
- `score < 45`: reject.

## Hard blocks

- No reachable source URL.
- Not Chinese AI related.
- Exact duplicate.
- Spam/SEO/gray-market content.
- Unsafe workflow.
