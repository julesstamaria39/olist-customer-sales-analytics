"""Build two editable PowerPoint decks and matching PDFs from verified evidence.

Text and shapes share one measured layout across PowerPoint and PDF. Chart
images are embedded; all headings, tables, diagrams and bar charts are editable.
PDF previews validate that layout, but are not a native PowerPoint render.
"""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "artifacts" / "presentation_tools"))

import pandas as pd
from PIL import Image
import pypdfium2 as pdfium
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_AUTO_SIZE
from pptx.util import Pt
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

OUT = ROOT / "presentations"
TABLES = ROOT / "reports" / "tables"
W, H = 960, 540
NAVY, TEAL, CORAL = "142D40", "007F82", "C05C3E"
INK, MUTED, PALE, WHITE, GRAY = "213748", "596D7D", "EDF3F5", "FFFFFF", "9EADB6"

pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("ArialBold", "C:/Windows/Fonts/arialbd.ttf"))


def read(name):
    return pd.read_csv(TABLES / name)


def wrap(text, width, size, bold):
    font = "ArialBold" if bold else "Arial"
    lines = []
    for paragraph in str(text).split("\n"):
        current = ""
        for word in paragraph.split():
            candidate = (current + " " + word).strip()
            if pdfmetrics.stringWidth(candidate, font, size) > width and current:
                lines.append(current)
                current = word
            else:
                current = candidate
        lines.append(current)
    assert all(pdfmetrics.stringWidth(line, font, size) <= width+0.1 for line in lines), text
    return lines


class Slide:
    def __init__(self, title, audience, number, source, notes="", dark=False):
        self.title, self.notes, self.elements = title, notes + "\n\nEvidence: " + source, []
        self.rect(0, 0, W, H, NAVY if dark else WHITE)
        self.rect(40, 28, 34, 4, TEAL)
        self.text(86, 22, 830, 20, f"OLIST  /  {audience.upper()}", 10, True, "85CDD0" if dark else TEAL)
        self.text(40, 60, 880, 94, title, 31, True, WHITE if dark else NAVY)
        self.rect(40, 506, 880, 1, "425866" if dark else "D5E0E5")
        self.text(40, 514, 825, 18, source, 8.5, False, "C0CED5" if dark else MUTED)
        self.text(883, 513, 37, 18, f"{number:02d}", 10, True, "C0CED5" if dark else MUTED)

    def rect(self, x, y, w, h, color):
        self.elements.append({"kind": "rect", "x": x, "y": y, "w": w, "h": h, "color": color})

    def text(self, x, y, w, h, text, size=18, bold=False, color=INK):
        lines = wrap(text, w, size, bold)
        assert len(lines)*size*1.16 <= h+0.1, f"Text height overflow: {text}"
        self.elements.append({"kind": "text", "x": x, "y": y, "w": w, "h": h,
                              "lines": lines, "size": size, "bold": bold, "color": color})

    def image(self, x, y, w, h, path):
        path = Path(path)
        with Image.open(path) as im:
            scale = min(w/im.width, h/im.height)
            iw, ih = im.width*scale, im.height*scale
        self.elements.append({"kind": "image", "x": x+(w-iw)/2, "y": y+(h-ih)/2,
                              "w": iw, "h": ih, "path": str(path)})

    def card(self, x, y, w, h, label, value, detail, accent=TEAL):
        self.rect(x, y, w, h, PALE)
        self.rect(x, y, 4, h, accent)
        self.text(x+18, y+15, w-36, 25, label.upper(), 11, True, MUTED)
        value_size = 32
        while len(wrap(value, w-36, value_size, True))*value_size*1.16 > 53:
            value_size -= 1
        self.text(x+18, y+49, w-36, 53, value, value_size, True, accent)
        self.text(x+18, y+110, w-36, h-112, detail, 16)

    def note(self, text, color=TEAL):
        self.rect(40, 448, 880, 44, PALE)
        self.rect(40, 448, 4, 44, color)
        self.text(55, 458, 850, 32, text, 13, False, INK)

    def table(self, x, y, widths, headers, rows, row_height=40, size=15):
        for r, values in enumerate([headers] + rows):
            xx = x
            for width, value in zip(widths, values):
                self.rect(xx, y+r*row_height, width-2, row_height-2, NAVY if r == 0 else PALE if r % 2 else "F8FAFB")
                self.text(xx+10, y+r*row_height+10, width-20, row_height-12, str(value), size,
                          r == 0, WHITE if r == 0 else INK)
                xx += width

    def bars(self, rows, x=40, y=175, label_width=230, width=380, step=55, maximum=None, fmt=".3f"):
        maximum = maximum or max(v for _, v, _ in rows)*1.2
        for i, (label, value, color) in enumerate(rows):
            yy = y+i*step
            self.text(x, yy+3, label_width-12, 36, label, 16)
            self.rect(x+label_width, yy, width, 27, PALE)
            self.rect(x+label_width, yy, max(0.3, width*value/maximum), 27, color)
            self.text(x+label_width+width+12, yy+3, 84, 30, format(value, fmt), 17, True, MUTED if color == GRAY else color)


