#!/bin/bash

# create empty result file
echo "" > result.csv

# We've got 4486 products, 70 per page
# This means that we should gather data 64 times
for p in {1..64}
do 
	# print page number on screen
	echo $p

	# get data from API
	# extract json
	# extract SKU, title & product type from json
	# append to result file
	curl -s \
		https://services.mybcapps.com/bc-sf-filter/filter\?shop\=rammount.myshopify.com\&page\=$p\&limit\=70\&display\=grid\&callback\=AAA \
	| sed -nE "s/(.*)(AAA\()(.*)(\);)/\3/p" \
	| jq -r '.products | .[] | [.skus[0], .title, .product_type] | @csv' \
	>> result.csv
done

