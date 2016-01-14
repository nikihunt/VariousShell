#!/bin/bash
host="http://10.103.16.49:9200"
indexPrefix="fast_news_all"
document="document"
file="querystr.data"
size=50000000
tmpfile="14.data"
targetfile="docid.data"
curl "$host/$indexPrefix/$document/_search?size=$size" --data-binary @$file > $tmpfile
python findOneYearDocId.py $tmpfile $targetfile
rm $tmpfile
