# Step 1 Output

Below I treated the article body only, excluding the appendix.
I also collapsed repeated prompts into a single row and flagged them in `notes`.

| article_question_id | language            | question_text                                                                                                                                                                                                                                | is_explicit | notes                                                                                                                                                          |
| ------------------- | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AQ01                | English             | Retrieve the total gross amount and total net amount for all orders placed in March 2022 at the store 'Zava Retail Seattle'                                                                                                                  | TRUE        | Explicitly presented, then asked to the Data Agent.                                                                                                            |
| AQ02                | English             | I need to calculate the net amount, total cost, and profit for products belonging to category PLUMBING in January 2025                                                                                                                       | TRUE        | Explicitly presented and asked to the Data Agent.                                                                                                              |
| AQ03                | English             | I need to calculate the net amount, total cost, and profit for products belonging to category POWER TOOLS in January 2025                                                                                                                    | FALSE       | Implicit variant. The text says to ask the same question again using "POWER TOOLS" instead of "PLUMBING".                                                      |
| AQ04                | English             | I need to calculate overall profit for category PLUMBING in January 2025. Within this category, compute the profit generated only by products of type VALVES, and the percentage of VALVES profit over the total.                            | TRUE        | Explicitly presented and asked to the Data Agent.                                                                                                              |
| AQ05                | English             | Provide month-by-month detail for the 'Angle Stop Valve' product at the Bellevue store in 2024. Show running totals, gross margin and profit change. Flag the month of highest net sales.                                                    | TRUE        | Explicitly presented and asked. Duplicated: later the article says to clear the chat and ask the same question again after adding the store-name instruction.  |
| AQ06                | English             | I need to calculate the net amount, total cost, and profit for pipe related products in January 2025.                                                                                                                                        | TRUE        | Explicitly presented. Treated as a Data Agent prompt because the article then says "If you ask the Data Agent the above question now...".                      |
| AQ07                | Italian             | Devo calcolare l'importo netto, il costo totale e il profitto per i prodotti relativi ai lavandini nel mese di febbraio 2025.                                                                                                                | TRUE        | Explicitly presented and asked. Duplicated: the article later says to ask the same question again in Italian after adding the translate-in/translate-out rule. |
| AQ08                | Italian             | Qual è il prodotto più venduto del 2025 nella categoria degli impianti idraulici?                                                                                                                                                            | TRUE        | Explicitly presented and asked. Duplicated: later the article says to ask the same Italian question again after updating data source instructions.             |
| AQ09                | English             | Provide month-by-month detail for the scrolling jigsaw product at the Bellevue store in 2024. Show running totals, gross margin and profit change. Flag the month of highest net sales.                                                      | TRUE        | Explicitly written later in the article as the English version of the multilingual example. Not a duplicate of AQ05 because the product is different.          |
| AQ10                | French              | Fournissez des détails mensuels pour le produit scrolling jigsaw dans le magasin Bellevue en 2024. Indiquez les totaux cumulés, la marge brute et l'évolution des bénéfices. Signalez le mois où les ventes nettes ont été les plus élevées. | TRUE        | Explicit multilingual prompt shown as actually asked to the Data Agent.                                                                                        |
| AQ11                | Traditional Chinese | 請提供2024年貝爾維尤店 scrolling jigsaw 產品的逐月詳細數據。顯示累計總額、毛利及利潤變動，並標註淨銷售額最高的月份。                                                                                                                                                                        | TRUE        | Explicit multilingual prompt shown as actually asked to the Data Agent.                                                                                        |

A small boundary choice I applied: I included only prompts that the narrative clearly frames as being sent to the Data Agent, and I excluded SQL statements, rhetorical questions, and the appendix copy of the example query.

# Step 2 Output

Here is a compact canonical grouping that merges only where the analytical structure is genuinely the same.

| intent_id | canonical_intent                                                                               | article_questions_included                | short_description                                                                                                                                                         | category_5                 | language_sensitivity |
| --------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- | -------------------- |
| INT01     | Compute gross amount and net amount for a filtered sales slice                                 | AQ01                                      | Aggregate two business-defined sales metrics over a constrained slice of data, typically by store and time period.                                                        | Aggregations               | medium               |
| INT02     | Compute net amount, cost, and profit for a filtered product subset in a time window            | AQ02, AQ03 (implicit variant), AQ06, AQ07 | Return a fixed bundle of three KPIs over a subset of products, where the subset may be defined by exact domain value or by text-based product matching.                   | Multi-metric / comparative | high                 |
| INT03     | Compare total profit vs subset profit and compute subset incidence                             | AQ04                                      | Compute total profit for a broader population, profit for a nested subset, and the percentage contribution of the subset over the total.                                  | Multi-metric / comparative | medium               |
| INT04     | Produce month-by-month product performance for a store with window metrics and peak-month flag | AQ05, AQ09, AQ10, AQ11                    | Build a monthly time series for one product in one store, including running totals, gross margin, period-over-period profit change, and identification of the best month. | Time intelligence          | high                 |
| INT05     | Identify the best-selling product within a category and time period                            | AQ08                                      | Rank products inside a filtered category over a defined period and return the top performer according to a sales criterion.                                               | Group by / ranking         | high                 |

A couple of merge decisions are worth making explicit:

* I merged `AQ02`, `AQ03`, `AQ06`, and `AQ07` because they all share the same core structure: same KPI bundle, same temporal filter, same product-subset restriction. The only thing that changes is how the subset is expressed: category domain value vs text match.
* I kept `AQ01` separate from `INT02` because its semantic focus is not just "aggregate some KPIs", but specifically the business disambiguation of **gross vs net**, which is a different intent family from **net/cost/profit**.
* I grouped `AQ05`, `AQ09`, `AQ10`, and `AQ11` into one intent because they are the same analytical pattern expressed with different entities and languages.

If useful, I can turn this directly into a benchmark-ready TSV with stable intent labels and canonical question templates.

# Step 3 Output

## tables

The file shows these **6 tables** as available in schema `[retail]`: `stores`, `products`, `product_types`, `orders`, `order_items`, `categories`. 

## columns_by_table

### `retail.stores`

* `store_id`
* `store_name`
* `rls_user_id`
* `is_online` 

### `retail.products`

* `product_id`
* `sku`
* `product_name`
* `category_id`
* `type_id`
* `cost`
* `base_price`
* `gross_margin_percent`
* `product_description` 

### `retail.product_types`

* `type_id`
* `category_id`
* `type_name` 

### `retail.orders`

* `order_id`
* `customer_id`
* `store_id`
* `order_date` 

### `retail.order_items`

* `order_item_id`
* `order_id`
* `store_id`
* `product_id`
* `quantity`
* `unit_price`
* `discount_percent`
* `discount_amount`
* `total_amount` 

### `retail.categories`

* `category_id`
* `category_name` 

## sample_entities

### Stores

Useful exact store entities visible in sample rows:

* `Zava Retail Seattle`
* `Zava Retail Bellevue`
* `Zava Retail Tacoma`
* `Zava Retail Spokane`
* `Zava Retail Everett`
* `Zava Retail Redmond`
* `Zava Retail Kirkland`
* `Zava Retail Online`
  Also useful attribute:
* `is_online = 1` only appears for `Zava Retail Online`; the others shown are `0`. 

### Categories

Visible domain values for `category_name`:

* `HAND TOOLS`
* `POWER TOOLS`
* `PAINT & FINISHES`
* `HARDWARE`
* `LUMBER & BUILDING MATERIALS`
* `ELECTRICAL`
* `PLUMBING`
* `GARDEN & OUTDOOR`
* `STORAGE & ORGANIZATION` 

### Product types

Visible sample domain values for `type_name`:

* `HAMMERS`
* `SCREWDRIVERS`
* `WRENCHES`
* `PLIERS`
* `HAND SAWS`
* `CHISELS`
* `FILES & RASPS`
* `MEASURING TOOLS`
* `ALLEN KEYS`
* `DRILLS`
* `CIRCULAR SAWS`
* `SANDERS`
* `JIGSAWS`
* `ANGLE GRINDERS`
* `RECIPROCATING SAWS`
* `ROUTERS`
* `IMPACT DRIVERS`
* `BELT SANDERS`
* `MITER SAWS`
* `INTERIOR PAINT`
  These are only the sample rows shown for `product_types`, not necessarily the full domain. 

### Products

Good benchmark-ready product entities explicitly shown:

* `Flathead Screwdriver Set`
* `Wood Rasp Set`
* `Tape Measure 25-foot`
* `Weather Resistant Outlet`
* `Weatherproof Box`
* `PVC Elbow Assortment`
* `Ball Valve 1/2-inch`
* `Fill Valve Assembly`
* `Plunger Set`
* `Fiberglass Pipe Insulation`
* `Tomato Plant Food`
* `Straw Mulch Bale`
* `Vegetable Seed Starter Kit`
* `Garden Soil Enriched`
* `Clear Storage Bin 27-Quart`
* `Magnetic Tool Holder`
* `Finishing Hammer 13oz`
* `Lineman's Pliers 9-inch`
* `USB Outlet with Charging`
* `Motion Sensor Switch` 

### Useful description keywords for text-filter questions

Terms clearly present in `product_description` that can support realistic LIKE-style questions:

* `flathead`
* `precision-machined`
* `weather resistant`
* `weatherproof`
* `PVC`
* `valve`
* `toilet`
* `sink`
* `plunger`
* `drain`
* `pipe`
* `tomato`
* `vegetable`
* `soil`
* `storage`
* `magnetic`
* `USB`
* `motion`
* `electrical`
* `outdoor` 

### Time values visible in sample rows

Useful benchmark periods directly evidenced by sample data:

* years visible in `orders.order_date`: `2020`, `2022`, `2023`, `2024`, `2025`, `2026`
* example exact months visible include `2020-05`, `2020-06`, `2022-04`, `2022-08`, `2022-11`, `2022-12`, `2023-02`, `2023-09`, `2023-10`, `2024-03`, `2024-11`, `2025-01`, `2025-08`, `2025-09`, `2026-02`, `2026-05`, `2026-06`, `2026-10` 

### Measures that can support realistic analytical questions

From `order_items` and `products`, the file clearly supports questions involving:

* `quantity`
* `unit_price`
* `discount_percent`
* `discount_amount`
* `total_amount`
* `cost`
* `base_price`
* `gross_margin_percent` 

## benchmark_constraints

1. **Only 6 tables are evidenced by the file**
   Benchmark questions should stay within `stores`, `products`, `product_types`, `orders`, `order_items`, `categories`. No other tables are supported by this file. 

2. **Sample rows are partial, not exhaustive**
   The file is explicitly a schema plus top rows view. It is safe to use shown entities as realistic examples, but unsafe to assume that the displayed rows represent the full domain or the true distribution of the data. 

3. **`categories` looks complete, `product_types` does not**
   `categories` shows 9 values and appears complete in the sample. `product_types` shows only the first 20 rows, so benchmark prompts should not assume the file exposes the full list of type values. 

4. **Joins are structurally clear, but sample-row continuity is not guaranteed**
   The schema supports obvious joins:

   * `orders.store_id -> stores.store_id`
   * `order_items.order_id -> orders.order_id`
   * `order_items.product_id -> products.product_id`
   * `products.category_id -> categories.category_id`
   * `products.type_id -> product_types.type_id`
     However, the displayed top rows are table-local samples, so a shown product/store/date is not guaranteed to co-occur in the shown rows of other tables. 

5. **Exact literals should match visible values**
   For realistic benchmark questions, prefer exact names that are explicitly shown, such as:

   * store names like `Zava Retail Bellevue`
   * category names like `PLUMBING`
   * product names like `Ball Valve 1/2-inch`
     This avoids inventing entities not evidenced by the file. 

6. **Text-filter questions should rely on visible description vocabulary**
   Questions like "pipe-related", "sink-related", "weatherproof", or "tomato-related" are well grounded because those strings appear in `product_description` samples. 

7. **Time-based questions should stay within years proven by the file**
   The sample dates show activity across `2020` to `2026`. Questions outside that range would not be grounded by the file. 

8. **Customer-level benchmarking is weakly grounded**
   `customer_id` exists in `orders`, but no customer table or customer attributes are shown. So customer segmentation or customer-profile questions are not well supported by this file alone. 

9. **RLS-related questions are weakly grounded**
   `rls_user_id` exists in `stores`, but the file gives no user table, no mapping logic, and only raw GUID-like values. So realistic benchmark questions should avoid detailed user-identity semantics. 

10. **Most reliable benchmark area**
    The most clearly supported benchmark space is retail analytics around:

    * store
    * date/time
    * category
    * product type
    * product
    * quantity / sales / discounts / net amount / cost / margin-related measures. 

# Step 4 Output

| intent_id | supported_yes_no | required_tables                                                                                       | changes_needed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | revised_canonical_question                                                                                                                                                                                             |
| --------- | ---------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| INT01     | Yes              | `retail.orders`, `retail.order_items`, `retail.stores`                                                | The intent is fully supported. The original example uses `Zava Retail Seattle`, which is visible in the file, so no entity replacement is strictly required. If you want a month/store combination that is more tightly grounded in the sample rows, a safer example is `Zava Retail Kirkland` in `January 2025`, because both are explicitly visible in the file.                                                                                                                                                            | Retrieve the total gross amount and total net amount for all orders placed in January 2025 at the store 'Zava Retail Kirkland'.                                                                                        |
| INT02     | Yes              | `retail.orders`, `retail.order_items`, `retail.products`, `retail.categories`                         | The intent is fully supported. Category-based variants are supported through `products -> categories`; text-filter variants are supported through `products.product_description`. Visible examples that should be preferred are category values such as `PLUMBING` and `POWER TOOLS`, and text terms such as `pipe` and `sink`, all explicitly visible in the file. The Italian sink-related version used `February 2025`, which is not explicitly visible in the sample dates, so `January 2025` is a safer benchmark month. | I need to calculate the net amount, total cost, and profit for products belonging to category PLUMBING in January 2025.                                                                                                |
| INT03     | Yes              | `retail.orders`, `retail.order_items`, `retail.products`, `retail.categories`, `retail.product_types` | The intent is fully supported structurally, but the original subset value `VALVES` is **not explicitly visible** in the file’s `product_types` sample rows. To keep the same analytical structure and stay fully grounded in visible values, replace `PLUMBING / VALVES` with a visible category/type pair such as `POWER TOOLS / JIGSAWS`.                                                                                                                                                                                   | I need to calculate overall profit for category POWER TOOLS in January 2025. Within this category, compute the profit generated only by products of type JIGSAWS, and the percentage of JIGSAWS profit over the total. |
| INT04     | Yes              | `retail.orders`, `retail.order_items`, `retail.products`, `retail.stores`                             | The intent is fully supported. The issue is only with entity grounding: `Angle Stop Valve` and `scrolling jigsaw` are **not explicitly visible** in the file. Replace them with visible product names such as `Ball Valve 1/2-inch`, `Tomato Plant Food`, or `Clear Storage Bin 27-Quart`. The store `Bellevue` is visible as `Zava Retail Bellevue`, so it can be kept.                                                                                                                                                      | Provide month-by-month detail for the 'Ball Valve 1/2-inch' product at the Bellevue store in 2024. Show running totals, gross margin and profit change. Flag the month of highest net sales.                           |
| INT05     | Yes              | `retail.orders`, `retail.order_items`, `retail.products`, `retail.categories`                         | The intent is fully supported. The original Italian business phrasing `impianti idraulici` is not a stored domain value and should be normalized to the visible category value `PLUMBING`. The year `2025` is visible in the sample rows, so it can be kept.                                                                                                                                                                                                                                                                  | What is the best-selling product in 2025 in category PLUMBING?                                                                                                                                                         |

