#!/bin/bash

FREE_KB=$(df -Pk / | awk 'NR==2 {print $4}')
FREE_GB=$(awk "BEGIN {printf \"%.2f\", $FREE_KB / 1024 / 1024}")

echo "================================"
echo "       KALI LINUX DISK CHECK"
echo "================================"
echo ""
echo "Sistemde bos yeriniz: ${FREE_GB} GB"
echo ""
echo "================================"
