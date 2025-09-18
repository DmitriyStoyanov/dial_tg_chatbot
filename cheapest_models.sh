#!/bin/bash

# Cheapest Models Analysis Script
# Make sure DIAL_API_URL and DIAL_API_KEY are set in your environment

echo "🔍 CHEAPEST MODELS ANALYSIS"
echo "=================================="
echo

echo "💰 TOP 15 CHEAPEST MODELS BY PROMPT PRICE:"
echo "-------------------------------------------"
curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | \
jq -r '.data[] | select(.pricing != null and .display_name != null) | [.display_name, (.display_version // "N/A"), .pricing.prompt, .pricing.completion] | @tsv' | \
sort -k3 -n | head -15 | \
awk 'BEGIN{printf "%-40s %-20s %-15s %-15s\n", "MODEL", "VERSION", "PROMPT", "COMPLETION"; print "=================================================================================="} {printf "%-40s %-20s %-15s %-15s\n", $1" "$2, $3, $4, $5}'

echo
echo "🆓 FREE MODELS (Prompt Price = 0):"
echo "-----------------------------------"
curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | \
jq -r '.data[] | select(.pricing != null and .display_name != null and (.pricing.prompt | tonumber) == 0) | "\(.display_name) (\(.display_version // "N/A")): Completion: \(.pricing.completion)"'

echo
echo "⚡ ULTRA-CHEAP MODELS (Prompt < $0.000001):"
echo "--------------------------------------------"
curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | \
jq -r '.data[] | select(.pricing != null and .display_name != null and (.pricing.prompt | tonumber) < 0.000001 and (.pricing.prompt | tonumber) > 0) | "\(.display_name) (\(.display_version // "N/A")): Prompt: $\(.pricing.prompt), Completion: $\(.pricing.completion)"'

echo
echo "💡 COST FOR 1M TOKENS (1M prompt + 1M completion):"
echo "---------------------------------------------------"
curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | \
jq -r '.data[] | select(.pricing != null and .display_name != null) | [.display_name, (.display_version // "N/A"), (.pricing.prompt | tonumber * 1000000 + .pricing.completion | tonumber * 1000000)] | "\(.[0]) (\(.[1])): $\(.[2])"' | \
sort -k2 -n | head -10

echo
echo "🏆 CHEAPEST BY CATEGORY:"
echo "------------------------"
echo "Text Generation Models:"
curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | \
jq -r '.data[] | select(.pricing != null and .display_name != null and (.description_keywords // [] | contains(["Text Generation"]))) | [.display_name, (.display_version // "N/A"), .pricing.prompt] | @tsv' | \
sort -k3 -n | head -5 | \
awk '{printf "  %-40s %-20s $%s\n", $1" "$2, $3, $4}'

echo
echo "Image Generation Models:"
curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | \
jq -r '.data[] | select(.pricing != null and .display_name != null and (.description_keywords // [] | contains(["Image Generation"]))) | [.display_name, (.display_version // "N/A"), .pricing.prompt] | @tsv' | \
sort -k3 -n | head -5 | \
awk '{printf "  %-40s %-20s $%s\n", $1" "$2, $3, $4}'