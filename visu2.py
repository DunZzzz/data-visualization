#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 emilien <emilien@emilien-pc>
#

import argparse
import pandas as pd
import geopandas as gpd
import geoplot as gplt
import matplotlib.pyplot as plt

import mapclassify

def ged171_df():
    return pd.read_csv("./ged171.csv")

def filters_years(df, start_year, period):
    return df[(df.year >= start_year) & (df.year < (start_year + period))]

def add_tot_deaths_col(df, civilians_only):
    df['tot_deaths'] = df['deaths_civilians' if civilians_only else 'best']
    return df[(df.tot_deaths > 0) & df.tot_deaths.notnull()]

def get_country_df(df):
    return df.groupby(['country'])['tot_deaths'].agg('sum')

# Index(['id', 'year', 'active_year', 'type_of_violence', 'conflict_new_id',
# 'conflict_name', 'dyad_new_id', 'dyad_name', 'side_a_new_id', 'gwnoa',
# 'side_a', 'side_b_new_id', 'gwnob', 'side_b', 'number_of_sources',
# 'source_article', 'source_office', 'source_date', 'source_headline',
# 'source_original', 'where_prec', 'where_coordinates', 'adm_1', 'adm_2',
# 'latitude', 'longitude', 'geom_wkt', 'priogrid_gid', 'country',
# 'country_id', 'region', 'event_clarity', 'date_prec', 'date_start',
# 'date_end', 'deaths_a', 'deaths_b', 'deaths_civilians',
# 'deaths_unknown', 'best', 'low', 'high'],
# gplt.kdeplot(gdf.head(n), ax=ax, tresh=0.5, cmap='Reds', n_levels=20)
# print(gdf.geometry.notnull())

# gplt.quadtree(gdf, ax=ax, hue=gdf.tot_deaths, cmap='Reds', edgecolor='white')
# world.plot(ax=ax, color='none', edgecolor='black')

# geoplot.polyplot(boroughs, ax=ax, zorder=1)


def main(args):
    df = ged171_df()

    df = filters_years(df, args.start_year, args.period)
    df = add_tot_deaths_col(df, args.civilians_only)
    cdf = get_country_df(df)
    world = gpd.read_file(
        gpd.datasets.get_path('naturalearth_lowres')
    )

    w = pd.merge(world, cdf, how="left", left_on="name", right_on="country")

    tdf = df.sort_values(['tot_deaths'], ascending=False).head(args.highest_casualties_events)
    print(tdf['tot_deaths'])
    gdf = gpd.GeoDataFrame(tdf, geometry=gpd.points_from_xy(tdf.longitude, tdf.latitude))

    ax = world.plot(edgecolor='black', color="lightgray")
    ax = w.plot(ax=ax, edgecolor='black', column="tot_deaths", legend=True,
                scheme="percentiles",
                cmap="viridis",
                missing_kwds={
                    "color": "lightgrey",
                    "label": "Missing values",
                })
    gdf['markersize'] = gdf['tot_deaths'].apply(lambda x: x if x < 5000 else 5000)
    gdf.plot(ax=ax, color='red', legend=True, alpha=0.5, edgecolor='k', markersize=gdf['markersize'])

    for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf.date_start):
        ax.annotate(label, xy=(x, y), xytext=(0, 0), textcoords="offset points")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_year", help="Choose the start year you wish to start the conflict at", type=int, default=2015)
    parser.add_argument("--period", help="How many year after start year should the research be made for (higher=slower)", type=int, default=1)
    parser.add_argument("--civilians_only", help="Whether to take only civilians deaths into account", type=bool, default=False)
    parser.add_argument("--highest_casualties_events", help="Number of events to show on the map", type=int, default=10)
    args = parser.parse_args()
    main(args)
