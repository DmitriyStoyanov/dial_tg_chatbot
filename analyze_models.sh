#!/bin/bash

# Set your DIAL API configuration
# Make sure DIAL_API_URL and DIAL_API_KEY are set in your environment

# Function to get models data
get_models() {
    curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY"
}

echo "=== Models Analysis Commands ==="
echo

echo "1. Show all models with their prompt and completion prices (sorted by prompt price):"
echo 'curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | jq -r '\''.data[] | select(.pricing != null) | "\(.display_name) (\(.display_version // "N/A")): Prompt: \(.pricing.prompt), Completion: \(.pricing.completion)"'\'' | sort -k3 -n'
echo

echo "2. Show models with prompt price less than 0.000001 (very cheap):"
echo 'curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | jq -r '\''.data[] | select(.pricing != null and (.pricing.prompt | tonumber) < 0.000001) | "\(.display_name) (\(.display_version // "N/A")): Prompt: \(.pricing.prompt), Completion: \(.pricing.completion)"'\'''
echo

echo "3. Show top 10 cheapest models by prompt price:"
echo 'curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | jq -r '\''.data[] | select(.pricing != null) | [.display_name, (.display_version // "N/A"), .pricing.prompt, .pricing.completion] | @tsv'\'' | sort -k3 -n | head -10 | column -t'
echo

echo "4. Show models with completion price less than 0.000005:"
echo 'curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | jq -r '\''.data[] | select(.pricing != null and (.pricing.completion | tonumber) < 0.000005) | "\(.display_name) (\(.display_version // "N/A")): Prompt: \(.pricing.prompt), Completion: \(.pricing.completion)"'\'''
echo

echo "5. Show cheapest models in each category (Text Generation, Image Generation, etc.):"
echo 'curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | jq -r '\''.data[] | select(.pricing != null and .description_keywords != null) | .description_keywords[] as $keyword | select($keyword == "Text Generation" or $keyword == "Image Generation" or $keyword == "Reasoning") | [$keyword, .display_name, (.display_version // "N/A"), .pricing.prompt, .pricing.completion] | @tsv'\'' | sort -k1,1 -k4,4n | awk '\''!seen[$1]++ {print}'\'' | column -t'
echo

echo "6. Compare pricing across model families (GPT, Claude, Gemini):"
echo 'curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | jq -r '\''.data[] | select(.pricing != null) | if (.display_name | test("GPT|gpt")) then "GPT" elif (.display_name | test("Claude|claude")) then "Claude" elif (.display_name | test("Gemini|gemini")) then "Gemini" elif (.display_name | test("Nova|nova")) then "Amazon Nova" else "Other" end as $family | [$family, .display_name, (.display_version // "N/A"), .pricing.prompt, .pricing.completion] | @tsv'\'' | sort -k1,1 -k4,4n | column -t'
echo

echo "7. Show free models (prompt price = 0):"
echo 'curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | jq -r '\''.data[] | select(.pricing != null and (.pricing.prompt | tonumber) == 0) | "\(.display_name) (\(.display_version // "N/A")): Completion: \(.pricing.completion)"'\'''
echo

echo "8. Calculate total cost for 1000 prompt tokens + 1000 completion tokens:"
echo 'curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | jq -r '\''.data[] | select(.pricing != null) | [.display_name, (.display_version // "N/A"), (.pricing.prompt | tonumber * 1000 + .pricing.completion | tonumber * 1000)] | "\(.[0]) (\(.[1])): $\(.[2])"'\'' | sort -k2 -n | head -10'