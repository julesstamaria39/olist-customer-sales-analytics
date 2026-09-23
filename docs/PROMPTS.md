# Task prompt templates

Replace bracketed fields with actual task details. Project-wide conventions live in AGENTS.md; avoid repeating them in every prompt. All analysis uses notebooks/Final_Project.ipynb; extend its sections and keep utilities separate.

## Implement

```text
Implement [concrete outcome] in the relevant section of notebooks/Final_Project.ipynb.
Use scripts/ or src/ only for utilities/reusable logic; do not create another
notebook or a duplicate step report.
Read docs/RUBRIC_ALIGNMENT.md and docs/PROJECT_BRIEF.md first.
Identify the relevant R1-R8 criteria and produce evidence for their
Outstanding/Exemplary descriptors. Update the tracker only with actual checks.
Preserve [specific constraints].
Done when [observable checks and expected behavior].
Validation budget: [runtime and any permitted external costs].
Proceed with routine reversible work. Ask if a missing decision materially
affects correctness or scope. Report what changed, actual checks, and limits.
```

## Review

```text
Review notebooks/Final_Project.ipynb against docs/RUBRIC_SOURCE.txt and docs/RUBRIC_ALIGNMENT.md.
Do not edit yet. Identify missing evidence for Outstanding/Exemplary criteria.
Check execution order, data leakage, split strategy, baseline, metric choice,
and agreement between conclusions and computed outputs where applicable.
List findings by severity with cell IDs/headings, evidence, and suggested fixes.
Distinguish confirmed issues from items requiring execution or clarification.
```

## Learn

```text
Help me understand [method/cell]. Explain its purpose and assumptions,
then give a small example. Let me attempt [specific part] before supplying
the full solution. Keep the assignment's constraints in view.
```

## Handoff

```text
Update docs/STATUS.md with verified changes, checks, decisions, unresolved
questions, and the next concrete task. Link relevant files. Distinguish
observed results from assumptions and unexecuted plans.
Update docs/RUBRIC_ALIGNMENT.md with criterion IDs, evidence paths, checks,
and remaining gaps. Do not infer earned points from planned artifacts.
```

## Rubric readiness review

```text
Audit the project against every Outstanding/Exemplary descriptor in
docs/RUBRIC_SOURCE.txt. Use docs/RUBRIC_ALIGNMENT.md as the evidence index.
For each R1-R8 criterion, list verified artifacts and checks, missing evidence,
and the next concrete fix. Prioritize substantive R4/R5 gaps and core criteria
before bonus work. Check both feature selection and dimensionality reduction,
tuned model comparisons, explainability, sensitive-group fairness coverage,
two separate 8-12-slide decks, and public repository readiness.
Do not invent protected attributes, ROI, metrics, or commit history.
Do not claim a guaranteed grade or publish anything during this review.
```
