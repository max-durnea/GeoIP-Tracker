#!/bin/bash

USERS_DIR="/mnt/d/Projects/Geo-IP/GeoIP-Tracker/users"

rm -rf "$USERS_DIR"/*

echo "$(date): Cleared $USERS_DIR" >> /var/log/cleanup_users.log