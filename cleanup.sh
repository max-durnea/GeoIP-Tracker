#!/bin/bash
echo "Cleanup script started at $(date)" >> /tmp/cleanup.log
USERS_DIR="/mnt/d/Projects/Geo-IP/GeoIP-Tracker/users"
DOWNLOADS_DIR="/mnt/d/Projects/Geo-IP/GeoIP-Tracker/downloads"
rm -rf "$USERS_DIR"/*
rm -rf "$DOWNLOADS_DIR"/*
echo "Cleanup done at $(date)" >> /tmp/cleanup.log