A couple of practical takeaways emerge from this alignment:

* All five canonical intents are supported by the real six-table perimeter.
* The main corrections are not structural but lexical: replacing article-only entities with names or domain values that are actually visible in the file.
* The weakest original benchmark element is `VALVES` as a visible `product_types` value, because that exact value does not appear in the provided sample rows.

# Step 5 Output

Assuming `ARTICLE_CORE` here corresponds to the five canonical intents extracted from the article body (`INT01` to `INT05`), this is the reusable metric catalog and its assignment.

| intent_id | metric_definition                                | formal_definition                                                                                                                                                                                                                                                                                  | notes                                                                                                                                                                                                                                                                                                            |
| --------- | ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| INT01     | `total_gross_amount`, `total_net_amount`         | `total_gross_amount = SUM(order_items.quantity * order_items.unit_price)` ; `total_net_amount = SUM(order_items.total_amount)`                                                                                                                                                                     | Reusable labels proposed here: `total_gross_amount`, `total_net_amount`, `total_cost`, `profit`, `gross_margin_pct`, `subset_profit_pct`, `best_selling_by_quantity`. This intent is the pure gross vs net aggregation pattern.                                                                                  |
| INT02     | `total_net_amount`, `total_cost`, `profit`       | `total_net_amount = SUM(order_items.total_amount)` ; `total_cost = SUM(products.cost * order_items.quantity)` ; `profit = SUM(order_items.total_amount - products.cost * order_items.quantity)`                                                                                                    | This is the standard KPI bundle for filtered product subsets, whether the filter is a category/domain value or a text match on product description.                                                                                                                                                              |
| INT03     | `profit`, `subset_profit_pct`                    | `profit = SUM(order_items.total_amount - products.cost * order_items.quantity)` ; `subset_profit_pct = SUM(CASE WHEN <subset_condition> THEN (order_items.total_amount - products.cost * order_items.quantity) ELSE 0 END) / SUM(order_items.total_amount - products.cost * order_items.quantity)` | `subset_profit_pct` should normally be returned as a percentage value if user-facing output requires it: multiply by `100.0`. Numerator = subset profit, denominator = overall profit within the parent filter scope.                                                                                            |
| INT04     | `total_net_amount`, `profit`, `gross_margin_pct` | `total_net_amount = SUM(order_items.total_amount)` ; `profit = SUM(order_items.total_amount - products.cost * order_items.quantity)` ; `gross_margin_pct = SUM(order_items.total_amount - products.cost * order_items.quantity) / NULLIF(SUM(order_items.total_amount), 0)`                        | For this monthly time-series intent, these metrics are typically computed per month. If displayed as a percentage, `gross_margin_pct` can be multiplied by `100.0`. "Profit change" is not a base metric label here: it is a time delta over `profit`, for example `profit - LAG(profit) OVER (ORDER BY month)`. |
| INT05     | `best_selling_by_quantity`                       | `best_selling_by_quantity = product with MAX(SUM(order_items.quantity)) within the requested filter scope`                                                                                                                                                                                         | Recommended deterministic tie-breaker: first `SUM(order_items.quantity)` descending, then `SUM(order_items.total_amount)` descending, then `product_name` ascending. This keeps "best-selling" stable and explicit.                                                                                              |

A clean reusable metric label set from this would be:

`total_gross_amount`
`total_net_amount`
`total_cost`
`profit`
`gross_margin_pct`
`subset_profit_pct`
`best_selling_by_quantity`

If you want, I can convert this into a benchmark-ready mapping table keyed by `intent_id` and `metric_definition_id`.

# Step 6 Output

Below are **13 additional intents** (`EXT01` to `EXT13`).
Combined with the **5 validated ARTICLE_CORE intents**, they bring the benchmark to **18 total intents**.

| intent_id | canonical_intent                                                    | category_5                   | language_sensitivity | required_tables                                                                                       | canonical_question                                                                                                     | expected_answer_type      | comparison_mode    | metric_definition                                                  |
| --------- | ------------------------------------------------------------------- | ---------------------------- | -------------------- | ----------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------- | ------------------ | ------------------------------------------------------------------ |
| EXT01     | Store with highest total net amount in a year                       | Group by / ranking           | medium               | `retail.orders`, `retail.order_items`, `retail.stores`                                                | Which store had the highest Total Net Amount in 2025?                                                                  | single ranked entity      | ranking_desc       | `total_net_amount`                                                 |
| EXT02     | Top N products by total net amount within a category and year       | Group by / ranking           | medium               | `retail.orders`, `retail.order_items`, `retail.products`, `retail.categories`                         | What are the top 5 products by Total Net Amount in category PLUMBING in 2025?                                          | ranked list               | ranking_desc       | `total_net_amount`                                                 |
| EXT03     | Net amount and profit by product type within a category             | Multi-metric / comparative   | medium               | `retail.orders`, `retail.order_items`, `retail.products`, `retail.product_types`, `retail.categories` | Show Total Net Amount and Profit by product type for category POWER TOOLS in 2025.                                     | grouped table             | group_breakdown    | `total_net_amount`, `profit`                                       |
| EXT04     | Compare online versus physical channel performance in a time window | Multi-metric / comparative   | medium               | `retail.orders`, `retail.order_items`, `retail.products`, `retail.stores`                             | Compare Total Net Amount and Profit between the online store and physical stores in January 2025.                      | comparative summary table | channel_comparison | `total_net_amount`, `profit`                                       |
| EXT05     | Monthly net amount and order count for a store                      | Time intelligence            | medium               | `retail.orders`, `retail.order_items`, `retail.stores`                                                | Show month-by-month Total Net Amount and order count for Zava Retail Bellevue in 2025.                                 | monthly table             | time_trend         | `total_net_amount`, `order_count`                                  |
| EXT06     | Highest-profit category within a store and year                     | Group by / ranking           | medium               | `retail.orders`, `retail.order_items`, `retail.products`, `retail.categories`, `retail.stores`        | Which category generated the highest Profit at Zava Retail Seattle in 2025?                                            | single ranked entity      | ranking_desc       | `profit`                                                           |
| EXT07     | Gross, net, and discount impact by category in a month              | Multi-metric / comparative   | medium               | `retail.orders`, `retail.order_items`, `retail.products`, `retail.categories`                         | Show Total Gross Amount, Total Net Amount, and discount impact amount by category in January 2025.                     | grouped table             | group_breakdown    | `total_gross_amount`, `total_net_amount`, `discount_impact_amount` |
| EXT08     | Category with highest average discount percent in a month           | Group by / ranking           | medium               | `retail.orders`, `retail.order_items`, `retail.products`, `retail.categories`                         | Which category had the highest average discount percent in January 2025?                                               | single ranked entity      | ranking_desc       | `avg_discount_pct`                                                 |
| EXT09     | Year-over-year comparison for a specific product                    | Time intelligence            | high                 | `retail.orders`, `retail.order_items`, `retail.products`                                              | Compare Total Net Amount for the product 'Ball Valve 1/2-inch' between 2024 and 2025.                                  | two-period comparison     | period_over_period | `total_net_amount`                                                 |
| EXT10     | Share of category net amount contributed by a specific product      | Multi-metric / comparative   | high                 | `retail.orders`, `retail.order_items`, `retail.products`, `retail.categories`                         | In January 2025, what percentage of Total Net Amount in category PLUMBING came from the product 'Ball Valve 1/2-inch'? | scalar percentage         | share_of_total     | `net_amount_share_pct`, `total_net_amount`                         |
| EXT11     | Rank products inside a text-defined subset                          | Text filters / domain values | high                 | `retail.orders`, `retail.order_items`, `retail.products`                                              | What are the top 3 pipe-related products by Profit in 2025?                                                            | ranked list               | ranking_desc       | `profit`                                                           |
| EXT12     | Peak month for the online store by net amount                       | Time intelligence            | medium               | `retail.orders`, `retail.order_items`, `retail.stores`                                                | For Zava Retail Online in 2025, which month had the highest Total Net Amount?                                          | single period answer      | peak_period        | `total_net_amount`                                                 |
| EXT13     | Quarterly net amount trend for a category                           | Time intelligence            | medium               | `retail.orders`, `retail.order_items`, `retail.products`, `retail.categories`                         | Show Total Net Amount by quarter for category GARDEN & OUTDOOR in 2025.                                                | quarterly table           | time_trend         | `total_net_amount`                                                 |

A few design choices behind this set:

* It stays fully inside the six visible tables.
* It avoids semantic duplication of the ARTICLE_CORE patterns:

  * no repeat of gross vs net at store-month aggregate only
  * no repeat of the exact `net + cost + profit` filtered subset bundle
  * no repeat of the `subset profit percentage` pattern
  * no repeat of the product/store monthly windowing pattern with running totals and profit deltas
  * no repeat of `best-selling by quantity within category`
* It covers all five benchmark families:

  * **Aggregations** are embedded through scalar and grouped KPI requests
  * **Group by / ranking**: `EXT01`, `EXT02`, `EXT06`, `EXT08`
  * **Time intelligence**: `EXT05`, `EXT09`, `EXT12`, `EXT13`
  * **Text filters / domain values**: `EXT11`
  * **Multi-metric / comparative**: `EXT03`, `EXT04`, `EXT07`, `EXT10`

If you want, I can now assemble the full **18-intent master table** with both `ARTICLE_CORE` and `SCHEMA_EXTENDED` in one benchmark-ready format.

# Step 7 Output

Checked: the catalog below has **18 intents total** (`5 ARTICLE_CORE + 13 SCHEMA_EXTENDED`), uses only the **6 available tables**, avoids semantic duplicates, and keeps a clear split between **taught anchor cases** and **generalization probes**.

