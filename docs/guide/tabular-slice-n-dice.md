# Tabular slice-n-dice

## Overview
<ThemedImage src="/images/table/overview.jpg" />

The default layout includes three main panels:

1.	**Column Navigation** (left panel): This panel helps you quickly navigate through your dataset’s columns—especially useful when working with dozens or even hundreds of columns. You can use it to hide or show columns, change their render types, and reorder them.
2.	**Main Table** (center panel): Displays the data table with column distribution plots embedded in the header, providing immediate visual insights.
3.	**Row Details** (right panel): When a row is clicked, this panel displays all its column values in a structured view for deeper inspection.


## Column header plots

The header plots convey important insights at a glance, giving you an intuitive understanding of each column’s type and distribution:

- Dark green pie charts show the percentage of null values, helping you quickly assess data completeness.
- Numerical columns display histograms that reveal the shape and spread of the data.
Examples: <ThemedImage src="/images/table/header_stats_iou.jpg" imageClass="inline" /><ThemedImage src="/images/table/header_stats_confidence.jpg" imageClass="inline" />
- Categorical columns show treemaps, highlighting the relative frequency of each category.
Examples: <ThemedImage src="/images/table/header_stats_match_type.jpg" imageClass="inline" /><ThemedImage src="/images/table/header_stats_category_name.jpg" imageClass="inline" />
- Text columns come with a quick filter: <ThemedImage src="/images/table/header_stats_filename.jpg" imageClass="inline" />


### Numerical columns

Clicking on the mini plot <ThemedImage src="/images/table/header_stats_confidence.jpg" imageClass="inline" />, you will see an enlarged histogram plot along with a brush to filter values by range.

<ThemedImage src="/images/table/header_stats_card_confidence.jpg" />

### Categorical columns
Clicking on the mini plot <ThemedImage src="/images/table/header_stats_category_name.jpg" imageClass="inline" />, you will see tree map with more details and percentage for each value.

<ThemedImage src="/images/table/header_stats_card_category_name.jpg" />
