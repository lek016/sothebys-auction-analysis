#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 20:05:43 2026

@author: Lauren
"""

# ============================================================
# Sotheby's Contemporary Discoveries Auction Analysis
#
# Purpose:
# Analyze auction estimates, bidding activity, and
# artist performance using scraped Sotheby's auction data
# ============================================================

# Import Data

import os
import pandas as pd

os.chdir("/Users/Lauren/Desktop/Folder")

print(os.getcwd())

df = pd.read_excel("sothebys_contemporary_discoveries.xlsx")


# Data Prep

df["currency"].value_counts()

# Calculate midpoint of auction estimate range
df["estimate_midpoint"] = (
    df["estimate_low"] + df["estimate_high"]
) / 2


print(
    df[
        [
            "title",
            "estimate_low",
            "estimate_high",
            "estimate_midpoint"
        ]
    ].head()
)


# Auction Value Analysis
# Identify highest estimated artworks

print(df["estimate_midpoint"].describe())


most_expensive = df.sort_values(
    "estimate_midpoint",
    ascending=False
)

print(
    most_expensive[
        [
            "artist",
            "title",
            "estimate_midpoint"
        ]
    ].head(10)
)


# Artist Representation Analysis
# Find artists with the most works in auction

artist_counts = df["artist"].value_counts()

print(artist_counts.head(15))


# Estimate Range Analysis
# Analyze uncertainty in artwork valuations

df["estimate_range"] = (
    df["estimate_high"] - df["estimate_low"]
)


print(
    df[
        [
            "artist",
            "title",
            "estimate_low",
            "estimate_high",
            "estimate_range"
        ]
    ]
    .sort_values(
        "estimate_range",
        ascending=False
    )
    .head(10)
)


# Bidding Competition Analysis
# Identify lots generating the most bidder interest

print(df["number_of_bids"].describe())


most_competitive = df.sort_values(
    "number_of_bids",
    ascending=False
)


print(
    most_competitive[
        [
            "artist",
            "title",
            "number_of_bids",
            "current_bid"
        ]
    ].head(10)
)


# Bid Performance Analysis
# Compare current bids against estimated value

df["bid_vs_estimate"] = (
    df["current_bid"] /
    df["estimate_midpoint"]
)


print(
    df[
        [
            "artist",
            "title",
            "current_bid",
            "estimate_midpoint",
            "bid_vs_estimate"
        ]
    ]
    .sort_values(
        "bid_vs_estimate",
        ascending=False
    )
    .head(10)
)


# Visualization
# Distribution of artwork estimates

import matplotlib.pyplot as plt


plt.hist(df["estimate_midpoint"], bins=30)

plt.xlabel("Estimate Midpoint ($)")
plt.ylabel("Number of Lots")
plt.title(
    "Distribution of Sotheby's Contemporary Discoveries Estimates"
)

plt.savefig("estimate_distribution.png", bbox_inches="tight")

plt.show()


# Artist-Level Performance Analysis
# Compare artists by volume and average estimate

artist_summary = (
    df.groupby("artist")
    .agg(
        number_of_lots=("title","count"),
        average_estimate=("estimate_midpoint","mean")
    )
    .sort_values(
        "number_of_lots",
        ascending=False
    )
)


print(artist_summary.head(15))


# Auction Momentum Score
# Combine bidder interest and price performance

df["auction_momentum"] = (
    df["number_of_bids"] *
    df["bid_vs_estimate"]
)


hot_lots = df.sort_values(
    "auction_momentum",
    ascending=False
)


print(
    hot_lots[
        [
            "artist",
            "title",
            "number_of_bids",
            "current_bid",
            "bid_vs_estimate"
        ]
    ].head(10)
)

# Correlation Analysis
# Examine relationship between bidding activity and current artwork prices

correlation = df[
    [
        "number_of_bids",
        "current_bid",
        "estimate_midpoint"
    ]
].corr()

print(correlation)

# Estimate vs Current Bid Visualization
# Identify artworks exceeding expectations

plt.figure(figsize=(8,6))

plt.scatter(
    df["estimate_midpoint"],
    df["current_bid"]
)

plt.xlabel("Estimated Value ($)")
plt.ylabel("Current Bid ($)")
plt.title(
    "Sotheby's Lots: Estimated Value vs Current Bid"
)

plt.savefig("bid_vs_estimate.png", bbox_inches="tight")

plt.show()

# Artist Market Performance
# Rank artists by average bidding performance

artist_performance = (
    df.groupby("artist")
    .agg(
        number_of_lots=("title","count"),
        average_bid=("current_bid","mean"),
        average_estimate=("estimate_midpoint","mean"),
        average_bid_ratio=("bid_vs_estimate","mean")
    )
    .sort_values(
        "average_bid_ratio",
        ascending=False
    )
)


print(
    artist_performance[
        artist_performance["number_of_lots"] >= 2
    ]
    .head(15)
)

# Undervalued Lots
# Lots where current bids are far below estimates

undervalued = df.sort_values(
    "bid_vs_estimate",
    ascending=True
)


print(
    undervalued[
        [
            "artist",
            "title",
            "estimate_midpoint",
            "current_bid",
            "bid_vs_estimate"
        ]
    ].head(10)
)