| benchmark_split | intent_id | source_type         | canonical_intent                                                            | category_5                   | language_sensitivity | required_tables                                                                               | canonical_question                                                                                                                                                                                                     | expected_answer_type   | comparison_mode         | metric_definition                                                                                                    | notes                                                                                                                                           |
| --------------- | --------- | ------------------- | --------------------------------------------------------------------------- | ---------------------------- | -------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- | ----------------------- | -------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| ARTICLE_CORE    | INT01     | taught_case         | Gross vs net for a filtered sales slice                                     | Aggregations                 | medium               | `retail.orders, retail.order_items, retail.stores`                                            | Retrieve the Total Gross Amount and Total Net Amount for all orders placed in January 2025 at the store 'Zava Retail Kirkland'.                                                                                        | scalar_pair            | none                    | `total_gross_amount, total_net_amount`                                                                               | Core taught metric-definition case. Uses visible store name.                                                                                    |
| ARTICLE_CORE    | INT02     | taught_case         | Net amount, cost, and profit for a filtered product subset in a time window | Multi-metric / comparative   | high                 | `retail.orders, retail.order_items, retail.products, retail.categories`                       | I need to calculate the Total Net Amount, Total Cost, and Profit for products belonging to category PLUMBING in January 2025.                                                                                          | scalar_triple          | none                    | `total_net_amount, total_cost, profit`                                                                               | Core taught KPI bundle. Domain-value variant anchored on visible category.                                                                      |
| ARTICLE_CORE    | INT03     | taught_case         | Total profit vs subset profit inside a parent scope                         | Multi-metric / comparative   | medium               | `retail.orders, retail.order_items, retail.products, retail.categories, retail.product_types` | I need to calculate overall Profit for category POWER TOOLS in January 2025. Within this category, compute the Profit generated only by products of type JIGSAWS, and the percentage of JIGSAWS Profit over the total. | scalar_plus_percentage | subset_vs_total         | `profit, subset_profit_pct`                                                                                          | Replaces non-visible `VALVES` with visible `JIGSAWS` while preserving structure.                                                                |
| ARTICLE_CORE    | INT04     | taught_case         | Month-by-month product performance for a store with window metrics          | Time intelligence            | high                 | `retail.orders, retail.order_items, retail.products, retail.stores`                           | Provide month-by-month detail for the 'Ball Valve 1/2-inch' product at the Bellevue store in 2024. Show running totals, gross margin and profit change. Flag the month of highest Total Net Amount.                    | monthly_table          | time_trend_with_windows | `total_net_amount, running_total_net_amount, gross_margin_pct, profit, profit_delta, peak_month_by_total_net_amount` | Preserves the article pattern with visible product and store entities.                                                                          |
| ARTICLE_CORE    | INT05     | taught_case         | Best-selling product within a category and time period                      | Group by / ranking           | high                 | `retail.orders, retail.order_items, retail.products, retail.categories`                       | What is the best-selling product in 2025 in category PLUMBING?                                                                                                                                                         | top1_entity            | ranking_desc            | `best_selling_by_quantity`                                                                                           | Core taught ranking case. Best-selling is defined by quantity.                                                                                  |
| SCHEMA_EXTENDED | EXT01     | generalization_case | Store with highest Total Net Amount in a year                               | Group by / ranking           | medium               | `retail.orders, retail.order_items, retail.stores`                                            | Which store had the highest Total Net Amount in 2025?                                                                                                                                                                  | top1_entity            | ranking_desc            | `total_net_amount`                                                                                                   | Generalizes from store filtering to store ranking.                                                                                              |
| SCHEMA_EXTENDED | EXT02     | generalization_case | Top N products by Total Net Amount within a category and year               | Group by / ranking           | medium               | `retail.orders, retail.order_items, retail.products, retail.categories`                       | What are the top 5 products by Total Net Amount in category PLUMBING in 2025?                                                                                                                                          | ranked_list            | ranking_desc            | `total_net_amount`                                                                                                   | Distinct from INT05 because metric is net amount, not quantity, and output is top 5.                                                            |
| SCHEMA_EXTENDED | EXT03     | generalization_case | Net amount and Profit by product type within a category                     | Multi-metric / comparative   | medium               | `retail.orders, retail.order_items, retail.products, retail.product_types, retail.categories` | Show Total Net Amount and Profit by product type for category POWER TOOLS in 2025.                                                                                                                                     | grouped_table          | group_breakdown         | `total_net_amount, profit`                                                                                           | Tests grouped multi-metric breakdown, not subset percentage.                                                                                    |
| SCHEMA_EXTENDED | EXT04     | generalization_case | Compare online versus physical channel performance in a time window         | Multi-metric / comparative   | medium               | `retail.orders, retail.order_items, retail.products, retail.stores`                           | Compare Total Net Amount and Profit between the online store and physical stores in January 2025.                                                                                                                      | comparative_summary    | channel_comparison      | `total_net_amount, profit`                                                                                           | Uses `stores.is_online` / visible online store concept.                                                                                         |
| SCHEMA_EXTENDED | EXT05     | generalization_case | Monthly Total Net Amount and order count for a store                        | Time intelligence            | medium               | `retail.orders, retail.order_items, retail.stores`                                            | Show month-by-month Total Net Amount and order count for Zava Retail Bellevue in 2025.                                                                                                                                 | monthly_table          | time_trend              | `total_net_amount, order_count`                                                                                      | Time trend at store level, distinct from INT04 product-level window analysis.                                                                   |
| SCHEMA_EXTENDED | EXT06     | generalization_case | Highest-Profit category within a store and year                             | Group by / ranking           | medium               | `retail.orders, retail.order_items, retail.products, retail.categories, retail.stores`        | Which category generated the highest Profit at Zava Retail Seattle in 2025?                                                                                                                                            | top1_entity            | ranking_desc            | `profit`                                                                                                             | Ranking over categories inside a store slice.                                                                                                   |
| SCHEMA_EXTENDED | EXT07     | generalization_case | Gross, net, and discount impact by category in a month                      | Multi-metric / comparative   | medium               | `retail.orders, retail.order_items, retail.products, retail.categories`                       | Show Total Gross Amount, Total Net Amount, and discount impact amount by category in January 2025.                                                                                                                     | grouped_table          | group_breakdown         | `total_gross_amount, total_net_amount, discount_impact_amount`                                                       | `discount_impact_amount = total_gross_amount - total_net_amount`. Distinct from INT01 because grouped by category and includes discount impact. |
| SCHEMA_EXTENDED | EXT08     | generalization_case | Category with highest average discount percent in a month                   | Group by / ranking           | medium               | `retail.orders, retail.order_items, retail.products, retail.categories`                       | Which category had the highest average discount percent in January 2025?                                                                                                                                               | top1_entity            | ranking_desc            | `avg_discount_pct`                                                                                                   | Tests discount-based ranking rather than revenue or profit ranking.                                                                             |
| SCHEMA_EXTENDED | EXT09     | generalization_case | Year-over-year Total Net Amount comparison for a specific product           | Time intelligence            | high                 | `retail.orders, retail.order_items, retail.products`                                          | Compare Total Net Amount for the product 'Ball Valve 1/2-inch' between 2024 and 2025.                                                                                                                                  | period_comparison      | period_over_period      | `total_net_amount`                                                                                                   | Uses visible product name. Tests entity precision plus year-over-year logic.                                                                    |
| SCHEMA_EXTENDED | EXT10     | generalization_case | Share of category Total Net Amount contributed by a specific product        | Multi-metric / comparative   | high                 | `retail.orders, retail.order_items, retail.products, retail.categories`                       | In January 2025, what percentage of Total Net Amount in category PLUMBING came from the product 'Ball Valve 1/2-inch'?                                                                                                 | scalar_percentage      | share_of_total          | `total_net_amount, net_amount_share_pct`                                                                             | Distinct from INT03 because it uses net amount share, not profit share of a type subset.                                                        |
| SCHEMA_EXTENDED | EXT11     | generalization_case | Rank products inside a text-defined subset                                  | Text filters / domain values | high                 | `retail.orders, retail.order_items, retail.products`                                          | What are the top 3 pipe-related products by Profit in 2025?                                                                                                                                                            | ranked_list            | ranking_desc            | `profit`                                                                                                             | Tests text filtering on `product_description` plus ranking.                                                                                     |
| SCHEMA_EXTENDED | EXT12     | generalization_case | Peak month for the online store by Total Net Amount                         | Time intelligence            | medium               | `retail.orders, retail.order_items, retail.stores`                                            | For Zava Retail Online in 2025, which month had the highest Total Net Amount?                                                                                                                                          | peak_period            | peak_period             | `total_net_amount`                                                                                                   | Time intelligence at channel/store level, distinct from full monthly breakdown.                                                                 |
| SCHEMA_EXTENDED | EXT13     | generalization_case | Quarterly Total Net Amount trend for a category                             | Time intelligence            | medium               | `retail.orders, retail.order_items, retail.products, retail.categories`                       | Show Total Net Amount by quarter for category GARDEN & OUTDOOR in 2025.                                                                                                                                                | quarterly_table        | time_trend              | `total_net_amount`                                                                                                   | Tests quarter grain and category aggregation.                                                                                                   |

### Validation summary

* **No semantic duplicates**: each intent differs by at least one of these dimensions: metric family, grouping grain, ranking target, comparison logic, time grain, or filter semantics.
* **Supported by available tables only**: every row uses only `stores`, `products`, `product_types`, `orders`, `order_items`, `categories`.
* **Balanced split**:

  * `ARTICLE_CORE` keeps the main taught patterns from the article: metric definitions, subset logic, multilingual-sensitive entity handling, and complex month-level output.
  * `SCHEMA_EXTENDED` expands into adjacent but distinct tasks: ranking, grouped breakdowns, year-over-year, share-of-total, discount logic, quarterly aggregation, and channel comparison.

If you want, the next clean step is to convert this catalog into the master benchmark table with `question_id`, paraphrase families, and `required_tables` already normalized as TSV-ready strings.

# Step 8 Output

| intent_id | question_id | variant_type     | question                                                                                                                                                                                                                                            |
| --------- | ----------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| INT01     | INT01_CAN   | canonical        | Recupera il Total Gross Amount e il Total Net Amount di tutti gli ordini effettuati a gennaio 2025 nel punto vendita 'Zava Retail Kirkland'.                                                                                                        |
| INT01     | INT01_COL   | sales_colloquial | Mi servono il Total Gross Amount e il Total Net Amount di tutti gli ordini di gennaio 2025 su 'Zava Retail Kirkland'.                                                                                                                               |
| INT01     | INT01_EXE   | sales_executive  | Quali sono il Total Gross Amount e il Total Net Amount generati nel mese di gennaio 2025 dal punto vendita 'Zava Retail Kirkland'?                                                                                                                  |
| INT01     | INT01_IMP   | sales_implicit   | Per gennaio 2025, quanto hanno fatto in totale lordo e netto gli ordini di 'Zava Retail Kirkland'?                                                                                                                                                  |
| INT02     | INT02_CAN   | canonical        | Calcola il Total Net Amount, il Total Cost e il Profit per i prodotti della categoria PLUMBING nel mese di gennaio 2025.                                                                                                                            |
| INT02     | INT02_COL   | sales_colloquial | Mi dai Total Net Amount, Total Cost e Profit della categoria PLUMBING a gennaio 2025?                                                                                                                                                               |
| INT02     | INT02_EXE   | sales_executive  | Qual è il contributo della categoria PLUMBING nel mese di gennaio 2025 in termini di Total Net Amount, Total Cost e Profit?                                                                                                                         |
| INT02     | INT02_IMP   | sales_implicit   | Su PLUMBING, a gennaio 2025, quanto abbiamo fatto di netto, costo e profitto?                                                                                                                                                                       |
| INT03     | INT03_CAN   | canonical        | Calcola il Profit complessivo della categoria POWER TOOLS nel mese di gennaio 2025. All'interno della categoria, calcola anche il Profit generato solo dai prodotti di tipo JIGSAWS e la percentuale del Profit di JIGSAWS sul totale.              |
| INT03     | INT03_COL   | sales_colloquial | Mi servono il Profit totale di POWER TOOLS a gennaio 2025, il Profit dei soli JIGSAWS e il peso percentuale dei JIGSAWS sul totale.                                                                                                                 |
| INT03     | INT03_EXE   | sales_executive  | Nel mese di gennaio 2025, qual è il Profit complessivo della categoria POWER TOOLS, quanto ne deriva dal tipo JIGSAWS e quale quota percentuale rappresenta sul totale?                                                                             |
| INT03     | INT03_IMP   | sales_implicit   | Per POWER TOOLS a gennaio 2025, quanto vale il Profit totale e quanto incidono i JIGSAWS in valore e in percentuale?                                                                                                                                |
| INT04     | INT04_CAN   | canonical        | Fornisci il dettaglio mese per mese del prodotto 'Ball Valve 1/2-inch' nel punto vendita 'Zava Retail Bellevue' nel 2024. Mostra i totali cumulati, il gross margin e la variazione del Profit. Evidenzia il mese con il Total Net Amount più alto. |
| INT04     | INT04_COL   | sales_colloquial | Mi fai il mese per mese del prodotto 'Ball Valve 1/2-inch' su 'Zava Retail Bellevue' nel 2024, con cumulato, gross margin, variazione di Profit e il mese migliore per Total Net Amount?                                                            |
| INT04     | INT04_EXE   | sales_executive  | Per il 2024, voglio una vista mensile del prodotto 'Ball Valve 1/2-inch' nel punto vendita 'Zava Retail Bellevue', con totali cumulati, gross margin, delta di Profit e segnalazione del mese con il Total Net Amount massimo.                      |
| INT04     | INT04_IMP   | sales_implicit   | Nel 2024, come si è mosso mese per mese 'Ball Valve 1/2-inch' su 'Zava Retail Bellevue', con cumulato, margine, cambio di Profit e mese top per Total Net Amount?                                                                                   |
| INT05     | INT05_CAN   | canonical        | Qual è il prodotto più venduto nel 2025 nella categoria PLUMBING?                                                                                                                                                                                   |
| INT05     | INT05_COL   | sales_colloquial | Nel 2025, qual è stato il prodotto più venduto in PLUMBING?                                                                                                                                                                                         |
| INT05     | INT05_EXE   | sales_executive  | Quale prodotto guida le vendite della categoria PLUMBING nel 2025?                                                                                                                                                                                  |
| INT05     | INT05_IMP   | sales_implicit   | In PLUMBING, nel 2025, chi è il best seller?                                                                                                                                                                                                        |
| EXT01     | EXT01_CAN   | canonical        | Quale punto vendita ha registrato il Total Net Amount più alto nel 2025?                                                                                                                                                                            |
| EXT01     | EXT01_COL   | sales_colloquial | Nel 2025, quale store ha fatto il Total Net Amount più alto?                                                                                                                                                                                        |
| EXT01     | EXT01_EXE   | sales_executive  | Qual è il punto vendita leader per Total Net Amount nel 2025?                                                                                                                                                                                       |
| EXT01     | EXT01_IMP   | sales_implicit   | Chi è stato il miglior store del 2025 per Total Net Amount?                                                                                                                                                                                         |
| EXT02     | EXT02_CAN   | canonical        | Quali sono i top 5 prodotti per Total Net Amount nella categoria PLUMBING nel 2025?                                                                                                                                                                 |
| EXT02     | EXT02_COL   | sales_colloquial | Mi dai i primi 5 prodotti di PLUMBING per Total Net Amount nel 2025?                                                                                                                                                                                |
| EXT02     | EXT02_EXE   | sales_executive  | Nel 2025, quali sono i 5 prodotti con il Total Net Amount più alto nella categoria PLUMBING?                                                                                                                                                        |
| EXT02     | EXT02_IMP   | sales_implicit   | Su PLUMBING nel 2025, quali sono i 5 prodotti che hanno portato più Total Net Amount?                                                                                                                                                               |
| EXT03     | EXT03_CAN   | canonical        | Mostra il Total Net Amount e il Profit per tipo prodotto nella categoria POWER TOOLS nel 2025.                                                                                                                                                      |
| EXT03     | EXT03_COL   | sales_colloquial | Mi fai il breakdown per tipo prodotto di POWER TOOLS nel 2025 con Total Net Amount e Profit?                                                                                                                                                        |
| EXT03     | EXT03_EXE   | sales_executive  | Per la categoria POWER TOOLS nel 2025, voglio vedere Total Net Amount e Profit per ciascun tipo prodotto.                                                                                                                                           |
| EXT03     | EXT03_IMP   | sales_implicit   | Dentro POWER TOOLS nel 2025, come si distribuiscono Total Net Amount e Profit per tipo prodotto?                                                                                                                                                    |
| EXT04     | EXT04_CAN   | canonical        | Confronta il Total Net Amount e il Profit tra 'Zava Retail Online' e i punti vendita fisici nel mese di gennaio 2025.                                                                                                                               |
| EXT04     | EXT04_COL   | sales_colloquial | A gennaio 2025, mi confronti Total Net Amount e Profit tra 'Zava Retail Online' e i negozi fisici?                                                                                                                                                  |
| EXT04     | EXT04_EXE   | sales_executive  | Nel mese di gennaio 2025, qual è il confronto tra 'Zava Retail Online' e i punti vendita fisici in termini di Total Net Amount e Profit?                                                                                                            |
| EXT04     | EXT04_IMP   | sales_implicit   | A gennaio 2025, 'Zava Retail Online' ha performato meglio o peggio dei negozi fisici su Total Net Amount e Profit?                                                                                                                                  |
| EXT05     | EXT05_CAN   | canonical        | Mostra mese per mese il Total Net Amount e il numero ordini per 'Zava Retail Bellevue' nel 2025.                                                                                                                                                    |
| EXT05     | EXT05_COL   | sales_colloquial | Mi fai il mese per mese di 'Zava Retail Bellevue' nel 2025 con Total Net Amount e numero ordini?                                                                                                                                                    |
| EXT05     | EXT05_EXE   | sales_executive  | Per 'Zava Retail Bellevue' voglio vedere nel 2025 l'andamento mensile di Total Net Amount e numero ordini.                                                                                                                                          |
| EXT05     | EXT05_IMP   | sales_implicit   | Nel 2025, come è andata mese per mese 'Zava Retail Bellevue' tra Total Net Amount e volumi ordini?                                                                                                                                                  |
| EXT06     | EXT06_CAN   | canonical        | Quale categoria ha generato il Profit più alto nel punto vendita 'Zava Retail Seattle' nel 2025?                                                                                                                                                    |
| EXT06     | EXT06_COL   | sales_colloquial | Nel 2025, qual è la categoria con più Profit su 'Zava Retail Seattle'?                                                                                                                                                                              |
| EXT06     | EXT06_EXE   | sales_executive  | Nel punto vendita 'Zava Retail Seattle', quale categoria è stata la migliore per Profit nel 2025?                                                                                                                                                   |
| EXT06     | EXT06_IMP   | sales_implicit   | Su 'Zava Retail Seattle' nel 2025, quale categoria ha portato più Profit?                                                                                                                                                                           |
| EXT07     | EXT07_CAN   | canonical        | Mostra il Total Gross Amount, il Total Net Amount e il discount impact amount per categoria nel mese di gennaio 2025.                                                                                                                               |
| EXT07     | EXT07_COL   | sales_colloquial | Mi fai per categoria, a gennaio 2025, Total Gross Amount, Total Net Amount e impatto sconti?                                                                                                                                                        |
| EXT07     | EXT07_EXE   | sales_executive  | Nel mese di gennaio 2025, voglio vedere per categoria il Total Gross Amount, il Total Net Amount e il valore di impatto degli sconti.                                                                                                               |
| EXT07     | EXT07_IMP   | sales_implicit   | A gennaio 2025, per categoria, mi dai lordo, netto e impatto sconti?                                                                                                                                                                                |
| EXT08     | EXT08_CAN   | canonical        | Quale categoria ha registrato l'average discount percent più alta nel mese di gennaio 2025?                                                                                                                                                         |
| EXT08     | EXT08_COL   | sales_colloquial | A gennaio 2025, quale categoria ha avuto la discount percent media più alta?                                                                                                                                                                        |
| EXT08     | EXT08_EXE   | sales_executive  | Nel mese di gennaio 2025, quale categoria ha applicato in media la discount percent più elevata?                                                                                                                                                    |
| EXT08     | EXT08_IMP   | sales_implicit   | A gennaio 2025, su quale categoria abbiamo scontato di più in percentuale media?                                                                                                                                                                    |
| EXT09     | EXT09_CAN   | canonical        | Confronta il Total Net Amount del prodotto 'Ball Valve 1/2-inch' tra il 2024 e il 2025.                                                                                                                                                             |
| EXT09     | EXT09_COL   | sales_colloquial | Mi confronti il Total Net Amount di 'Ball Valve 1/2-inch' tra 2024 e 2025?                                                                                                                                                                          |
| EXT09     | EXT09_EXE   | sales_executive  | Per il prodotto 'Ball Valve 1/2-inch', voglio il confronto del Total Net Amount tra 2024 e 2025.                                                                                                                                                    |
| EXT09     | EXT09_IMP   | sales_implicit   | Nel passaggio dal 2024 al 2025, come cambia il Total Net Amount di 'Ball Valve 1/2-inch'?                                                                                                                                                           |
| EXT10     | EXT10_CAN   | canonical        | Nel mese di gennaio 2025, quale percentuale del Total Net Amount della categoria PLUMBING è stata generata dal prodotto 'Ball Valve 1/2-inch'?                                                                                                      |
| EXT10     | EXT10_COL   | sales_colloquial | A gennaio 2025, che quota del Total Net Amount di PLUMBING arriva da 'Ball Valve 1/2-inch'?                                                                                                                                                         |
| EXT10     | EXT10_EXE   | sales_executive  | Nel mese di gennaio 2025, quanto pesa il prodotto 'Ball Valve 1/2-inch' sul Total Net Amount complessivo della categoria PLUMBING?                                                                                                                  |
| EXT10     | EXT10_IMP   | sales_implicit   | Dentro PLUMBING, a gennaio 2025, quanto incide 'Ball Valve 1/2-inch' sul netto totale?                                                                                                                                                              |
| EXT11     | EXT11_CAN   | canonical        | Quali sono i top 3 prodotti pipe-related per Profit nel 2025?                                                                                                                                                                                       |
| EXT11     | EXT11_COL   | sales_colloquial | Mi dai i primi 3 prodotti pipe-related per Profit nel 2025?                                                                                                                                                                                         |
| EXT11     | EXT11_EXE   | sales_executive  | Nel 2025, quali sono i 3 prodotti pipe-related con il Profit più alto?                                                                                                                                                                              |
| EXT11     | EXT11_IMP   | sales_implicit   | Nel 2025, quali prodotti pipe-related spingono di più il Profit?                                                                                                                                                                                    |
| EXT12     | EXT12_CAN   | canonical        | Per 'Zava Retail Online' nel 2025, qual è il mese con il Total Net Amount più alto?                                                                                                                                                                 |
| EXT12     | EXT12_COL   | sales_colloquial | Su 'Zava Retail Online' nel 2025, qual è il mese migliore per Total Net Amount?                                                                                                                                                                     |
| EXT12     | EXT12_EXE   | sales_executive  | Nel 2025, quale mese rappresenta il picco di Total Net Amount per 'Zava Retail Online'?                                                                                                                                                             |
| EXT12     | EXT12_IMP   | sales_implicit   | Per 'Zava Retail Online' nel 2025, in quale mese tocchiamo il massimo di Total Net Amount?                                                                                                                                                          |
| EXT13     | EXT13_CAN   | canonical        | Mostra il Total Net Amount per trimestre per la categoria GARDEN & OUTDOOR nel 2025.                                                                                                                                                                |
| EXT13     | EXT13_COL   | sales_colloquial | Mi fai il Total Net Amount per trimestre di GARDEN & OUTDOOR nel 2025?                                                                                                                                                                              |
| EXT13     | EXT13_EXE   | sales_executive  | Per la categoria GARDEN & OUTDOOR, voglio vedere nel 2025 il Total Net Amount per trimestre.                                                                                                                                                        |
| EXT13     | EXT13_IMP   | sales_implicit   | Nel 2025, come si distribuisce per trimestre il Total Net Amount di GARDEN & OUTDOOR?                                                                                                                                                               |

