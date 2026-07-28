# Sotheby's Contemporary Discoveries Auction Analysis

## Overview

This project analyzes Sotheby's Contemporary Discoveries auction data to understand pricing trends, artist representation, and bidding activity.

I built a Python data pipeline that:
- Scraped auction lot data from Sotheby's GraphQL API
- Collected 373 contemporary art lots
- Analyzed estimates, bidding activity, and market interest

## Data Collection

Data was collected using:
- Python
- Requests
- GraphQL API queries

The dataset includes:
- Artist
- Lot title
- Estimate range
- Current bid
- Number of bids
- Reserve status

## Analysis Performed

The project explores:

### Pricing Analysis
- Estimate midpoint calculations
- Highest valued lots
- Estimate distributions

### Artist Analysis
- Most represented artists
- Average estimate by artist
- Artist-level market trends

### Auction Activity
- Number of bids per lot
- Bid-to-estimate ratios
- Auction momentum scoring

## Key Metrics

Dataset size:
- 373 auction lots
- 330 lots with active bidding data

## Tools

- Python
- Pandas
- Matplotlib
- Requests
- BeautifulSoup
- OpenPyXL

## Project Structure

```
sothebys-auction-analysis/
│
├── sothebys_scraper.py
├── sothebys_analysis.py
├── sothebys_contemporary_discoveries.xlsx
├── requirements.txt
└── README.md
```

## Visualizations

### Estimate Distribution

![Estimate Distribution](estimate_distribution.png)

### Bid Activity vs Estimated Value

![Bid vs Estimate](bid_vs_estimate.png)


## Future Improvements

Potential next steps:
- Add auction result data after sale completion
- Compare estimate accuracy versus final hammer prices
- Build predictive models for auction performance
- Create an interactive dashboard
