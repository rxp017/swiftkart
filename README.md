# Swiftkart — Power BI report

An offline Power BI report for an Indian quick-commerce business, using generated sample data for January 2023–December 2025.

**Rajashekar Reddy · 24e51a6645**

![Home report](docs/pdf-preview/page-1.png)

## Open the finished dashboard

Download this repository using **Code → Download ZIP**, then extract it. Open [`swiftkart_report.pbix`](swiftkart_report.pbix) in free Power BI Desktop. The file includes the report, semantic model and imported data. No account or publishing is needed.

Use the bottom page tabs to switch pages. Click the year, metric, store-view and city slicers normally; navigation does not depend on buttons. Right-click a city to drill through to its detail page. Clear the incoming City filter in the Filters pane before choosing a different city after drill-through.

[`swiftkart_report.pdf`](swiftkart_report.pdf) provides a static preview without Power BI. The PDF contains five visible pages; the hidden tooltip page remains available in the interactive report.

## What each page answers

| Page | Question |
|---|---|
| Home | How is Swiftkart doing? |
| Customers & Products | Who buys, and what sells? |
| Delivery & Stores | Are we fast and reliable? |
| City deep dive | How is the selected city doing? |
| City locations | Where are Swiftkart's cities? |
| Quick numbers | Three numbers for the hovered selection |

The location view uses an offline latitude/longitude scatter chart, with no online basemap or map-service dependency.

## Edit or refresh the source project

Keep these together:

```text
swiftkart_report.pbip
swiftkart_report.Report/
swiftkart_report.SemanticModel/
data/
generate_data.py
setup_project.py
```

1. Close the PBIP in Desktop before configuring it.
2. Run `python setup_project.py` from the downloaded repository. It sets the five CSV paths to this checkout's location; it uses only Python's standard library.
3. Open `swiftkart_report.pbip` and click **Refresh** to import the local CSVs. A first open may require this refresh because local caches are excluded from GitHub.

The setup script edits only the TMDL CSV paths. It does not modify the PBIX. The finished PBIX opens using its saved data; refreshing it on another computer requires updating the CSV paths through **Transform data → Data source settings**.

To regenerate the dataset:

```shell
python -m pip install -r requirements.txt
python generate_data.py
python setup_project.py
```

Then refresh the PBIP in Desktop. The generator uses seed 42, pandas and NumPy, with 150,000 orders, 20,000 customers, 400 products and 60 stores. It validates keys, relationships and sales calculations.

## Model and verification

The model uses a date/customer/product/store star schema with single-direction relationships and 150 measures. Currency displays use Indian Cr/L/K units. Before submission, live checks covered measure values, total sales versus category sums, global store ranks, city totals and delivery/rating ranges; visible slicers were tested using clicks without Ctrl.

2025: sales ₹25,797,405.179; profit ₹9,776,626.059; 80,667 orders. These are sample figures, not real company performance.

## Report previews

![Customers and products](docs/pdf-preview/page-2.png)

![Delivery and stores](docs/pdf-preview/page-3.png)

![Mumbai detail](docs/pdf-preview/page-4.png)

![City locations](docs/pdf-preview/page-5.png)

## File choices

- PBIX is sufficient to view and interact with the dashboard.
- PBIP plus both definition folders preserves the editable source.
- CSVs are needed for refresh; the generator makes them reproducible.
- PDF and preview images document the result but do not run the dashboard.
- Cache/editor files, working backups, duplicate verification exports and presentation files are excluded from the repository. The PPT is included in the separate submission ZIP.