Se vuoi, nel passo successivo posso unirle al catalogo finale in una master table completa da benchmark con anche `benchmark_split`, `required_tables` e `metric_definition`.

# Step 9 Output

Below is a clean structure for the **master benchmark table** for the final **72-question benchmark**.

## Master benchmark table

| column                 | meaning                                                                                                               | mandatory | frozen conventions                                                                                                                                                                                                                                                                                            |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------- | --------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `benchmark_split`      | Logical partition of the benchmark used to distinguish taught patterns from generalization patterns.                  |       yes | Allowed values only: `ARTICLE_CORE`, `SCHEMA_EXTENDED`. Must stay stable across benchmark versions.                                                                                                                                                                                                           |
| `intent_id`            | Stable identifier of the canonical analytical intent shared by multiple question variants.                            |       yes | Use the frozen IDs already defined: `INT01` to `INT05` for article-derived intents, `EXT01` to `EXT13` for generalization intents. One `intent_id` maps to exactly 4 questions.                                                                                                                               |
| `question_id`          | Stable identifier of a specific question formulation.                                                                 |       yes | Format: `<intent_id>_<suffix>`. Recommended suffixes: `CAN`, `COL`, `EXE`, `IMP`. Example: `INT03_EXE`. Must be unique.                                                                                                                                                                                       |
| `source_type`          | Indicates whether the intent comes from a taught case or a generalization case.                                       |       yes | Allowed values only: `taught_case`, `generalization_case`. This is intent-level metadata and should remain constant across all 4 variants of the same intent.                                                                                                                                                 |
| `language`             | Language of the user-facing question.                                                                                 |       yes | For this benchmark, freeze to `Italian` for all 72 rows. If multilingual extensions are added later, use full names like `Italian`, `English`, `French`.                                                                                                                                                      |
| `variant_type`         | Reformulation family used for the same underlying intent.                                                             |       yes | Allowed values only: `canonical`, `sales_colloquial`, `sales_executive`, `sales_implicit`. Exactly one row per variant per intent.                                                                                                                                                                            |
| `category_5`           | High-level analytical family used for coverage analysis.                                                              |       yes | Allowed values only: `Aggregations`, `Group by / ranking`, `Time intelligence`, `Text filters / domain values`, `Multi-metric / comparative`. Must be assigned at intent level and reused unchanged across its 4 variants.                                                                                    |
| `language_sensitivity` | Expected vulnerability of the intent to wording, entity normalization, domain-value mapping, or linguistic ambiguity. |       yes | Allowed values only: `low`, `medium`, `high`. Assigned at intent level, not per variant.                                                                                                                                                                                                                      |
| `required_tables`      | Minimal set of tables needed to answer the question correctly.                                                        |       yes | Store as a normalized comma-separated list using fully qualified names, for example `retail.orders, retail.order_items, retail.stores`. Order should be stable, ideally alphabetical or join-path based. Same for all 4 variants of the same intent.                                                          |
| `question`             | Actual user-facing benchmark question to send to the Data Agent.                                                      |       yes | Must preserve the exact analytical meaning of the parent intent. Must not change period, filter logic, entity, metric, or ranking target across variants. Exact database entities must remain un-translated where needed.                                                                                     |
| `expected_answer`      | Ground-truth expected result for evaluation.                                                                          |       yes | Can contain either the exact scalar result, a structured JSON-like object, or a normalized table representation, depending on `expected_answer_type`. Must be generated from the benchmark database with frozen metric rules.                                                                                 |
| `expected_answer_type` | Shape of the ground-truth answer.                                                                                     |       yes | Recommended controlled values: `scalar`, `scalar_pair`, `scalar_triple`, `scalar_percentage`, `scalar_plus_percentage`, `top1_entity`, `ranked_list`, `grouped_table`, `monthly_table`, `quarterly_table`, `comparative_summary`, `period_comparison`, `peak_period`. Must remain stable for reproducibility. |
| `comparison_mode`      | Evaluation logic required to compare model output with ground truth.                                                  |       yes | Recommended controlled values: `none`, `ranking_desc`, `subset_vs_total`, `time_trend`, `time_trend_with_windows`, `group_breakdown`, `channel_comparison`, `period_over_period`, `share_of_total`, `peak_period`. Freeze these labels so evaluation logic can branch deterministically.                      |
| `metric_definition`    | Frozen metric rule set required by the question.                                                                      |       yes | Store as a normalized comma-separated list of metric labels, for example `total_net_amount, total_cost, profit`. Use only the official labels defined for the benchmark. Keep order stable.                                                                                                                   |
| `notes`                | Free-text metadata for benchmark maintainers.                                                                         |        no | Use for caveats only: entity-normalization hints, tie-break rules, evaluation nuances, or why a formulation is language-sensitive. Do not put essential evaluation logic here if it can be formalized elsewhere.                                                                                              |

---

## Frozen conventions to keep the benchmark stable

### 1. Split logic

* `ARTICLE_CORE`: intents directly aligned with patterns already taught in the article.
* `SCHEMA_EXTENDED`: intents designed to test adjacent generalization.

### 2. One intent = four variants

Each `intent_id` must always have exactly these four `variant_type` rows:

* `canonical`
* `sales_colloquial`
* `sales_executive`
* `sales_implicit`

### 3. Intent-level columns must not vary across the 4 variants

These should be identical for all rows sharing the same `intent_id`:

* `benchmark_split`
* `source_type`
* `category_5`
* `language_sensitivity`
* `required_tables`
* `expected_answer`
* `expected_answer_type`
* `comparison_mode`
* `metric_definition`
* usually also `notes`

### 4. Exact entity preservation

When labels must match the database exactly, they must remain exactly as stored:

* store names like `Zava Retail Bellevue`
* category values like `PLUMBING`
* product types like `JIGSAWS`
* product names like `Ball Valve 1/2-inch`

### 5. Metric labels should be frozen

Use only the controlled metric labels already defined, such as:

* `total_gross_amount`
* `total_net_amount`
* `total_cost`
* `profit`
* `gross_margin_pct`
* `subset_profit_pct`
* `best_selling_by_quantity`
* `discount_impact_amount`
* `avg_discount_pct`
* `order_count`
* `net_amount_share_pct`
* `running_total_net_amount`
* `profit_delta`
* `peak_month_by_total_net_amount`

### 6. Expected answer normalization

To make evaluation reproducible:

* Scalars should be stored with a frozen numeric precision.
* Percentages should have a frozen representation rule, either ratio or percentage, but never mixed.
* Ranked lists and grouped tables should have deterministic ordering.
* If ties are possible, the tie-break rule must be frozen in `notes` or evaluation logic.

---

## Recommended data types

| column                 | suggested type |
| ---------------------- | -------------- |
| `benchmark_split`      | string / enum  |
| `intent_id`            | string         |
| `question_id`          | string         |
| `source_type`          | string / enum  |
| `language`             | string / enum  |
| `variant_type`         | string / enum  |
| `category_5`           | string / enum  |
| `language_sensitivity` | string / enum  |
| `required_tables`      | string         |
| `question`             | text           |
| `expected_answer`      | text           |
| `expected_answer_type` | string / enum  |
| `comparison_mode`      | string / enum  |
| `metric_definition`    | string         |
| `notes`                | text nullable  |

---

## Minimal evaluation view for `evaluate_data_agent()`

If you want the absolute minimum interface, use only:

| column            | meaning                                       |
| ----------------- | --------------------------------------------- |
| `question`        | The prompt sent to the Data Agent             |
| `expected_answer` | The benchmark ground truth to compare against |

### Minimal view

```text
question
expected_answer
```

### Purpose

This is enough for a very lightweight evaluator that:

1. sends `question` to the Data Agent
2. captures the returned answer
3. compares it against `expected_answer`

### Limitation

This minimal view is sufficient only for **basic answer checking**. It does **not** carry:

* answer shape
* comparison strategy
* ranking semantics
* tolerance rules
* table normalization logic

So it is fine for a first `evaluate_data_agent()` prototype, but for a robust benchmark runner you will soon want at least:

* `expected_answer_type`
* `comparison_mode`

---

## Recommended practical setup

Keep two artifacts:

### A. Master benchmark table

Full benchmark metadata with all 15 columns.

### B. Minimal evaluation view

A derived view like:

| question | expected_answer |
| -------- | --------------- |

This lets you keep the benchmark maintainable while exposing a very small interface to the evaluator.

## Suggested SQL-style view

```sql
SELECT
    question,
    expected_answer
FROM benchmark_master;
```

