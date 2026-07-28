#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 20:03:05 2026

@author: Lauren
"""
#ART SCRAPE

import requests
import pandas as pd


graphql_url = "https://clientapi.prod.sothelabs.com/graphql"

auction_id = "2da6467d-b6d5-4b69-a8c3-5945c64b9dba"


def get_lot_page(offset):

    query = f"""
    query AuctionQuery {{
      auction(id: "{auction_id}", language: ENGLISH) {{
        lotCardsConnection(filter: ALL, limit: 48, offset: {offset}) {{
          totalCount
          hasNextPage
          lots {{
            lotId
            title
            creatorsDisplayTitle

            estimateV2 {{
              ... on LowHighEstimateV2 {{
                lowEstimate {{
                  amount
                }}
                highEstimate {{
                  amount
                }}
              }}
            }}

            bidState {{
              currentBidV2 {{
                amount
                currency
              }}
              numberOfBids
              reserveMet
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(
        graphql_url,
        json={"query": query}
    )

    return response.json()



all_lots = []

for offset in range(0, 400, 48):

    print("Getting offset:", offset)

    result = get_lot_page(offset)

    if "errors" in result:
        print("ERROR:")
        print(result["errors"])
        break

    page = result["data"]["auction"]["lotCardsConnection"]

    print("Returned:", len(page["lots"]))

    all_lots.extend(page["lots"])

    if not page["hasNextPage"]:
        break



print("\nTOTAL LOTS:", len(all_lots))

print("\nFIRST LOT:")
print(all_lots[0])



# -----------------------
# CLEAN DATAFRAME
# -----------------------

rows = []

for lot in all_lots:

    estimate = lot.get("estimateV2") or {}

    low = estimate.get("lowEstimate") or {}
    high = estimate.get("highEstimate") or {}

    bid = lot.get("bidState") or {}
    current = bid.get("currentBidV2") or {}

    rows.append({

        "lot_id": lot.get("lotId"),

        "artist": lot.get("creatorsDisplayTitle"),

        "title": lot.get("title"),

        "estimate_low":
            low.get("amount"),

        "estimate_high":
            high.get("amount"),

        "current_bid":
            current.get("amount"),

        "currency":
            current.get("currency"),

        "number_of_bids":
            bid.get("numberOfBids"),

        "reserve_met":
            bid.get("reserveMet")
    })


df = pd.DataFrame(rows)


print("\nCOLUMNS:")
print(df.columns)

print("\nDATA:")
print(df.head())


df.to_excel(
    "sothebys_contemporary_discoveries.xlsx",
    index=False
)

print("\nSaved!")