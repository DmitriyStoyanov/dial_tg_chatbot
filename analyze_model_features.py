#!/usr/bin/env python3
"""
Analyze model features from the models.json file
"""

import json
from collections import defaultdict

def analyze_models():
    """Analyze model features and parameters"""

    with open('tmp/models.json', 'r') as f:
        data = json.load(f)

    models = data['data']

    # Analyze temperature support
    temp_support = defaultdict(list)
    max_tokens_support = defaultdict(list)

    for model in models:
        model_id = model['id']
        features = model.get('features', {})

        # Temperature support
        if features.get('temperature'):
            temp_support['supported'].append(model_id)
        else:
            temp_support['not_supported'].append(model_id)

        # Check limits for max tokens info
        limits = model.get('limits', {})
        if 'max_total_tokens' in limits:
            max_tokens_support['max_total_tokens'].append(model_id)
        elif 'max_prompt_tokens' in limits:
            max_tokens_support['max_prompt_tokens'].append(model_id)
        else:
            max_tokens_support['no_limits'].append(model_id)

    print("=== TEMPERATURE SUPPORT ===")
    print(f"Models supporting temperature ({len(temp_support['supported'])}):")
    for model in temp_support['supported'][:10]:  # Show first 10
        print(f"  - {model}")
    if len(temp_support['supported']) > 10:
        print(f"  ... and {len(temp_support['supported']) - 10} more")

    print(f"\nModels NOT supporting temperature ({len(temp_support['not_supported'])}):")
    for model in temp_support['not_supported']:
        print(f"  - {model}")

    print("\n=== TOKEN LIMITS ===")
    print(f"Models with max_total_tokens: {len(max_tokens_support['max_total_tokens'])}")
    print(f"Models with max_prompt_tokens: {len(max_tokens_support['max_prompt_tokens'])}")
    print(f"Models with no limits: {len(max_tokens_support['no_limits'])}")

    # Analyze specific model families
    print("\n=== MODEL FAMILIES ANALYSIS ===")
    families = defaultdict(list)
    for model in models:
        model_id = model['id']
        if model_id.startswith('gpt-5'):
            families['gpt-5'].append(model_id)
        elif model_id.startswith('gpt-4'):
            families['gpt-4'].append(model_id)
        elif model_id.startswith('o1-') or model_id.startswith('o3-') or model_id.startswith('o4-'):
            families['reasoning'].append(model_id)
        elif 'claude' in model_id.lower():
            families['claude'].append(model_id)
        elif 'gemini' in model_id.lower():
            families['gemini'].append(model_id)
        elif 'deepseek' in model_id.lower():
            families['deepseek'].append(model_id)

    for family, models_list in families.items():
        print(f"{family}: {len(models_list)} models")
        for model in models_list[:3]:  # Show first 3
            print(f"  - {model}")
        if len(models_list) > 3:
            print(f"  ... and {len(models_list) - 3} more")

if __name__ == "__main__":
    analyze_models()