If you want, I can now produce the full column specification as a benchmark-ready markdown table that you can paste directly into the article or repository README.

# Step 10 Output

```tsv
benchmark_split	intent_id	question_id	source_type	language	variant_type	category_5	language_sensitivity	required_tables	question	expected_answer	expected_answer_type	comparison_mode	metric_definition	notes
ARTICLE_CORE	INT01	INT01_CAN	taught_case	Italian	canonical	Aggregations	medium	retail.orders, retail.order_items, retail.stores	Recupera il Total Gross Amount e il Total Net Amount di tutti gli ordini effettuati a gennaio 2025 nel punto vendita 'Zava Retail Kirkland'.		scalar_pair	none	total_gross_amount, total_net_amount	Core taught metric-definition case. Uses visible store name.
ARTICLE_CORE	INT01	INT01_COL	taught_case	Italian	sales_colloquial	Aggregations	medium	retail.orders, retail.order_items, retail.stores	Mi servono il Total Gross Amount e il Total Net Amount di tutti gli ordini di gennaio 2025 su 'Zava Retail Kirkland'.		scalar_pair	none	total_gross_amount, total_net_amount	Core taught metric-definition case. Uses visible store name.
ARTICLE_CORE	INT01	INT01_EXE	taught_case	Italian	sales_executive	Aggregations	medium	retail.orders, retail.order_items, retail.stores	Quali sono il Total Gross Amount e il Total Net Amount generati nel mese di gennaio 2025 dal punto vendita 'Zava Retail Kirkland'?		scalar_pair	none	total_gross_amount, total_net_amount	Core taught metric-definition case. Uses visible store name.
ARTICLE_CORE	INT01	INT01_IMP	taught_case	Italian	sales_implicit	Aggregations	medium	retail.orders, retail.order_items, retail.stores	Per gennaio 2025, quanto hanno fatto in totale lordo e netto gli ordini di 'Zava Retail Kirkland'?		scalar_pair	none	total_gross_amount, total_net_amount	Core taught metric-definition case. Uses visible store name.
ARTICLE_CORE	INT02	INT02_CAN	taught_case	Italian	canonical	Multi-metric / comparative	high	retail.orders, retail.order_items, retail.products, retail.categories	Calcola il Total Net Amount, il Total Cost e il Profit per i prodotti della categoria PLUMBING nel mese di gennaio 2025.		scalar_triple	none	total_net_amount, total_cost, profit	Core taught KPI bundle. Domain-value variant anchored on visible category.
ARTICLE_CORE	INT02	INT02_COL	taught_case	Italian	sales_colloquial	Multi-metric / comparative	high	retail.orders, retail.order_items, retail.products, retail.categories	Mi dai Total Net Amount, Total Cost e Profit della categoria PLUMBING a gennaio 2025?		scalar_triple	none	total_net_amount, total_cost, profit	Core taught KPI bundle. Domain-value variant anchored on visible category.
ARTICLE_CORE	INT02	INT02_EXE	taught_case	Italian	sales_executive	Multi-metric / comparative	high	retail.orders, retail.order_items, retail.products, retail.categories	Qual è il contributo della categoria PLUMBING nel mese di gennaio 2025 in termini di Total Net Amount, Total Cost e Profit?		scalar_triple	none	total_net_amount, total_cost, profit	Core taught KPI bundle. Domain-value variant anchored on visible category.
ARTICLE_CORE	INT02	INT02_IMP	taught_case	Italian	sales_implicit	Multi-metric / comparative	high	retail.orders, retail.order_items, retail.products, retail.categories	Su PLUMBING, a gennaio 2025, quanto abbiamo fatto di netto, costo e profitto?		scalar_triple	none	total_net_amount, total_cost, profit	Core taught KPI bundle. Domain-value variant anchored on visible category.
ARTICLE_CORE	INT03	INT03_CAN	taught_case	Italian	canonical	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.categories, retail.product_types	Calcola il Profit complessivo della categoria POWER TOOLS nel mese di gennaio 2025. All'interno della categoria, calcola anche il Profit generato solo dai prodotti di tipo JIGSAWS e la percentuale del Profit di JIGSAWS sul totale.		scalar_plus_percentage	subset_vs_total	profit, subset_profit_pct	Replaces non-visible VALVES with visible JIGSAWS while preserving structure.
ARTICLE_CORE	INT03	INT03_COL	taught_case	Italian	sales_colloquial	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.categories, retail.product_types	Mi servono il Profit totale di POWER TOOLS a gennaio 2025, il Profit dei soli JIGSAWS e il peso percentuale dei JIGSAWS sul totale.		scalar_plus_percentage	subset_vs_total	profit, subset_profit_pct	Replaces non-visible VALVES with visible JIGSAWS while preserving structure.
ARTICLE_CORE	INT03	INT03_EXE	taught_case	Italian	sales_executive	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.categories, retail.product_types	Nel mese di gennaio 2025, qual è il Profit complessivo della categoria POWER TOOLS, quanto ne deriva dal tipo JIGSAWS e quale quota percentuale rappresenta sul totale?		scalar_plus_percentage	subset_vs_total	profit, subset_profit_pct	Replaces non-visible VALVES with visible JIGSAWS while preserving structure.
ARTICLE_CORE	INT03	INT03_IMP	taught_case	Italian	sales_implicit	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.categories, retail.product_types	Per POWER TOOLS a gennaio 2025, quanto vale il Profit totale e quanto incidono i JIGSAWS in valore e in percentuale?		scalar_plus_percentage	subset_vs_total	profit, subset_profit_pct	Replaces non-visible VALVES with visible JIGSAWS while preserving structure.
ARTICLE_CORE	INT04	INT04_CAN	taught_case	Italian	canonical	Time intelligence	high	retail.orders, retail.order_items, retail.products, retail.stores	Fornisci il dettaglio mese per mese del prodotto 'Ball Valve 1/2-inch' nel punto vendita 'Zava Retail Bellevue' nel 2024. Mostra i totali cumulati, il gross margin e la variazione del Profit. Evidenzia il mese con il Total Net Amount più alto.		monthly_table	time_trend_with_windows	total_net_amount, running_total_net_amount, gross_margin_pct, profit, profit_delta, peak_month_by_total_net_amount	Preserves the article pattern with visible product and store entities.
ARTICLE_CORE	INT04	INT04_COL	taught_case	Italian	sales_colloquial	Time intelligence	high	retail.orders, retail.order_items, retail.products, retail.stores	Mi fai il mese per mese del prodotto 'Ball Valve 1/2-inch' su 'Zava Retail Bellevue' nel 2024, con cumulato, gross margin, variazione di Profit e il mese migliore per Total Net Amount?		monthly_table	time_trend_with_windows	total_net_amount, running_total_net_amount, gross_margin_pct, profit, profit_delta, peak_month_by_total_net_amount	Preserves the article pattern with visible product and store entities.
ARTICLE_CORE	INT04	INT04_EXE	taught_case	Italian	sales_executive	Time intelligence	high	retail.orders, retail.order_items, retail.products, retail.stores	Per il 2024, voglio una vista mensile del prodotto 'Ball Valve 1/2-inch' nel punto vendita 'Zava Retail Bellevue', con totali cumulati, gross margin, delta di Profit e segnalazione del mese con il Total Net Amount massimo.		monthly_table	time_trend_with_windows	total_net_amount, running_total_net_amount, gross_margin_pct, profit, profit_delta, peak_month_by_total_net_amount	Preserves the article pattern with visible product and store entities.
ARTICLE_CORE	INT04	INT04_IMP	taught_case	Italian	sales_implicit	Time intelligence	high	retail.orders, retail.order_items, retail.products, retail.stores	Nel 2024, come si è mosso mese per mese 'Ball Valve 1/2-inch' su 'Zava Retail Bellevue', con cumulato, margine, cambio di Profit e mese top per Total Net Amount?		monthly_table	time_trend_with_windows	total_net_amount, running_total_net_amount, gross_margin_pct, profit, profit_delta, peak_month_by_total_net_amount	Preserves the article pattern with visible product and store entities.
ARTICLE_CORE	INT05	INT05_CAN	taught_case	Italian	canonical	Group by / ranking	high	retail.orders, retail.order_items, retail.products, retail.categories	Qual è il prodotto più venduto nel 2025 nella categoria PLUMBING?		top1_entity	ranking_desc	best_selling_by_quantity	Core taught ranking case. Best-selling is defined by quantity.
ARTICLE_CORE	INT05	INT05_COL	taught_case	Italian	sales_colloquial	Group by / ranking	high	retail.orders, retail.order_items, retail.products, retail.categories	Nel 2025, qual è stato il prodotto più venduto in PLUMBING?		top1_entity	ranking_desc	best_selling_by_quantity	Core taught ranking case. Best-selling is defined by quantity.
ARTICLE_CORE	INT05	INT05_EXE	taught_case	Italian	sales_executive	Group by / ranking	high	retail.orders, retail.order_items, retail.products, retail.categories	Quale prodotto guida le vendite della categoria PLUMBING nel 2025?		top1_entity	ranking_desc	best_selling_by_quantity	Core taught ranking case. Best-selling is defined by quantity.
ARTICLE_CORE	INT05	INT05_IMP	taught_case	Italian	sales_implicit	Group by / ranking	high	retail.orders, retail.order_items, retail.products, retail.categories	In PLUMBING, nel 2025, chi è il best seller?		top1_entity	ranking_desc	best_selling_by_quantity	Core taught ranking case. Best-selling is defined by quantity.
SCHEMA_EXTENDED	EXT01	EXT01_CAN	generalization_case	Italian	canonical	Group by / ranking	medium	retail.orders, retail.order_items, retail.stores	Quale punto vendita ha registrato il Total Net Amount più alto nel 2025?		top1_entity	ranking_desc	total_net_amount	Generalizes from store filtering to store ranking.
SCHEMA_EXTENDED	EXT01	EXT01_COL	generalization_case	Italian	sales_colloquial	Group by / ranking	medium	retail.orders, retail.order_items, retail.stores	Nel 2025, quale store ha fatto il Total Net Amount più alto?		top1_entity	ranking_desc	total_net_amount	Generalizes from store filtering to store ranking.
SCHEMA_EXTENDED	EXT01	EXT01_EXE	generalization_case	Italian	sales_executive	Group by / ranking	medium	retail.orders, retail.order_items, retail.stores	Qual è il punto vendita leader per Total Net Amount nel 2025?		top1_entity	ranking_desc	total_net_amount	Generalizes from store filtering to store ranking.
SCHEMA_EXTENDED	EXT01	EXT01_IMP	generalization_case	Italian	sales_implicit	Group by / ranking	medium	retail.orders, retail.order_items, retail.stores	Chi è stato il miglior store del 2025 per Total Net Amount?		top1_entity	ranking_desc	total_net_amount	Generalizes from store filtering to store ranking.
SCHEMA_EXTENDED	EXT02	EXT02_CAN	generalization_case	Italian	canonical	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories	Quali sono i top 5 prodotti per Total Net Amount nella categoria PLUMBING nel 2025?		ranked_list	ranking_desc	total_net_amount	Distinct from INT05 because metric is net amount, not quantity, and output is top 5.
SCHEMA_EXTENDED	EXT02	EXT02_COL	generalization_case	Italian	sales_colloquial	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories	Mi dai i primi 5 prodotti di PLUMBING per Total Net Amount nel 2025?		ranked_list	ranking_desc	total_net_amount	Distinct from INT05 because metric is net amount, not quantity, and output is top 5.
SCHEMA_EXTENDED	EXT02	EXT02_EXE	generalization_case	Italian	sales_executive	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories	Nel 2025, quali sono i 5 prodotti con il Total Net Amount più alto nella categoria PLUMBING?		ranked_list	ranking_desc	total_net_amount	Distinct from INT05 because metric is net amount, not quantity, and output is top 5.
SCHEMA_EXTENDED	EXT02	EXT02_IMP	generalization_case	Italian	sales_implicit	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories	Su PLUMBING nel 2025, quali sono i 5 prodotti che hanno portato più Total Net Amount?		ranked_list	ranking_desc	total_net_amount	Distinct from INT05 because metric is net amount, not quantity, and output is top 5.
SCHEMA_EXTENDED	EXT03	EXT03_CAN	generalization_case	Italian	canonical	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.product_types, retail.categories	Mostra il Total Net Amount e il Profit per tipo prodotto nella categoria POWER TOOLS nel 2025.		grouped_table	group_breakdown	total_net_amount, profit	Tests grouped multi-metric breakdown, not subset percentage.
SCHEMA_EXTENDED	EXT03	EXT03_COL	generalization_case	Italian	sales_colloquial	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.product_types, retail.categories	Mi fai il breakdown per tipo prodotto di POWER TOOLS nel 2025 con Total Net Amount e Profit?		grouped_table	group_breakdown	total_net_amount, profit	Tests grouped multi-metric breakdown, not subset percentage.
SCHEMA_EXTENDED	EXT03	EXT03_EXE	generalization_case	Italian	sales_executive	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.product_types, retail.categories	Per la categoria POWER TOOLS nel 2025, voglio vedere Total Net Amount e Profit per ciascun tipo prodotto.		grouped_table	group_breakdown	total_net_amount, profit	Tests grouped multi-metric breakdown, not subset percentage.
SCHEMA_EXTENDED	EXT03	EXT03_IMP	generalization_case	Italian	sales_implicit	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.product_types, retail.categories	Dentro POWER TOOLS nel 2025, come si distribuiscono Total Net Amount e Profit per tipo prodotto?		grouped_table	group_breakdown	total_net_amount, profit	Tests grouped multi-metric breakdown, not subset percentage.
SCHEMA_EXTENDED	EXT04	EXT04_CAN	generalization_case	Italian	canonical	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.stores	Confronta il Total Net Amount e il Profit tra 'Zava Retail Online' e i punti vendita fisici nel mese di gennaio 2025.		comparative_summary	channel_comparison	total_net_amount, profit	Uses stores.is_online and visible online store concept.
SCHEMA_EXTENDED	EXT04	EXT04_COL	generalization_case	Italian	sales_colloquial	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.stores	A gennaio 2025, mi confronti Total Net Amount e Profit tra 'Zava Retail Online' e i negozi fisici?		comparative_summary	channel_comparison	total_net_amount, profit	Uses stores.is_online and visible online store concept.
SCHEMA_EXTENDED	EXT04	EXT04_EXE	generalization_case	Italian	sales_executive	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.stores	Nel mese di gennaio 2025, qual è il confronto tra 'Zava Retail Online' e i punti vendita fisici in termini di Total Net Amount e Profit?		comparative_summary	channel_comparison	total_net_amount, profit	Uses stores.is_online and visible online store concept.
SCHEMA_EXTENDED	EXT04	EXT04_IMP	generalization_case	Italian	sales_implicit	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.stores	A gennaio 2025, 'Zava Retail Online' ha performato meglio o peggio dei negozi fisici su Total Net Amount e Profit?		comparative_summary	channel_comparison	total_net_amount, profit	Uses stores.is_online and visible online store concept.
SCHEMA_EXTENDED	EXT05	EXT05_CAN	generalization_case	Italian	canonical	Time intelligence	medium	retail.orders, retail.order_items, retail.stores	Mostra mese per mese il Total Net Amount e il numero ordini per 'Zava Retail Bellevue' nel 2025.		monthly_table	time_trend	total_net_amount, order_count	Time trend at store level, distinct from INT04 product-level window analysis.
SCHEMA_EXTENDED	EXT05	EXT05_COL	generalization_case	Italian	sales_colloquial	Time intelligence	medium	retail.orders, retail.order_items, retail.stores	Mi fai il mese per mese di 'Zava Retail Bellevue' nel 2025 con Total Net Amount e numero ordini?		monthly_table	time_trend	total_net_amount, order_count	Time trend at store level, distinct from INT04 product-level window analysis.
SCHEMA_EXTENDED	EXT05	EXT05_EXE	generalization_case	Italian	sales_executive	Time intelligence	medium	retail.orders, retail.order_items, retail.stores	Per 'Zava Retail Bellevue' voglio vedere nel 2025 l'andamento mensile di Total Net Amount e numero ordini.		monthly_table	time_trend	total_net_amount, order_count	Time trend at store level, distinct from INT04 product-level window analysis.
SCHEMA_EXTENDED	EXT05	EXT05_IMP	generalization_case	Italian	sales_implicit	Time intelligence	medium	retail.orders, retail.order_items, retail.stores	Nel 2025, come è andata mese per mese 'Zava Retail Bellevue' tra Total Net Amount e volumi ordini?		monthly_table	time_trend	total_net_amount, order_count	Time trend at store level, distinct from INT04 product-level window analysis.
SCHEMA_EXTENDED	EXT06	EXT06_CAN	generalization_case	Italian	canonical	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories, retail.stores	Quale categoria ha generato il Profit più alto nel punto vendita 'Zava Retail Seattle' nel 2025?		top1_entity	ranking_desc	profit	Ranking over categories inside a store slice.
SCHEMA_EXTENDED	EXT06	EXT06_COL	generalization_case	Italian	sales_colloquial	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories, retail.stores	Nel 2025, qual è la categoria con più Profit su 'Zava Retail Seattle'?		top1_entity	ranking_desc	profit	Ranking over categories inside a store slice.
SCHEMA_EXTENDED	EXT06	EXT06_EXE	generalization_case	Italian	sales_executive	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories, retail.stores	Nel punto vendita 'Zava Retail Seattle', quale categoria è stata la migliore per Profit nel 2025?		top1_entity	ranking_desc	profit	Ranking over categories inside a store slice.
SCHEMA_EXTENDED	EXT06	EXT06_IMP	generalization_case	Italian	sales_implicit	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories, retail.stores	Su 'Zava Retail Seattle' nel 2025, quale categoria ha portato più Profit?		top1_entity	ranking_desc	profit	Ranking over categories inside a store slice.
SCHEMA_EXTENDED	EXT07	EXT07_CAN	generalization_case	Italian	canonical	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.categories	Mostra il Total Gross Amount, il Total Net Amount e il discount impact amount per categoria nel mese di gennaio 2025.		grouped_table	group_breakdown	total_gross_amount, total_net_amount, discount_impact_amount	discount_impact_amount = total_gross_amount - total_net_amount. Distinct from INT01 because grouped by category and includes discount impact.
SCHEMA_EXTENDED	EXT07	EXT07_COL	generalization_case	Italian	sales_colloquial	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.categories	Mi fai per categoria, a gennaio 2025, Total Gross Amount, Total Net Amount e impatto sconti?		grouped_table	group_breakdown	total_gross_amount, total_net_amount, discount_impact_amount	discount_impact_amount = total_gross_amount - total_net_amount. Distinct from INT01 because grouped by category and includes discount impact.
SCHEMA_EXTENDED	EXT07	EXT07_EXE	generalization_case	Italian	sales_executive	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.categories	Nel mese di gennaio 2025, voglio vedere per categoria il Total Gross Amount, il Total Net Amount e il valore di impatto degli sconti.		grouped_table	group_breakdown	total_gross_amount, total_net_amount, discount_impact_amount	discount_impact_amount = total_gross_amount - total_net_amount. Distinct from INT01 because grouped by category and includes discount impact.
SCHEMA_EXTENDED	EXT07	EXT07_IMP	generalization_case	Italian	sales_implicit	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.categories	A gennaio 2025, per categoria, mi dai lordo, netto e impatto sconti?		grouped_table	group_breakdown	total_gross_amount, total_net_amount, discount_impact_amount	discount_impact_amount = total_gross_amount - total_net_amount. Distinct from INT01 because grouped by category and includes discount impact.
SCHEMA_EXTENDED	EXT08	EXT08_CAN	generalization_case	Italian	canonical	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories	Quale categoria ha registrato l'average discount percent più alta nel mese di gennaio 2025?		top1_entity	ranking_desc	avg_discount_pct	Tests discount-based ranking rather than revenue or profit ranking.
SCHEMA_EXTENDED	EXT08	EXT08_COL	generalization_case	Italian	sales_colloquial	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories	A gennaio 2025, quale categoria ha avuto la discount percent media più alta?		top1_entity	ranking_desc	avg_discount_pct	Tests discount-based ranking rather than revenue or profit ranking.
SCHEMA_EXTENDED	EXT08	EXT08_EXE	generalization_case	Italian	sales_executive	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories	Nel mese di gennaio 2025, quale categoria ha applicato in media la discount percent più elevata?		top1_entity	ranking_desc	avg_discount_pct	Tests discount-based ranking rather than revenue or profit ranking.
SCHEMA_EXTENDED	EXT08	EXT08_IMP	generalization_case	Italian	sales_implicit	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories	A gennaio 2025, su quale categoria abbiamo scontato di più in percentuale media?		top1_entity	ranking_desc	avg_discount_pct	Tests discount-based ranking rather than revenue or profit ranking.
SCHEMA_EXTENDED	EXT09	EXT09_CAN	generalization_case	Italian	canonical	Time intelligence	high	retail.orders, retail.order_items, retail.products	Confronta il Total Net Amount del prodotto 'Ball Valve 1/2-inch' tra il 2024 e il 2025.		period_comparison	period_over_period	total_net_amount	Uses visible product name. Tests entity precision plus year-over-year logic.
SCHEMA_EXTENDED	EXT09	EXT09_COL	generalization_case	Italian	sales_colloquial	Time intelligence	high	retail.orders, retail.order_items, retail.products	Mi confronti il Total Net Amount di 'Ball Valve 1/2-inch' tra 2024 e 2025?		period_comparison	period_over_period	total_net_amount	Uses visible product name. Tests entity precision plus year-over-year logic.
SCHEMA_EXTENDED	EXT09	EXT09_EXE	generalization_case	Italian	sales_executive	Time intelligence	high	retail.orders, retail.order_items, retail.products	Per il prodotto 'Ball Valve 1/2-inch', voglio il confronto del Total Net Amount tra 2024 e 2025.		period_comparison	period_over_period	total_net_amount	Uses visible product name. Tests entity precision plus year-over-year logic.
SCHEMA_EXTENDED	EXT09	EXT09_IMP	generalization_case	Italian	sales_implicit	Time intelligence	high	retail.orders, retail.order_items, retail.products	Nel passaggio dal 2024 al 2025, come cambia il Total Net Amount di 'Ball Valve 1/2-inch'?		period_comparison	period_over_period	total_net_amount	Uses visible product name. Tests entity precision plus year-over-year logic.
SCHEMA_EXTENDED	EXT10	EXT10_CAN	generalization_case	Italian	canonical	Multi-metric / comparative	high	retail.orders, retail.order_items, retail.products, retail.categories	Nel mese di gennaio 2025, quale percentuale del Total Net Amount della categoria PLUMBING è stata generata dal prodotto 'Ball Valve 1/2-inch'?		scalar_percentage	share_of_total	total_net_amount, net_amount_share_pct	Distinct from INT03 because it uses net amount share, not profit share of a type subset.
SCHEMA_EXTENDED	EXT10	EXT10_COL	generalization_case	Italian	sales_colloquial	Multi-metric / comparative	high	retail.orders, retail.order_items, retail.products, retail.categories	A gennaio 2025, che quota del Total Net Amount di PLUMBING arriva da 'Ball Valve 1/2-inch'?		scalar_percentage	share_of_total	total_net_amount, net_amount_share_pct	Distinct from INT03 because it uses net amount share, not profit share of a type subset.
SCHEMA_EXTENDED	EXT10	EXT10_EXE	generalization_case	Italian	sales_executive	Multi-metric / comparative	high	retail.orders, retail.order_items, retail.products, retail.categories	Nel mese di gennaio 2025, quanto pesa il prodotto 'Ball Valve 1/2-inch' sul Total Net Amount complessivo della categoria PLUMBING?		scalar_percentage	share_of_total	total_net_amount, net_amount_share_pct	Distinct from INT03 because it uses net amount share, not profit share of a type subset.
SCHEMA_EXTENDED	EXT10	EXT10_IMP	generalization_case	Italian	sales_implicit	Multi-metric / comparative	high	retail.orders, retail.order_items, retail.products, retail.categories	Dentro PLUMBING, a gennaio 2025, quanto incide 'Ball Valve 1/2-inch' sul netto totale?		scalar_percentage	share_of_total	total_net_amount, net_amount_share_pct	Distinct from INT03 because it uses net amount share, not profit share of a type subset.
SCHEMA_EXTENDED	EXT11	EXT11_CAN	generalization_case	Italian	canonical	Text filters / domain values	high	retail.orders, retail.order_items, retail.products	Quali sono i top 3 prodotti pipe-related per Profit nel 2025?		ranked_list	ranking_desc	profit	Tests text filtering on product_description plus ranking.
SCHEMA_EXTENDED	EXT11	EXT11_COL	generalization_case	Italian	sales_colloquial	Text filters / domain values	high	retail.orders, retail.order_items, retail.products	Mi dai i primi 3 prodotti pipe-related per Profit nel 2025?		ranked_list	ranking_desc	profit	Tests text filtering on product_description plus ranking.
SCHEMA_EXTENDED	EXT11	EXT11_EXE	generalization_case	Italian	sales_executive	Text filters / domain values	high	retail.orders, retail.order_items, retail.products	Nel 2025, quali sono i 3 prodotti pipe-related con il Profit più alto?		ranked_list	ranking_desc	profit	Tests text filtering on product_description plus ranking.
SCHEMA_EXTENDED	EXT11	EXT11_IMP	generalization_case	Italian	sales_implicit	Text filters / domain values	high	retail.orders, retail.order_items, retail.products	Nel 2025, quali prodotti pipe-related spingono di più il Profit?		ranked_list	ranking_desc	profit	Tests text filtering on product_description plus ranking.
SCHEMA_EXTENDED	EXT12	EXT12_CAN	generalization_case	Italian	canonical	Time intelligence	medium	retail.orders, retail.order_items, retail.stores	Per 'Zava Retail Online' nel 2025, qual è il mese con il Total Net Amount più alto?		peak_period	peak_period	total_net_amount	Time intelligence at channel/store level, distinct from full monthly breakdown.
SCHEMA_EXTENDED	EXT12	EXT12_COL	generalization_case	Italian	sales_colloquial	Time intelligence	medium	retail.orders, retail.order_items, retail.stores	Su 'Zava Retail Online' nel 2025, qual è il mese migliore per Total Net Amount?		peak_period	peak_period	total_net_amount	Time intelligence at channel/store level, distinct from full monthly breakdown.
SCHEMA_EXTENDED	EXT12	EXT12_EXE	generalization_case	Italian	sales_executive	Time intelligence	medium	retail.orders, retail.order_items, retail.stores	Nel 2025, quale mese rappresenta il picco di Total Net Amount per 'Zava Retail Online'?		peak_period	peak_period	total_net_amount	Time intelligence at channel/store level, distinct from full monthly breakdown.
SCHEMA_EXTENDED	EXT12	EXT12_IMP	generalization_case	Italian	sales_implicit	Time intelligence	medium	retail.orders, retail.order_items, retail.stores	Per 'Zava Retail Online' nel 2025, in quale mese tocchiamo il massimo di Total Net Amount?		peak_period	peak_period	total_net_amount	Time intelligence at channel/store level, distinct from full monthly breakdown.
SCHEMA_EXTENDED	EXT13	EXT13_CAN	generalization_case	Italian	canonical	Time intelligence	medium	retail.orders, retail.order_items, retail.products, retail.categories	Mostra il Total Net Amount per trimestre per la categoria GARDEN & OUTDOOR nel 2025.		quarterly_table	time_trend	total_net_amount	Tests quarter grain and category aggregation.
SCHEMA_EXTENDED	EXT13	EXT13_COL	generalization_case	Italian	sales_colloquial	Time intelligence	medium	retail.orders, retail.order_items, retail.products, retail.categories	Mi fai il Total Net Amount per trimestre di GARDEN & OUTDOOR nel 2025?		quarterly_table	time_trend	total_net_amount	Tests quarter grain and category aggregation.
SCHEMA_EXTENDED	EXT13	EXT13_EXE	generalization_case	Italian	sales_executive	Time intelligence	medium	retail.orders, retail.order_items, retail.products, retail.categories	Per la categoria GARDEN & OUTDOOR, voglio vedere nel 2025 il Total Net Amount per trimestre.		quarterly_table	time_trend	total_net_amount	Tests quarter grain and category aggregation.
SCHEMA_EXTENDED	EXT13	EXT13_IMP	generalization_case	Italian	sales_implicit	Time intelligence	medium	retail.orders, retail.order_items, retail.products, retail.categories	Nel 2025, come si distribuisce per trimestre il Total Net Amount di GARDEN & OUTDOOR?		quarterly_table	time_trend	total_net_amount	Tests quarter grain and category aggregation.
```

