# Quick Commands for Model Price Analysis

## Prerequisites
```bash
export DIAL_API_URL="your_dial_api_url"
export DIAL_API_KEY="your_dial_api_key"
```

## Essential Commands

### 1. Top 10 Cheapest Models by Prompt Price
```bash
curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | jq -r '.data[] | select(.pricing != null and .display_name != null) | [.display_name, (.display_version // "N/A"), .pricing.prompt, .pricing.completion] | @tsv' | sort -k3 -n | head -10 | column -t
```

### 2. Models with Prompt Price < $0.000001 (Ultra-cheap)
```bash
curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | jq -r '.data[] | select(.pricing != null and .display_name != null and (.pricing.prompt | tonumber) < 0.000001 and (.pricing.prompt | tonumber) > 0) | "\(.display_name) (\(.display_version // "N/A")): Prompt: $\(.pricing.prompt), Completion: $\(.pricing.completion)"'
```

### 3. Free Models (Prompt Price = $0)
```bash
curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | jq -r '.data[] | select(.pricing != null and .display_name != null and (.pricing.prompt | tonumber) == 0) | "\(.display_name) (\(.display_version // "N/A")): Completion: $\(.pricing.completion)"'
```

### 4. Cost for 1M Tokens (1M prompt + 1M completion) - Top 10 Cheapest
```bash
curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | jq -r '.data[] | select(.pricing != null and .display_name != null) | [.display_name, (.display_version // "N/A"), (.pricing.prompt | tonumber * 1000000 + .pricing.completion | tonumber * 1000000)] | "\(.[0]) (\(.[1])): $\(.[2])"' | sort -k2 -n | head -10
```

### 5. Cheapest Text Generation Models
```bash
curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | jq -r '.data[] | select(.pricing != null and .display_name != null and (.description_keywords // [] | contains(["Text Generation"]))) | [.display_name, (.display_version // "N/A"), .pricing.prompt, .pricing.completion] | @tsv' | sort -k3 -n | head -10 | column -t
```

### 6. Cheapest Image Generation Models
```bash
curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | jq -r '.data[] | select(.pricing != null and .display_name != null and (.description_keywords // [] | contains(["Image Generation"]))) | [.display_name, (.display_version // "N/A"), .pricing.prompt, .pricing.completion] | @tsv' | sort -k3 -n | head -10 | column -t
```

### 7. Compare Model Families (GPT vs Claude vs Gemini vs Amazon)
```bash
curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | jq -r '.data[] | select(.pricing != null and .display_name != null) | if (.display_name | test("GPT|gpt")) then "GPT" elif (.display_name | test("Claude|claude")) then "Claude" elif (.display_name | test("Gemini|gemini")) then "Gemini" elif (.display_name | test("Nova|nova|Amazon")) then "Amazon" else "Other" end as $family | [$family, .display_name, (.display_version // "N/A"), .pricing.prompt, .pricing.completion] | @tsv' | sort -k1,1 -k4,4n | column -t
```

### 8. Models with Completion Price < $0.000005
```bash
curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY" | jq -r '.data[] | select(.pricing != null and .display_name != null and (.pricing.completion | tonumber) < 0.000005) | "\(.display_name) (\(.display_version // "N/A")): Prompt: $\(.pricing.prompt), Completion: $\(.pricing.completion)"'
```

## Key Findings from Your Data

**Cheapest Models by Prompt Price:**
1. Amazon Nova Micro: $0.000000035
2. Amazon Nova Lite: $0.00000006
3. Google Gemini 2.0 Flash Lite: $0.000000075
4. Google Gemini 2.0 Flash: $0.0000001
5. GPT OSS 120B: $0.00000015
6. OpenAI GPT-4o mini: $0.000000165

**Free Models (Prompt = $0):**
- DALL-E 3, Stable Diffusion models, Google Imagen (image generation)

**Best Value for Text Generation:**
- Amazon Nova Micro: $0.000000035 prompt + $0.00000014 completion
- Amazon Nova Lite: $0.00000006 prompt + $0.00000024 completion
- Google Gemini models: Very competitive pricing