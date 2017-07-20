# one-tableau-online-tools

This repo contains resources helpful to Tableau users on the ONE policy team. It also contains some scripts to pull and clean certain external data sets for use on Tableau Online.

### Dimensions

This directory contains .csv files that can be useful add-ons to other data analysis in Tableau

#### country_code_mapping.csv

Use this file to look up ISO-3 country codes for any data set that uses country names. Left-join this table onto your main data set, using the 'Country' field as a join key to whichever field contains country name in your data set.

After joining, check to see if there are any null values in the new 'countryCode' field. If there are, that means that the country name in your data set is not contained in the mapping file. Please manually add the new country name and its ISO-3 code into the file and merge the new update into the Github. Or contact Kate for assistance.

Over time, we will create a list that is universally applicable to all of ONE's data sources, which will make it much easier to standardise country names across multiple data sets.

#### country_groupings.csv

This list uses ISO-3 country codes and then has multiple fields that specify whether or not a country is in a certain country group. By standardising this, we can ensure that all policy team data outputs use a consistant grouping methodology.

If you'd like to update this file - either by adding additional countries, adding additional groups, or updating groupings - please push an updated file or ask Kate for help.

Current groupings contained in this file:
* Less developed countries (currently based on [this] (https://www.un.org/development/desa/dpad/wp-content/uploads/sites/45/publication/ldc_list.pdf) list
* Sub-Saharan African country
* Fragile State (OECD definition; needs citation)
* African country

### data-pull-scripts

This directory contains python scripts for pulling and cleaning data sets. More information to come.