# Step 11 Output

1. No issues found. The TSV passes all requested checks:

* 72 rows
* 18 unique intents
* 4 variants per intent
* no duplicated `question_id`
* `required_tables` populated in every row
* `expected_answer_type` and `comparison_mode` are internally consistent
* `metric_definition` is consistent within each intent
* no row requires tables outside the allowed perimeter

```tsv
benchmark_split	intent_id	question_id	source_type	language	variant_type	category_5	language_sensitivity	required_tables	question	expected_answer	expected_answer_type	comparison_mode	metric_definition	notes
ARTICLE_CORE	INT01	INT01_CAN	taught_case	Italian	canonical	Aggregations	medium	retail.orders, retail.order_items, retail.stores	Recupera il Total Gross Amount e il Total Net Amount di tutti gli ordini effettuati a gennaio 2025 nel punto vendita 'Zava Retail Kirkland'.		scalar_pair	none	total_gross_amount, total_net_amount	Core taught metric-definition case. Uses visible store name.
ARTICLE_CORE	INT01	INT01_COL	taught_case	Italian	sales_colloquial	Aggregations	medium	retail.orders, retail.order_items, retail.stores	Mi servono il Total Gross Amount e il Total Net Amount di tutti gli ordini di gennaio 2025 su 'Zava Retail Kirkland'.		scalar_pair	none	total_gross_amount, total_net_amount	Core taught metric-definition case. Uses visible store name.
ARTICLE_CORE	INT01	INT01_EXE	taught_case	Italian	sales_executive	Aggregations	medium	retail.orders, retail.order_items, retail.stores	Quali sono il Total Gross Amount e il Total Net Amount generati nel mese di gennaio 2025 dal punto vendita 'Zava Retail Kirkland'?		scalar_pair	none	total_gross_amount, total_net_amount	Core taught metric-definition case. Uses visible store name.
ARTICLE_CORE	INT01	INT01_IMP	taught_case	Italian	sales_implicit	Aggregations	medium	retail.orders, retail.order_items, retail.stores	Per gennaio 2025, quanto hanno fatto in totale lordo e netto gli ordini di 'Zava Retail Kirkland'?		scalar_pair	none	total_gross_amount, total_net_amount	Core taught metric-definition case. Uses visible store name.
ARTICLE_CORE	INT02	INT02_CAN	taught_case	Italian	canonical	Multi-metric / comparative	high	retail.orders, retail.order_items, retail.products, retail.categories	Calcola il Total Net Amount, il Total Cost e il Profit per i prodotti della categoria PLUMBING nel mese di gennaio 2025.		scalar_triple	none	total_net_amount, total_cost, profit	Core taught KPI bundle. Domain-value variant anchored on visible category.
ARTICLE_CORE	INT02	INT02_COL	taught_case	Italian	sales_colloquial	Multi-metric / comparative	high	retail.orders, retail.order_items, retail.products, retail.categories	Mi dai Total Net Amount, Total Cost e Profit della categoria PLUMBING a gennaio 2025?		scalar_triple	none	total_net_amount, total_cost, profit	Core taught KPI bundle. Domain-value variant anchored on visible category.
ARTICLE_CORE	INT02	INT02_EXE	taught_case	Italian	sales_executive	Multi-metric / comparative	high	retail.orders, retail.order_items, retail.products, retail.categories	Qual è il contributo della categoria PLUMBING nel mese di gennaio 2025 in termini di Total Net Amount, Total Cost e Profit?		scalar_triple	none	total_net_amount, total_cost, profit	Core taught KPI bundle. Domain-value variant anchored on visible category.
ARTICLE_CORE	INT02	INT02_IMP	taught_case	Italian	sales_implicit	Multi-metric / comparative	high	retail.orders, retail.order_items, retail.products, retail.categories	Su PLUMBING, a gennaio 2025, quanto abbiamo fatto di netto, costo e profitto?		scalar_triple	none	total_net_amount, total_cost, profit	Core taught KPI bundle. Domain-value variant anchored on visible category.
ARTICLE_CORE	INT03	INT03_CAN	taught_case	Italian	canonical	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.categories, retail.product_types	Calcola il Profit complessivo della categoria POWER TOOLS nel mese di gennaio 2025. All'interno della categoria, calcola anche il Profit generato solo dai prodotti di tipo JIGSAWS e la percentuale del Profit di JIGSAWS sul totale.		scalar_plus_percentage	subset_vs_total	profit, subset_profit_pct	Replaces non-visible VALVES with visible JIGSAWS while preserving structure.
ARTICLE_CORE	INT03	INT03_COL	taught_case	Italian	sales_colloquial	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.categories, retail.product_types	Mi servono il Profit totale di POWER TOOLS a gennaio 2025, il Profit dei soli JIGSAWS e il peso percentuale dei JIGSAWS sul totale.		scalar_plus_percentage	subset_vs_total	profit, subset_profit_pct	Replaces non-visible VALVES with visible JIGSAWS while preserving structure.
ARTICLE_CORE	INT03	INT03_EXE	taught_case	Italian	sales_executive	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.categories, retail.product_types	Nel mese di gennaio 2025, qual è il Profit complessivo della categoria POWER TOOLS, quanto ne deriva dal tipo JIGSAWS e quale quota percentuale rappresenta sul totale?		scalar_plus_percentage	subset_vs_total	profit, subset_profit_pct	Replaces non-visible VALVES with visible JIGSAWS while preserving structure.
ARTICLE_CORE	INT03	INT03_IMP	taught_case	Italian	sales_implicit	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.categories, retail.product_types	Per POWER TOOLS a gennaio 2025, quanto vale il Profit totale e quanto incidono i JIGSAWS in valore e in percentuale?		scalar_plus_percentage	subset_vs_total	profit, subset_profit_pct	Replaces non-visible VALVES with visible JIGSAWS while preserving structure.
ARTICLE_CORE	INT04	INT04_CAN	taught_case	Italian	canonical	Time intelligence	high	retail.orders, retail.order_items, retail.products, retail.stores	Fornisci il dettaglio mese per mese del prodotto 'Ball Valve 1/2-inch' nel punto vendita 'Zava Retail Bellevue' nel 2024. Mostra i totali cumulati, il gross margin e la variazione del Profit. Evidenzia il mese con il Total Net Amount più alto.		monthly_table	time_trend_with_windows	total_net_amount, running_total_net_amount, gross_margin_pct, profit, profit_delta, peak_month_by_total_net_amount	Preserves the article pattern with visible product and store entities.
ARTICLE_CORE	INT04	INT04_COL	taught_case	Italian	sales_colloquial	Time intelligence	high	retail.orders, retail.order_items, retail.products, retail.stores	Mi fai il mese per mese del prodotto 'Ball Valve 1/2-inch' su 'Zava Retail Bellevue' nel 2024, con cumulato, gross margin, variazione di Profit e il mese migliore per Total Net Amount?		monthly_table	time_trend_with_windows	total_net_amount, running_total_net_amount, gross_margin_pct, profit, profit_delta, peak_month_by_total_net_amount	Preserves the article pattern with visible product and store entities.
ARTICLE_CORE	INT04	INT04_EXE	taught_case	Italian	sales_executive	Time intelligence	high	retail.orders, retail.order_items, retail.products, retail.stores	Per il 2024, voglio una vista mensile del prodotto 'Ball Valve 1/2-inch' nel punto vendita 'Zava Retail Bellevue', con totali cumulati, gross margin, delta di Profit e segnalazione del mese con il Total Net Amount massimo.		monthly_table	time_trend_with_windows	total_net_amount, running_total_net_amount, gross_margin_pct, profit, profit_delta, peak_month_by_total_net_amount	Preserves the article pattern with visible product and store entities.
ARTICLE_CORE	INT04	INT04_IMP	taught_case	Italian	sales_implicit	Time intelligence	high	retail.orders, retail.order_items, retail.products, retail.stores	Nel 2024, come si è mosso mese per mese 'Ball Valve 1/2-inch' su 'Zava Retail Bellevue', con cumulato, margine, cambio di Profit e mese top per Total Net Amount?		monthly_table	time_trend_with_windows	total_net_amount, running_total_net_amount, gross_margin_pct, profit, profit_delta, peak_month_by_total_net_amount	Preserves the article pattern with visible product and store entities.
ARTICLE_CORE	INT05	INT05_CAN	taught_case	Italian	canonical	Group by / ranking	high	retail.orders, retail.order_items, retail.products, retail.categories	Qual è il prodotto più venduto nel 2025 nella categoria PLUMBING?		top1_entity	ranking_desc	best_selling_by_quantity	Core taught ranking case. Best-selling is defined by quantity.
ARTICLE_CORE	INT05	INT05_COL	taught_case	Italian	sales_colloquial	Group by / ranking	high	retail.orders, retail.order_items, retail.products, retail.categories	Nel 2025, qual è stato il prodotto più venduto in PLUMBING?		top1_entity	ranking_desc	best_selling_by_quantity	Core taught ranking case. Best-selling is defined by quantity.
ARTICLE_CORE	INT05	INT05_EXE	taught_case	Italian	sales_executive	Group by / ranking	high	retail.orders, retail.order_items, retail.products, retail.categories	Quale prodotto guida le vendite della categoria PLUMBING nel 2025?		top1_entity	ranking_desc	best_selling_by_quantity	Core taught ranking case. Best-selling is defined by quantity.
ARTICLE_CORE	INT05	INT05_IMP	taught_case	Italian	sales_implicit	Group by / ranking	high	retail.orders, retail.order_items, retail.products, retail.categories	In PLUMBING, nel 2025, chi è il best seller?		top1_entity	ranking_desc	best_selling_by_quantity	Core taught ranking case. Best-selling is defined by quantity.
SCHEMA_EXTENDED	EXT01	EXT01_CAN	generalization_case	Italian	canonical	Group by / ranking	medium	retail.orders, retail.order_items, retail.stores	Quale punto vendita ha registrato il Total Net Amount più alto nel 2025?		top1_entity	ranking_desc	total_net_amount	Generalizes from store filtering to store ranking.
SCHEMA_EXTENDED	EXT01	EXT01_COL	generalization_case	Italian	sales_colloquial	Group by / ranking	medium	retail.orders, retail.order_items, retail.stores	Nel 2025, quale store ha fatto il Total Net Amount più alto?		top1_entity	ranking_desc	total_net_amount	Generalizes from store filtering to store ranking.
SCHEMA_EXTENDED	EXT01	EXT01_EXE	generalization_case	Italian	sales_executive	Group by / ranking	medium	retail.orders, retail.order_items, retail.stores	Qual è il punto vendita leader per Total Net Amount nel 2025?		top1_entity	ranking_desc	total_net_amount	Generalizes from store filtering to store ranking.
SCHEMA_EXTENDED	EXT01	EXT01_IMP	generalization_case	Italian	sales_implicit	Group by / ranking	medium	retail.orders, retail.order_items, retail.stores	Chi è stato il miglior store del 2025 per Total Net Amount?		top1_entity	ranking_desc	total_net_amount	Generalizes from store filtering to store ranking.
SCHEMA_EXTENDED	EXT02	EXT02_CAN	generalization_case	Italian	canonical	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories	Quali sono i top 5 prodotti per Total Net Amount nella categoria PLUMBING nel 2025?		ranked_list	ranking_desc	total_net_amount	Distinct from INT05 because metric is net amount, not quantity, and output is top 5.
SCHEMA_EXTENDED	EXT02	EXT02_COL	generalization_case	Italian	sales_colloquial	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories	Mi dai i primi 5 prodotti di PLUMBING per Total Net Amount nel 2025?		ranked_list	ranking_desc	total_net_amount	Distinct from INT05 because metric is net amount, not quantity, and output is top 5.
SCHEMA_EXTENDED	EXT02	EXT02_EXE	generalization_case	Italian	sales_executive	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories	Nel 2025, quali sono i 5 prodotti con il Total Net Amount più alto nella categoria PLUMBING?		ranked_list	ranking_desc	total_net_amount	Distinct from INT05 because metric is net amount, not quantity, and output is top 5.
SCHEMA_EXTENDED	EXT02	EXT02_IMP	generalization_case	Italian	sales_implicit	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories	Su PLUMBING nel 2025, quali sono i 5 prodotti che hanno portato più Total Net Amount?		ranked_list	ranking_desc	total_net_amount	Distinct from INT05 because metric is net amount, not quantity, and output is top 5.
SCHEMA_EXTENDED	EXT03	EXT03_CAN	generalization_case	Italian	canonical	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.product_types, retail.categories	Mostra il Total Net Amount e il Profit per tipo prodotto nella categoria POWER TOOLS nel 2025.		grouped_table	group_breakdown	total_net_amount, profit	Tests grouped multi-metric breakdown, not subset percentage.
SCHEMA_EXTENDED	EXT03	EXT03_COL	generalization_case	Italian	sales_colloquial	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.product_types, retail.categories	Mi fai il breakdown per tipo prodotto di POWER TOOLS nel 2025 con Total Net Amount e Profit?		grouped_table	group_breakdown	total_net_amount, profit	Tests grouped multi-metric breakdown, not subset percentage.
SCHEMA_EXTENDED	EXT03	EXT03_EXE	generalization_case	Italian	sales_executive	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.product_types, retail.categories	Per la categoria POWER TOOLS nel 2025, voglio vedere Total Net Amount e Profit per ciascun tipo prodotto.		grouped_table	group_breakdown	total_net_amount, profit	Tests grouped multi-metric breakdown, not subset percentage.
SCHEMA_EXTENDED	EXT03	EXT03_IMP	generalization_case	Italian	sales_implicit	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.product_types, retail.categories	Dentro POWER TOOLS nel 2025, come si distribuiscono Total Net Amount e Profit per tipo prodotto?		grouped_table	group_breakdown	total_net_amount, profit	Tests grouped multi-metric breakdown, not subset percentage.
SCHEMA_EXTENDED	EXT04	EXT04_CAN	generalization_case	Italian	canonical	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.stores	Confronta il Total Net Amount e il Profit tra 'Zava Retail Online' e i punti vendita fisici nel mese di gennaio 2025.		comparative_summary	channel_comparison	total_net_amount, profit	Uses stores.is_online and visible online store concept.
SCHEMA_EXTENDED	EXT04	EXT04_COL	generalization_case	Italian	sales_colloquial	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.stores	A gennaio 2025, mi confronti Total Net Amount e Profit tra 'Zava Retail Online' e i negozi fisici?		comparative_summary	channel_comparison	total_net_amount, profit	Uses stores.is_online and visible online store concept.
SCHEMA_EXTENDED	EXT04	EXT04_EXE	generalization_case	Italian	sales_executive	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.stores	Nel mese di gennaio 2025, qual è il confronto tra 'Zava Retail Online' e i punti vendita fisici in termini di Total Net Amount e Profit?		comparative_summary	channel_comparison	total_net_amount, profit	Uses stores.is_online and visible online store concept.
SCHEMA_EXTENDED	EXT04	EXT04_IMP	generalization_case	Italian	sales_implicit	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.stores	A gennaio 2025, 'Zava Retail Online' ha performato meglio o peggio dei negozi fisici su Total Net Amount e Profit?		comparative_summary	channel_comparison	total_net_amount, profit	Uses stores.is_online and visible online store concept.
SCHEMA_EXTENDED	EXT05	EXT05_CAN	generalization_case	Italian	canonical	Time intelligence	medium	retail.orders, retail.order_items, retail.stores	Mostra mese per mese il Total Net Amount e il numero ordini per 'Zava Retail Bellevue' nel 2025.		monthly_table	time_trend	total_net_amount, order_count	Time trend at store level, distinct from INT04 product-level window analysis.
SCHEMA_EXTENDED	EXT05	EXT05_COL	generalization_case	Italian	sales_colloquial	Time intelligence	medium	retail.orders, retail.order_items, retail.stores	Mi fai il mese per mese di 'Zava Retail Bellevue' nel 2025 con Total Net Amount e numero ordini?		monthly_table	time_trend	total_net_amount, order_count	Time trend at store level, distinct from INT04 product-level window analysis.
SCHEMA_EXTENDED	EXT05	EXT05_EXE	generalization_case	Italian	sales_executive	Time intelligence	medium	retail.orders, retail.order_items, retail.stores	Per 'Zava Retail Bellevue' voglio vedere nel 2025 l'andamento mensile di Total Net Amount e numero ordini.		monthly_table	time_trend	total_net_amount, order_count	Time trend at store level, distinct from INT04 product-level window analysis.
SCHEMA_EXTENDED	EXT05	EXT05_IMP	generalization_case	Italian	sales_implicit	Time intelligence	medium	retail.orders, retail.order_items, retail.stores	Nel 2025, come è andata mese per mese 'Zava Retail Bellevue' tra Total Net Amount e volumi ordini?		monthly_table	time_trend	total_net_amount, order_count	Time trend at store level, distinct from INT04 product-level window analysis.
SCHEMA_EXTENDED	EXT06	EXT06_CAN	generalization_case	Italian	canonical	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories, retail.stores	Quale categoria ha generato il Profit più alto nel punto vendita 'Zava Retail Seattle' nel 2025?		top1_entity	ranking_desc	profit	Ranking over categories inside a store slice.
SCHEMA_EXTENDED	EXT06	EXT06_COL	generalization_case	Italian	sales_colloquial	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories, retail.stores	Nel 2025, qual è la categoria con più Profit su 'Zava Retail Seattle'?		top1_entity	ranking_desc	profit	Ranking over categories inside a store slice.
SCHEMA_EXTENDED	EXT06	EXT06_EXE	generalization_case	Italian	sales_executive	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories, retail.stores	Nel punto vendita 'Zava Retail Seattle', quale categoria è stata la migliore per Profit nel 2025?		top1_entity	ranking_desc	profit	Ranking over categories inside a store slice.
SCHEMA_EXTENDED	EXT06	EXT06_IMP	generalization_case	Italian	sales_implicit	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories, retail.stores	Su 'Zava Retail Seattle' nel 2025, quale categoria ha portato più Profit?		top1_entity	ranking_desc	profit	Ranking over categories inside a store slice.
SCHEMA_EXTENDED	EXT07	EXT07_CAN	generalization_case	Italian	canonical	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.categories	Mostra il Total Gross Amount, il Total Net Amount e il discount impact amount per categoria nel mese di gennaio 2025.		grouped_table	group_breakdown	total_gross_amount, total_net_amount, discount_impact_amount	discount_impact_amount = total_gross_amount - total_net_amount. Distinct from INT01 because grouped by category and includes discount impact.
SCHEMA_EXTENDED	EXT07	EXT07_COL	generalization_case	Italian	sales_colloquial	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.categories	Mi fai per categoria, a gennaio 2025, Total Gross Amount, Total Net Amount e impatto sconti?		grouped_table	group_breakdown	total_gross_amount, total_net_amount, discount_impact_amount	discount_impact_amount = total_gross_amount - total_net_amount. Distinct from INT01 because grouped by category and includes discount impact.
SCHEMA_EXTENDED	EXT07	EXT07_EXE	generalization_case	Italian	sales_executive	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.categories	Nel mese di gennaio 2025, voglio vedere per categoria il Total Gross Amount, il Total Net Amount e il valore di impatto degli sconti.		grouped_table	group_breakdown	total_gross_amount, total_net_amount, discount_impact_amount	discount_impact_amount = total_gross_amount - total_net_amount. Distinct from INT01 because grouped by category and includes discount impact.
SCHEMA_EXTENDED	EXT07	EXT07_IMP	generalization_case	Italian	sales_implicit	Multi-metric / comparative	medium	retail.orders, retail.order_items, retail.products, retail.categories	A gennaio 2025, per categoria, mi dai lordo, netto e impatto sconti?		grouped_table	group_breakdown	total_gross_amount, total_net_amount, discount_impact_amount	discount_impact_amount = total_gross_amount - total_net_amount. Distinct from INT01 because grouped by category and includes discount impact.
SCHEMA_EXTENDED	EXT08	EXT08_CAN	generalization_case	Italian	canonical	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories	Quale categoria ha registrato l'average discount percent più alta nel mese di gennaio 2025?		top1_entity	ranking_desc	avg_discount_pct	Tests discount-based ranking rather than revenue or profit ranking.
SCHEMA_EXTENDED	EXT08	EXT08_COL	generalization_case	Italian	sales_colloquial	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories	A gennaio 2025, quale categoria ha avuto la discount percent media più alta?		top1_entity	ranking_desc	avg_discount_pct	Tests discount-based ranking rather than revenue or profit ranking.
SCHEMA_EXTENDED	EXT08	EXT08_EXE	generalization_case	Italian	sales_executive	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories	Nel mese di gennaio 2025, quale categoria ha applicato in media la discount percent più elevata?		top1_entity	ranking_desc	avg_discount_pct	Tests discount-based ranking rather than revenue or profit ranking.
SCHEMA_EXTENDED	EXT08	EXT08_IMP	generalization_case	Italian	sales_implicit	Group by / ranking	medium	retail.orders, retail.order_items, retail.products, retail.categories	A gennaio 2025, su quale categoria abbiamo scontato di più in percentuale media?		top1_entity	ranking_desc	avg_discount_pct	Tests discount-based ranking rather than revenue or profit ranking.
SCHEMA_EXTENDED	EXT09	EXT09_CAN	generalization_case	Italian	canonical	Time intelligence	high	retail.orders, retail.order_items, retail.products	Confronta il Total Net Amount del prodotto 'Ball Valve 1/2-inch' tra il 2024 e il 2025.		period_comparison	period_over_period	total_net_amount	Uses visible product name. Tests entity precision plus year-over-year logic.
SCHEMA_EXTENDED	EXT09	EXT09_COL	generalization_case	Italian	sales_colloquial	Time intelligence	high	retail.orders, retail.order_items, retail.products	Mi confronti il Total Net Amount di 'Ball Valve 1/2-inch' tra 2024 e 2025?		period_comparison	period_over_period	total_net_amount	Uses visible product name. Tests entity precision plus year-over-year logic.
SCHEMA_EXTENDED	EXT09	EXT09_EXE	generalization_case	Italian	sales_executive	Time intelligence	high	retail.orders, retail.order_items, retail.products	Per il prodotto 'Ball Valve 1/2-inch', voglio il confronto del Total Net Amount tra 2024 e 2025.		period_comparison	period_over_period	total_net_amount	Uses visible product name. Tests entity precision plus year-over-year logic.
SCHEMA_EXTENDED	EXT09	EXT09_IMP	generalization_case	Italian	sales_implicit	Time intelligence	high	retail.orders, retail.order_items, retail.products	Nel passaggio dal 2024 al 2025, come cambia il Total Net Amount di 'Ball Valve 1/2-inch'?		period_comparison	period_over_period	total_net_amount	Uses visible product name. Tests entity precision plus year-over-year logic.
SCHEMA_EXTENDED	EXT10	EXT10_CAN	generalization_case	Italian	canonical	Multi-metric / comparative	high	retail.orders, retail.order_items, retail.products, retail.categories	Nel mese di gennaio 2025, quale percentuale del Total Net Amount della categoria PLUMBING è stata generata dal prodotto 'Ball Valve 1/2-inch'?		scalar_percentage	share_of_total	total_net_amount, net_amount_share_pct	Distinct from INT03 because it uses net amount share, not profit share of a type subset.
SCHEMA_EXTENDED	EXT10	EXT10_COL	generalization_case	Italian	sales_colloquial	Multi-metric / comparative	high	retail.orders, retail.order_items, retail.products, retail.categories	A gennaio 2025, che quota del Total Net Amount di PLUMBING arriva da 'Ball Valve 1/2-inch'?		scalar_percentage	share_of_total	total_net_amount, net_amount_share_pct	Distinct from INT03 because it uses net amount share, not profit share of a type subset.
SCHEMA_EXTENDED	EXT10	EXT10_EXE	generalization_case	Italian	sales_executive	Multi-metric / comparative	high	retail.orders, retail.order_items, retail.products, retail.categories	Nel mese di gennaio 2025, quanto pesa il prodotto 'Ball Valve 1/2-inch' sul Total Net Amount complessivo della categoria PLUMBING?		scalar_percentage	share_of_total	total_net_amount, net_amount_share_pct	Distinct from INT03 because it uses net amount share, not profit share of a type subset.
SCHEMA_EXTENDED	EXT10	EXT10_IMP	generalization_case	Italian	sales_implicit	Multi-metric / comparative	high	retail.orders, retail.order_items, retail.products, retail.categories	Dentro PLUMBING, a gennaio 2025, quanto incide 'Ball Valve 1/2-inch' sul netto totale?		scalar_percentage	share_of_total	total_net_amount, net_amount_share_pct	Distinct from INT03 because it uses net amount share, not profit share of a type subset.
SCHEMA_EXTENDED	EXT11	EXT11_CAN	generalization_case	Italian	canonical	Text filters / domain values	high	retail.orders, retail.order_items, retail.products	Quali sono i top 3 prodotti pipe-related per Profit nel 2025?		ranked_list	ranking_desc	profit	Tests text filtering on product_description plus ranking.
SCHEMA_EXTENDED	EXT11	EXT11_COL	generalization_case	Italian	sales_colloquial	Text filters / domain values	high	retail.orders, retail.order_items, retail.products	Mi dai i primi 3 prodotti pipe-related per Profit nel 2025?		ranked_list	ranking_desc	profit	Tests text filtering on product_description plus ranking.
SCHEMA_EXTENDED	EXT11	EXT11_EXE	generalization_case	Italian	sales_executive	Text filters / domain values	high	retail.orders, retail.order_items, retail.products	Nel 2025, quali sono i 3 prodotti pipe-related con il Profit più alto?		ranked_list	ranking_desc	profit	Tests text filtering on product_description plus ranking.
SCHEMA_EXTENDED	EXT11	EXT11_IMP	generalization_case	Italian	sales_implicit	Text filters / domain values	high	retail.orders, retail.order_items, retail.products	Nel 2025, quali prodotti pipe-related spingono di più il Profit?		ranked_list	ranking_desc	profit	Tests text filtering on product_description plus ranking.
SCHEMA_EXTENDED	EXT12	EXT12_CAN	generalization_case	Italian	canonical	Time intelligence	medium	retail.orders, retail.order_items, retail.stores	Per 'Zava Retail Online' nel 2025, qual è il mese con il Total Net Amount più alto?		peak_period	peak_period	total_net_amount	Time intelligence at channel/store level, distinct from full monthly breakdown.
SCHEMA_EXTENDED	EXT12	EXT12_COL	generalization_case	Italian	sales_colloquial	Time intelligence	medium	retail.orders, retail.order_items, retail.stores	Su 'Zava Retail Online' nel 2025, qual è il mese migliore per Total Net Amount?		peak_period	peak_period	total_net_amount	Time intelligence at channel/store level, distinct from full monthly breakdown.
SCHEMA_EXTENDED	EXT12	EXT12_EXE	generalization_case	Italian	sales_executive	Time intelligence	medium	retail.orders, retail.order_items, retail.stores	Nel 2025, quale mese rappresenta il picco di Total Net Amount per 'Zava Retail Online'?		peak_period	peak_period	total_net_amount	Time intelligence at channel/store level, distinct from full monthly breakdown.
SCHEMA_EXTENDED	EXT12	EXT12_IMP	generalization_case	Italian	sales_implicit	Time intelligence	medium	retail.orders, retail.order_items, retail.stores	Per 'Zava Retail Online' nel 2025, in quale mese tocchiamo il massimo di Total Net Amount?		peak_period	peak_period	total_net_amount	Time intelligence at channel/store level, distinct from full monthly breakdown.
SCHEMA_EXTENDED	EXT13	EXT13_CAN	generalization_case	Italian	canonical	Time intelligence	medium	retail.orders, retail.order_items, retail.products, retail.categories	Mostra il Total Net Amount per trimestre per la categoria GARDEN & OUTDOOR nel 2025.		quarterly_table	time_trend	total_net_amount	Tests quarter grain and category aggregation.
SCHEMA_EXTENDED	EXT13	EXT13_COL	generalization_case	Italian	sales_colloquial	Time intelligence	medium	retail.orders, retail.order_items, retail.products, retail.categories	Mi fai il Total Net Amount per trimestre di GARDEN & OUTDOOR nel 2025?		quarterly_table	time_trend	total_net_amount	Tests quarter grain and category aggregation.
SCHEMA_EXTENDED	EXT13	EXT13_EXE	generalization_case	Italian	sales_executive	Time intelligence	medium	retail.orders, retail.order_items, retail.products, retail.categories	Per la categoria GARDEN & OUTDOOR, voglio vedere nel 2025 il Total Net Amount per trimestre.		quarterly_table	time_trend	total_net_amount	Tests quarter grain and category aggregation.
SCHEMA_EXTENDED	EXT13	EXT13_IMP	generalization_case	Italian	sales_implicit	Time intelligence	medium	retail.orders, retail.order_items, retail.products, retail.categories	Nel 2025, come si distribuisce per trimestre il Total Net Amount di GARDEN & OUTDOOR?		quarterly_table	time_trend	total_net_amount	Tests quarter grain and category aggregation.
```
