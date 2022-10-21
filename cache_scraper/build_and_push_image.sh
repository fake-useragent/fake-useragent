#!/usr/bin/env bash
docker build -t danger89/useragent_scraper .
docker push danger89/useragent_scraper:latest