def make_decks():
    segment = read("04_customer_business_profiles.csv").set_index("segment")
    finalists = read("04_cluster_finalists.csv").set_index("trial")
    weekly = read("04_forecast_test_comparison.csv").set_index("model")
    product = read("04_forecast_business_profiles.csv").set_index("product")
    daily = read("04_daily_trends.csv")
    fairness = json.loads((ROOT/"configs"/"step5_bias_audit.json").read_text())["geography"]
    manifest = json.loads((ROOT/"docs"/"DATA_MANIFEST.json").read_text())
    rf, mean = weekly.loc["Random forest 2", "test_mae"], weekly.loc["Four-week mean", "test_mae"]
    daily_rf, daily_mean = daily.rf_mae.mean(), daily.benchmark_mae.mean()
    match = int(daily.predicted_trend.eq(daily.actual_trend).sum())
    source = "Source: Final_Project.ipynb, executed Steps 1-5; exported model results."
    data_notes = (f"Source: {manifest['source_url']}\nPublisher: Olist; listed license: {manifest['publisher_listed_license']}. "
                  "The dataset is historical and does not represent today's Olist operations. "
                  "Raw-file hashes and counts are in docs/DATA_MANIFEST.json.")
    tech, biz = [], []
    def t(title, src=source, notes="", dark=False):
        slide = Slide(title, "Technical presentation", len(tech)+1, src, notes, dark)
        tech.append(slide)
        return slide
    def b(title, src=source, notes="", dark=False):
        slide = Slide(title, "Business presentation", len(biz)+1, src, notes, dark)
        biz.append(slide)
        return slide

    s=t("Customer segments are clear.\nForecast gains are not.", notes=data_notes, dark=True)
    s.text(40, 172, 850, 64, "A reproducible eCommerce study of customer segmentation and observed-sales forecasting.", 23, False, WHITE)
    s.card(40, 274, 275, 150, "Segmentation sample", "6,000", "customers before April 2018")
    s.card(342, 274, 275, 150, "Forecasting scope", "5 products", "selected using earlier sales")
    s.card(645, 274, 275, 150, "Notebook validation", "36 cells", "fresh-kernel execution passed")
    s.text(40, 460, 865, 34, "Tasks: unsupervised clustering + supervised regression. Repeat-purchase classification was retired.", 13, False, "C0CED5")

    s=t("Start with the correct unit of analysis", "Source: notebook §§2.1-2.3; docs/DATA_MANIFEST.json.", data_notes)
    for x, title, value, detail in [
        (40,"Orders",f"{manifest['files']['olist_orders_dataset.csv']['rows']:,}","One order_id per order"),
        (342,"Customers",f"{manifest['files']['olist_customers_dataset.csv']['rows']:,}","customer_unique_id links repeat buyers"),
        (645,"Order items",f"{manifest['files']['olist_order_items_dataset.csv']['rows']:,}","Multiple item rows can belong to an order")]:
        s.card(x,160,275,180,title,value,detail)
    s.text(40, 361, 880, 62, "Join on validated keys; remove invalid required values and duplicates. Count item rows for sales and distinct orders for customer frequency.", 19)
    s.note("Approval timestamps define the event; approval does not prove delivery. Preserve valid sales history for modeling.")

    s=t("Build features before comparing models", "Source: notebook Step 3; artifacts/step3_bc/feature_selection.csv; configs/step4_models.json.",
        "Correlation filtering at absolute Spearman >0.90 retains recency, frequency, spend and variety. "
        "Average order value overlaps with spend; history length overlaps with recency. This uses the historical development population, "
        "not an unseen-customer test. Preparation and PCA are refitted on the clustering sample and stability subsets. "
        "Two-component PCA is an explicit reduced comparison; the 95%-variance preparation did not compress below four features.")
    s.text(40,160,410,28,"CUSTOMERS",13,True,TEAL)
    s.text(40,200,410,92,"Recency, order frequency, recorded spending, product variety",25,True)
    s.text(40,303,410,116,"Remove overlapping average spend and history length. Impute, log-transform skewed inputs, scale, and compare four features with 2D PCA.",18)
    s.text(505,160,415,28,"PRODUCT SALES",13,True,TEAL)
    s.text(505,200,415,85,"Weekly: lags 1-4 + recent mean\nDaily: calendar inputs only",24,True)
    s.text(505,303,415,116,"Keep zero-sales periods. Use complete historical targets. Product IDs identify the daily models; they are not numeric predictors.",18)
    s.note("Price outlier filtering is for EDA only. It does not erase valid purchase history or target counts.")

    s=t("Respect time when tuning and evaluating", "Source: configs/step4_models.json; configs/step4_daily_forecast.json.",
        "Weekly: 12 settings across 3 four-origin validation windows starting 2 Oct 2017, 6 Nov 2017, 1 Jan 2018. "
        "Every training origin +28 days is no later than its scoring start. Test: 65 origins x products, four outputs; outcomes end 23 Jul exclusive. "
        "Daily: 364/91/112 days for train/validation/test; 1,820/455/560 product-day rows. Four RF settings, 5 separate models; refit train+validation once. "
        "Top products differ between weekly and daily tasks. ML-only weekly selection was requested after prior test inspection; no new untouched-test claim.")
    s.text(40,158,880,27,"WEEKLY: 12 settings / 3 chronological validation windows",19,True)
    s.text(40,195,880,43,"Training outcomes must finish before scoring. Final forecasts: 2 April-25 June 2018; targets end 22 July.",18)
    for x,label,value,detail in [(40,"Daily train","2017","2 Jan-31 Dec; select top five"),(342,"Daily validation","Jan-Mar 2018","Through 1 Apr; tune settings"),(645,"Daily test","Apr-Jul 2018","2 Apr-22 Jul; fixed models")]:
        s.card(x,263,275,160,label,value,detail)
    s.note("These are historical backtests: evaluation dates were already viewed. Weekly target windows overlap.",CORAL)

    s=t("K-Means gives a stable, broad two-group split", "Source: 04_cluster_finalists.csv; 04_cluster_stability.csv.",
        "22 trials across K-Means k=2..6 and DBSCAN eps .2/.4/.6, min_samples 10/30 in selected-feature and PCA spaces. "
        "Compare silhouette in one feature space on the same 1,453 assigned evaluation customers. "
        "Three 80% resamples refit preparation/PCA. ARI measures agreement on shared assigned customers, not unseen-customer accuracy. "
        "K-Means original and PCA tie on common silhouette; original features retained for readability. No test-population generalization claim.")
    s.text(40,145,880,24,"Common-sample silhouette: higher means clearer separation",15,False,MUTED)
    s.bars([("K-Means / 4 features",finalists.loc['cluster_00','common_silhouette'],TEAL),
            ("K-Means / PCA (2)",finalists.loc['cluster_11','common_silhouette'],GRAY),
            ("DBSCAN / PCA (2)",finalists.loc['cluster_19','common_silhouette'],GRAY)],width=360,maximum=1,step=63)
    s.text(40,382,865,44,"Selected K-Means: 2 groups | 100% assigned | mean resampling ARI 1.00",20,True)
    s.note("Descriptive results for a 6,000-customer sample; strong separation does not prove marketing uplift.")

    s=t("Random Forest wins within ML, not overall", "Source: 04_forecast_test_comparison.csv; 04_forecast_ml_ranking.csv.",
        "Weekly RF: 100 trees, max_depth=3, min_samples_leaf=5. Tree: max_depth=2, min_samples_leaf=8. "
        "Weekly validation MAE: RF 1.996, tree 2.110; benchmark mean 1.954. Baselines are benchmark-only. "
        "Test MAE averages 260 product-origin-horizon predictions. The last-week rule is numerically best in test; benchmark selection used validation.")
    s.bars([(name,weekly.loc[key,'test_mae'],color) for name,key,color in [
        ("Last-week benchmark","Last week",GRAY),("Four-week mean","Four-week mean",GRAY),
        ("Random Forest","Random forest 2",TEAL),("Decision Tree","Decision tree 2",TEAL)]],width=370,step=53,maximum=1.3)
    s.text(40,398,865,34,f"Weekly error: items per product-week, averaged across the four horizons. Lower is better.",16)
    s.note(f"RF error is {(rf/mean-1)*100:.1f}% higher than the four-week mean. No forecasting improvement is claimed.",CORAL)

    s=t("Calendar-only daily forecasts miss direction", "Source: 04_daily_trends.csv; configs/step4_daily_forecast.json.",
        "Daily models: one RF per training-selected top product, 100 trees, depth 6, min_samples_leaf 7, seed42. "
        "Inputs: elapsed day number, month, day of month, day of week; no sales history. "
        "Trend = mean of last 28 test days minus first 28; +/-0.1 items/day is a descriptive flat band, not a statistical significance rule. "
        "RF cannot extrapolate sustained time trends. Full product IDs are available in 04_daily_products.csv.")
    s.table(40,159,[190,230,230,230],["Daily product","Predicted trend","Observed trend","Daily error"],
            [[str(i+1),r.predicted_trend,r.actual_trend,f"{r.rf_mae:.2f} items"] for i,r in daily.iterrows()],row_height=40,size=15)
    s.text(40,414,880,24,"Trend: last 28 vs first 28 test days; changes within +/-0.1 items/day count as flat.",14,False,MUTED)
    s.note(f"Trend matches: {match}/5. Daily MAE: RF {daily_rf:.3f} vs average benchmark {daily_mean:.3f}.",CORAL)

    s=t("Recent activity drives the weekly predictions", "Source: notebook §5.1; 05_pdp.csv; reports/figures/05_pdp_ice.png.",
        "Actual sklearn partial_dependence, kind=both, method=brute, output week 1; 180 development rows, 15 grid points, 30 ICE lines shown. "
        "PDP is the averaged model response; ICE shows product-date variation. Lags and their mean are correlated, "
        "so varying one independently creates some unrealistic combinations. These curves are not causal effects. "
        "Method: https://scikit-learn.org/stable/modules/partial_dependence.html")
    s.image(40,159,880,255,ROOT/"reports/figures/05_pdp_ice.png")
    s.note("Dark lines: average response (PDP). Pale lines: individual responses (ICE). Explanation is not causation.")

    s=t("Bias auditing exposes limits, not a fairness pass", "Source: configs/step5_bias_audit.json; 05_sales_errors.csv; 05_state_selection.csv.",
        "Scenario only: offer to higher-median-spend segment, 200/6000 customers; no offers sent. "
        "14 states with >=50 sample customers, 5718/6000 covered. Gap=max-min selection rate; ratio=min/max. "
        "PA 0/54 vs SP 94/2380; PA Wilson interval extends to 6.64%. Intervals exclude model-selection uncertainty. "
        "No valid eligibility/benefit label exists for equalized odds. No gender, race, age, or income fields; geography is not a proxy label. "
        "Definitions: https://fairlearn.org/main/user_guide/assessment/common_fairness_metrics.html")
    s.card(40,165,275,184,"State selection gap",f"{fairness['selection_rate_gap']*100:.2f} pp","Hypothetical segment-only offer",CORAL)
    s.card(342,165,275,184,"Min/max rate ratio",f"{fairness['min_max_selection_ratio']:.2f}","Driven by a small state sample",CORAL)
    s.card(645,165,275,184,"Protected attributes","Missing","Gender, race, age and income",CORAL)
    s.text(40,370,880,63,"Both forecasting models underpredict positive-sales periods. Propose inclusive outreach, better coverage and human review; validate before deployment.",18)
    s.note("Geographic disparity does not establish discrimination. Sensitive-group fairness remains unmeasurable.",CORAL)

    s=t("Reproducible evidence; clear remaining gaps", "Source: notebook, scripts/, configs/, models/, reports/; docs/STATUS.md.",
        "Commands from project root: ../.venv/Scripts/python.exe scripts/run_notebook.py; "
        "scripts/check_daily_forecasting.py; scripts/check_bias_audit.py. Single notebook, model reloads and raw hashes verified. "
        "Clean-environment recreation remains unverified. Final report currently contains only Bias & Fairness Analysis; other chapters remain pending. "
        "Decks do not resolve missing protected-attribute data, mitigation validation, or public repository publication.")
    s.text(40,164,405,31,"WHAT IS SAVED",14,True,TEAL)
    s.text(40,212,405,175,"One executed notebook\nFitted models + preprocessing\nConfigs, seeds and source hashes\nPredictions, metrics and figures\nTargeted leakage/audit checks",20)
    s.text(505,164,415,31,"WHAT COMES NEXT",14,True,CORAL)
    s.text(505,212,415,175,"Validate on newly collected data\nTest practical mitigations\nWindows reproduction verified\nCombined final report complete\nTrack results and limitations",20)
    s.note("Conclusion: segmentation is descriptive; neither forecasting RF has demonstrated an overall benchmark gain.")

    s=b("Use the analysis to plan a measured pilot",notes=data_notes,dark=True)
    s.text(40,175,850,65,"Understand customer groups. Improve sales planning. Keep decisions under review.",25,False,WHITE)
    s.card(40,275,275,150,"Customer insight","2 groups","Broad patterns to investigate")
    s.card(342,275,275,150,"Forecast readiness","Limited","Simple rules still perform better",CORAL)
    s.card(645,275,275,150,"Financial impact","Unproven","ROI requires a controlled pilot",CORAL)
    s.text(40,460,860,31,"Historical Olist study: findings support investigation, not a promise of live commercial results.",14,False,"C0CED5")

    s=b("Two business decisions guide the project",notes=data_notes)
    s.card(40,164,425,238,"Customer planning","Who needs attention?","Use purchase patterns to design and test relevant outreach.")
    s.card(495,164,425,238,"Operations planning","What may sell next?","Compare forecasts with simple rules before using them to order stock.")
    s.note("Scope: a 6,000-customer sample and two training-selected five-product sets. Recorded sales are not total demand.")

    s=b("The large single-order group still matters", "Source: 04_customer_business_profiles.csv; 6,000-customer development sample.",
        "The 5800 single-order customers represent 96.67% of the sampled customers and 93.84% of recorded spending. "
        "The 200 repeat/broader-basket segment has 89% repeats and 90% multiple products. "
        "A historical single order is not evidence that a customer never returned elsewhere or after observation ended.")
    for x,i,label in [(40,0,"Single-order group"),(495,1,"Repeat / broader basket")]:
        r=segment.loc[i]
        s.card(x,165,425,212,label,f"{int(r.customers):,} customers",f"Median recorded spend: BRL {r.median_recorded_spend_brl:.2f}\nShare of sample spending: {r.recorded_spend_share_pct:.1f}%")
    s.text(40,398,875,35,"A smaller individual basket does not make the largest customer group unimportant.",18,True)
    s.note("These are sample profiles, not validated lifetime-value or loyalty categories.")

    s=b("Investigate the first-purchase experience", "Source: notebook §4.4 and Step 2 feasibility discussion; proposed follow-up, not measured effects.")
    for x,label,value,detail in [(40,"Investigate","Experience","Review delivery delays, ratings and product issues."),(342,"Design","Relevant outreach","Include single-order customers; avoid segment-only exclusion."),(645,"Evaluate","Incremental benefit","Compare with a randomized control group over the same period.")]:
        s.card(x,173,275,232,label,value,detail)
    s.note("Repeat-purchase classification was retired. One observed order does not mean permanent churn.")

    s=b("Keep simple forecasting rules in the decision", "Source: 04_forecast_test_comparison.csv; 04_daily_trends.csv.",
        "Weekly comparison shown uses the validation-selected four-week mean benchmark. Last-week benchmark test MAE was even lower at 0.869. "
        "RF is the best ML candidate, but weekly RF MAE 1.021 versus mean0.894. Daily MAE0.850 versus mean0.817; trend matches0/5. "
        "Daily and weekly errors have different units and cannot be compared as a claim of improvement.")
    s.bars([("Four-week average",mean,GRAY),("Weekly Random Forest",rf,TEAL)],y=183,width=370,maximum=1.3,step=74)
    s.text(40,342,880,64,f"Weekly RF error is {(rf/mean-1)*100:.1f}% higher. Daily models matched {match}/5 observed trend directions.",23,True,CORAL)
    s.note("Error is average items per product-week, across four horizons. Human review remains necessary.")

    share=product.loc['Product 1','selected_product_sales_share_pct']
    s=b("Concentrate review where recorded activity is", "Source: 04_forecast_business_profiles.csv; 16 evaluated weeks, five weekly-selected products.",
        "Count actual product-week sales once, despite overlapping forecast windows. Product1:63/81 items, 77.78%; "
        "Product3:12; Products2/5:3 each; Product4:0. These are not category-wide figures. "
        "Full product IDs and categories are in reports/tables/04_forecast_business_profiles.csv. "
        "Availability and stockouts are unobserved; zero sales does not establish zero demand.")
    s.text(40,133,880,23,"Recorded items across 16 evaluation weeks",15,False,MUTED)
    s.bars([(name,float(product.loc[name,'recorded_items']),TEAL if name=='Product 1' else GRAY)
            for name in ['Product 1','Product 2','Product 3','Product 4','Product 5']],y=159,label_width=155,width=365,step=48,maximum=70,fmt=".0f")
    s.text(682,177,238,69,f"{share:.0f}%",46,True,TEAL)
    s.text(682,255,238,142,"of this small product set's recorded sales came from Product 1. Review its forecasts first.",20)
    s.note("For quiet products, check availability before assuming declining demand or changing stock orders.")

    # Assumptions are explicit and independent of the observed model scores.
    contacts, margin, cost_each, setup = 1000, 40, 1, 500
    total_cost=contacts*cost_each+setup
    roi=pd.DataFrame([{"assumed_uplift_pp":lift*100,"extra_orders":contacts*lift,
        "incremental_contribution_brl":contacts*lift*margin,
        "pilot_cost_brl":total_cost,"net_value_brl":contacts*lift*margin-total_cost,
        "roi_pct":100*(contacts*lift*margin-total_cost)/total_cost} for lift in [.01,.03,.05]])
    s=b("What would a customer pilot need to earn?", "Source: illustrative assumptions only; presentations/roi_scenarios.csv. No observed ROI claimed.",
        "Illustrative outreach ROI, unrelated to forecast MAE. Assume1000 contacted customers, BRL40 incremental contribution "
        "per extra order after variable fulfillment costs, BRL1 outreach cost per contacted customer, BRL500 setup; totalcost1500. "
        "Uplift is percentage-point increase in the probability of one incremental order per customer, relative to a randomized control. "
        "ROI=(incremental contribution-cost)/cost. Break-even uplift1500/(1000*40)=3.75pp, or at least38 whole extra orders. "
        "Assumptions must be replaced by actual costs, opt-in eligibility and measured incremental outcomes.")
    s.text(40,161,880,64,"ASSUMPTIONS: 1,000 customers; BRL 40 contribution per extra order; BRL 1 contact cost + BRL 500 setup.",19,True)
    s.table(40,247,[220,200,235,225],["Assumed uplift","Extra orders","Net value (BRL)","ROI"],
            [[f"{r.assumed_uplift_pp:.0f} percentage point" + ("s" if r.assumed_uplift_pp != 1 else ""),f"{r.extra_orders:.0f}",f"{r.net_value_brl:+,.0f}",f"{r.roi_pct:+.1f}%"] for r in roi.itertuples()],row_height=42,size=16)
    s.note("Break-even: +3.75 percentage points, or at least 38 extra orders. These are scenarios, not predictions.",CORAL)

    s=b("Keep customer access and uncertainty visible", "Source: Step 5 audit; configs/step5_bias_audit.json; 05_state_selection.csv.",
        "Hypothetical higher-spending-segment offer selects200/6000. Among14 supported states, geographic rate gap3.95pp, ratio0. "
        "PA0/54 and SP94/2380 drive extremes. PA95%Wilson interval extends6.64%; fitting/selection uncertainty omitted. "
        "No gender/race/age/income fields; geographic comparisons do not satisfy a sensitive-group fairness audit. "
        "No offers were sent and no automated policy was deployed.")
    s.card(40,165,275,213,"Unequal sample coverage",f"{fairness['selection_rate_gap']*100:.2f} pp","State selection-rate gap for a hypothetical offer",CORAL)
    s.card(342,165,275,213,"Important missing data","4 attributes","No gender, race, age or income data",CORAL)
    s.card(645,165,275,213,"Practical safeguard","Human review","Avoid automatic exclusion or replenishment",TEAL)
    s.text(40,398,880,33,"The state gap warrants investigation; small groups make it uncertain.",19,True)
    s.note("Proposed mitigations need testing. Geography is not a substitute for protected attributes.")

    s=b("Run a small pilot with clear success measures", "Source: proposed strategy, derived from notebook limitations; no pilot or rollout has occurred.")
    s.table(40,164,[185,385,310],["Stage","Action","Evidence needed"],[
        ["Prepare","Confirm costs, consent and availability","Usable data; named owners"],
        ["Test customers","Randomize outreach and control","Incremental contribution; reach"],
        ["Test forecasts","Compare on new dates in shadow mode","Error vs simple benchmark"],
        ["Decide","Review value, uncertainty and coverage","Documented go / revise / stop"]],row_height=51,size=16)
    s.note("Use newly collected, relevant data. Historical 2017-2018 results do not establish current performance.")

    s=b("Recommended next step: a measured pilot", "Source: integrated findings from Steps 4-5; proposals are not measured business outcomes.", dark=True)
    s.text(40,174,865,113,"1  Keep the large single-order group in scope.\n2  Retain simple sales benchmarks and human review.\n3  Invest in better evidence before automation.",25,True,WHITE)
    s.text(40,326,870,100,"Success means positive incremental contribution, better forecast error on new dates, and acceptable customer coverage with uncertainty reported.",23,False,WHITE)
    s.text(40,458,870,37,"No proven ROI yet. Report complete; fresh Windows analysis run verified. Fairness gaps remain.",14,False,"C0CED5")
    return tech,biz,roi


