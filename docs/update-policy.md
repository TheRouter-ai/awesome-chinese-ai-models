# Update Policy

## Daily target

The maintainer agent should collect at least 10 accepted daily updates when sufficient high-quality sources exist.

Accepted updates may include:

- model releases and updates
- API/docs/pricing changes
- open-weight releases
- official resources and model cards
- benchmark updates
- tutorials and playbooks
- product capability changes
- major industry, policy, infrastructure, or safety news

## Stable list vs daily digest

Not every daily update belongs in the main awesome list.

- Long-term, reusable resources should be added to `data/models.yaml`, `data/resources.yaml`, or `collections/`.
- Short-term news should go to `data/news.yaml` and `newsletters/`.
- Low-confidence community signals should stay out until verified.

## Generated files

README generated blocks must be updated by `scripts/generate_readme.py`.

Generated regions:

- `latest-news`
- `featured-models`
- `providers`

## PR policy

Default: PR-first, no direct push to `main` by automation.

Low-risk PR:

- official sources only
- no broken links
- no new taxonomy category
- no warnings
- 10-20 updates max

Medium-risk PR:

- includes media sources
- includes unclear license or JS-only links
- includes new category proposals

High-risk PR:

- rumors, policy/safety controversy, large batch changes, or unverifiable claims

High-risk PRs should be draft PRs or require human review.
