#!/bin/bash

cqlsh db-d1 -e "truncate twitter.user;"
cqlsh db-d1 -e "truncate twitter.tweet;"
cqlsh db-d1 -e "truncate twitter.relation;"