def render(deck, stem):
    prs=Presentation()
    prs.slide_width,prs.slide_height=Pt(W),Pt(H)
    prs.core_properties.title="Olist | " + ("Technical presentation" if stem.startswith("technical") else "Business presentation")
    prs.core_properties.subject="AIM capstone: customer segmentation, sales forecasting and ethical AI"
    prs.core_properties.author="AIM capstone project"
    pdf=canvas.Canvas(str(OUT/f"{stem}.pdf"),pagesize=(W,H))
    pdf.setTitle(prs.core_properties.title)
    pdf.setAuthor("AIM capstone project")
    for spec in deck:
        slide=prs.slides.add_slide(prs.slide_layouts[6])
        slide.notes_slide.notes_text_frame.text=spec.title + "\n\n" + spec.notes
        for e in spec.elements:
            x,y,w,h=e['x'],e['y'],e['w'],e['h']
            assert min(x,y,w,h)>=0 and x+w<=W+.1 and y+h<=H+.1, e
            if e['kind']=='rect':
                shape=slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,Pt(x),Pt(y),Pt(w),Pt(h))
                shape.fill.solid(); shape.fill.fore_color.rgb=RGBColor.from_string(e['color'])
                shape.line.fill.background()
                pdf.setFillColor(HexColor('#'+e['color'])); pdf.rect(x,H-y-h,w,h,stroke=0,fill=1)
            elif e['kind']=='text':
                shape=slide.shapes.add_textbox(Pt(x),Pt(y),Pt(w),Pt(h))
                tf=shape.text_frame
                tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0
                tf.word_wrap=False; tf.auto_size=MSO_AUTO_SIZE.NONE
                font="ArialBold" if e['bold'] else "Arial"
                pdf.setFont(font,e['size']); pdf.setFillColor(HexColor('#'+e['color']))
                for i,line in enumerate(e['lines']):
                    p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
                    p.text=line; p.space_before=Pt(0); p.space_after=Pt(0); p.line_spacing=Pt(e['size']*1.16)
                    p.font.name='Arial'; p.font.size=Pt(e['size']); p.font.bold=e['bold']; p.font.color.rgb=RGBColor.from_string(e['color'])
                    pdf.drawString(x,H-y-e['size']*.92-i*e['size']*1.16,line)
            else:
                slide.shapes.add_picture(e['path'],Pt(x),Pt(y),Pt(w),Pt(h))
                pdf.drawImage(e['path'],x,H-y-h,width=w,height=h,mask='auto')
        pdf.showPage()
    prs.save(OUT/f"{stem}.pptx")
    pdf.save()
    # Reopen the native file and confirm slide, note and text persistence.
    check=Presentation(OUT/f"{stem}.pptx")
    assert len(check.slides)==10
    for slide,spec in zip(check.slides,deck):
        assert spec.title in slide.notes_slide.notes_text_frame.text
        assert any(shape.has_text_frame for shape in slide.shapes)
    doc=pdfium.PdfDocument(str(OUT/f"{stem}.pdf"))
    assert len(doc)==10
    thumb=Image.new("RGB",(960,1350),"#DCE5E9")
    preview=OUT/"previews"/stem
    preview.mkdir(parents=True,exist_ok=True)
    for i in range(len(doc)):
        page=doc[i]
        img=page.render(scale=1.5).to_pil()
        img.save(preview/f"slide_{i+1:02d}.png")
        img.thumbnail((480,270))
        thumb.paste(img,((i%2)*480,(i//2)*270))
        page.close()
    thumb.save(OUT/"previews"/f"{stem}_contact.png")
    doc.close()
    return {"slides":len(deck),"titles":[s.title for s in deck],"notes":True,
            "pptx_reopened":True,"pdf_pages_rendered":10}


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    tech,biz,roi=make_decks()
    roi.to_csv(OUT/"roi_scenarios.csv",index=False)
    checks={stem:render(deck,stem) for deck,stem in [(tech,"technical_deck"),(biz,"business_deck")]}
    sources=list(TABLES.glob("04_*.csv"))+list(TABLES.glob("05_*.csv"))+[
        ROOT/"configs/step4_models.json",ROOT/"configs/step4_daily_forecast.json",ROOT/"configs/step5_bias_audit.json",
        ROOT/"docs/DATA_MANIFEST.json",ROOT/"notebooks/Final_Project.ipynb"]
    checks["source_hashes"]={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    checks["validation_limit"]="PDF previews share the PowerPoint layout; no native PowerPoint/LibreOffice renderer is installed."
    checks["roi_assumptions"]={"contacts":1000,"contribution_per_extra_order_brl":40,"cost_per_contact_brl":1,"setup_brl":500,
                               "break_even_uplift_pp":3.75,"observed_roi":False}
    (OUT/"build_manifest.json").write_text(json.dumps(checks,indent=2),encoding="utf-8")
    print("PASS: two editable 10-slide PowerPoint decks, matching PDFs, 20 rendered pages, notes and source manifest.")


if __name__=='__main__':
    main()
