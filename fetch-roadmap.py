#!/usr/bin/env python3
"""
Script để fetch toàn bộ nội dung từ roadmap.sh
Fetch từ GitHub repository của developer-roadmap
"""

import requests
import json
import os
import re
import yaml

GITHUB_RAW = "https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/src/data/roadmaps/json/content"

# Các roadmap cần fetch
ROADMAPS = [
    "backend",
    "devops",
    "sql",
    "spring-boot",
    "kubernetes",
    "docker",
    "redis",
    "aws",
    "java",
    "system-design",
    "git-github",
    "cloudflare",
    "elasticsearch",
    "linux",
    "aws-best-practices",
]

def fetch_roadmap_from_github(roadmap_name):
    """Fetch roadmap content từ GitHub"""
    url = f"{GITHUB_RAW}/{roadmap_name}.md"
    print(f"\n{'='*60}")
    print(f"Fetching: {url}")
    print('='*60)

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        content = response.text
        return parse_roadmap_markdown(roadmap_name, content)

    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def parse_roadmap_markdown(name, content):
    """Parse markdown content thành structured data"""
    result = {
        'name': name,
        'title': name,
        'topics': [],
        'subtopics': [],
        'groups': [],
        'all_items': []
    }

    lines = content.split('\n')
    current_group = None
    current_subgroup = None

    for line in lines:
        stripped = line.strip()

        # Skip empty lines và comments
        if not stripped or stripped.startswith('<!--'):
            continue

        # Parse headings
        if stripped.startswith('# '):
            # Top-level heading (title)
            result['title'] = stripped[2:].strip()
        elif stripped.startswith('## '):
            # Group heading
            group_name = stripped[3:].strip()
            current_group = {'name': group_name, 'topics': [], 'subtopics': []}
            result['groups'].append(current_group)
            current_subgroup = None
        elif stripped.startswith('### '):
            # Subgroup heading
            if current_group:
                subgroup_name = stripped[4:].strip()
                current_subgroup = {'name': subgroup_name, 'items': []}
                current_group['subtopics'].append(current_subgroup)
        elif stripped.startswith('- ') or stripped.startswith('* '):
            # List item (topic)
            item = stripped[2:].strip()
            # Remove links, keep text only
            item = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', item)
            # Remove images
            item = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', item)
            # Remove extra formatting
            item = re.sub(r'[`*_~]', '', item)

            if item:
                if current_subgroup:
                    current_subgroup['items'].append(item)
                elif current_group:
                    current_group['topics'].append(item)
                else:
                    result['topics'].append(item)

                result['all_items'].append(item)

    return result


def fetch_all_roadmaps():
    """Fetch tất cả roadmaps"""
    output_dir = '/home/dattran/workspace/backend-learning/roadmap-data'
    os.makedirs(output_dir, exist_ok=True)

    results = {}

    for roadmap in ROADMAPS:
        data = fetch_roadmap_from_github(roadmap)
        if data:
            results[roadmap] = data

            # Save individual file
            output_file = os.path.join(output_dir, f"{roadmap}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  ✓ Saved: {output_file}")
            print(f"     Items: {len(data.get('all_items', []))}")

    # Create summary
    summary = {
        'roadmaps_fetched': list(results.keys()),
        'total_count': len(results),
        'items_per_roadmap': {
            name: len(data.get('all_items', []))
            for name, data in results.items()
        },
        'groups_per_roadmap': {
            name: len(data.get('groups', []))
            for name, data in results.items()
        }
    }

    output_file = os.path.join(output_dir, 'summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    # Also save as markdown for readability
    md_output = os.path.join(output_dir, 'ROADMAP_SUMMARY.md')
    with open(md_output, 'w', encoding='utf-8') as f:
        f.write("# Roadmap.sh Content Summary\n\n")
        f.write(f"Generated from GitHub: kamranahmedse/developer-roadmap\n\n")

        for name, data in results.items():
            f.write(f"## {data.get('title', name).upper()}\n\n")
            f.write(f"**Groups:** {len(data.get('groups', []))} | ")
            f.write(f"**Items:** {len(data.get('all_items', []))}\n\n")

            for group in data.get('groups', []):
                f.write(f"### {group['name']}\n")
                if group['topics']:
                    for topic in group['topics'][:10]:  # Show first 10
                        f.write(f"- {topic}\n")
                for subgroup in group.get('subtopics', []):
                    f.write(f"  - **{subgroup['name']}**:\n")
                    for item in subgroup['items'][:5]:  # Show first 5
                        f.write(f"    - {item}\n")
                f.write("\n")

            f.write("---\n\n")

    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    for name, data in results.items():
        item_count = len(data.get('all_items', []))
        group_count = len(data.get('groups', []))
        print(f"  {name}: {item_count} items, {group_count} groups")

    print(f"\nOutput directory: {output_dir}")
    print(f"Markdown summary: {md_output}")
    return results


if __name__ == '__main__':
    print("🚀 Starting roadmap.sh scraper (from GitHub)...")
    print(f"Roadmaps to fetch: {', '.join(ROADMAPS)}")

    results = fetch_all_roadmaps()
