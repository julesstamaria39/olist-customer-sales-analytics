# Step 6: Final Presentation & Communication

Two 10-slide decks, generated from the executed notebook and its saved evidence:

| Audience | Editable PowerPoint | PDF |
| --- | --- | --- |
| Peers / technical reviewers | [technical_deck.pptx](technical_deck.pptx) | [technical_deck.pdf](technical_deck.pdf) |
| Executives / business stakeholders | [business_deck.pptx](business_deck.pptx) | [business_deck.pdf](business_deck.pdf) |

The technical deck covers data joins, features, temporal validation, model comparisons, PDP/ICE, fairness limitations, and reproducibility. The business deck covers customer priorities, forecast readiness, product planning, illustrative ROI, risks, and a proposed pilot. Repeat-purchase classification stays retired. Forecasting limitations and missing sensitive attributes are explicit.

Headings, body text, tables, diagrams and bar charts are editable PowerPoint objects. The PDP/ICE figure is an embedded image. Speaker notes contain supporting details and evidence references; slide footers identify sources. Both decks use a consistent 16:9 layout and Arial fonts.

The ROI scenarios are assumptions, not model outputs or observed benefits. [roi_scenarios.csv](roi_scenarios.csv) records the calculations: 1,000 contacted customers, BRL 40 contribution per incremental order, BRL 1 contact cost and BRL 500 setup. Break-even is 3.75 percentage points of incremental orders/customer, or at least 38 whole extra orders. Pilot/control outcomes and real costs must replace these assumptions before a business decision.

## Regenerate

Run from the repository root using the environment created in the project README. Presentation dependencies are isolated from that environment:

```powershell
.venv\Scripts\python.exe -m pip install --target artifacts/presentation_tools -r requirements-presentations.txt
.venv\Scripts\python.exe scripts/build_presentations.py
```

The builder reads existing notebook results; it does not retrain models. Regenerate the notebook first if model inputs or analysis have changed. Editing the generator and rebuilding will overwrite generated decks and PDFs; preserve any manual PowerPoint edits separately before rebuilding.

## Checks and limits

The builder checks measured text bounds, object bounds, reopened PowerPoint slide counts, speaker notes, and ten PDF pages per deck. All 20 PDF pages are rendered under previews/ and visually reviewed. [build_manifest.json](build_manifest.json) records the slide titles, validation results, input hashes and ROI assumptions.

PDFs and PowerPoints are generated from the same layout. No native PowerPoint or LibreOffice renderer is installed here, so the visual review uses the matching PDFs rather than an Office-rendered export. Native Office rendering may vary slightly. No extra notebook, external upload, or public publication is created.

The combined final report and a fresh Windows/Python 3.13 analysis run are complete. Protected-group fairness evidence and mitigation validation remain unavailable. See the root README for publication status.
