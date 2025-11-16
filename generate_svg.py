#!/usr/bin/env python3
"""
Dynamic GitHub Profile SVG Generator
Fetches your GitHub stats and generates beautiful SVG images
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Tuple

# Configuration
GITHUB_USERNAME = "alaeddinedaly"
GITHUB_TOKEN = ""  # Optional: Add your token for higher rate limits

# Colors
COLORS = {
    "dark": {
        "bg": "#0d1117",
        "text_primary": "#c9d1d9",
        "text_secondary": "#8b949e",
        "accent": "#58a6ff",
        "accent_glow": "rgba(88, 166, 255, 0.1)",
        "border": "#21262d",
        "card_bg": "#161b22",
    },
    "light": {
        "bg": "#ffffff",
        "text_primary": "#24292f",
        "text_secondary": "#57606a",
        "accent": "#0969da",
        "accent_glow": "rgba(9, 105, 218, 0.1)",
        "border": "#d0d7de",
        "card_bg": "#f6f8fa",
    }
}

def fetch_github_data() -> Dict:
    """Fetch user data from GitHub API"""
    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    # User data
    user_url = f"https://api.github.com/users/{GITHUB_USERNAME}"
    user_data = requests.get(user_url, headers=headers).json()
    
    # Repos data
    repos_url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100"
    repos_data = requests.get(repos_url, headers=headers).json()
    
    # Calculate stats
    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos_data if isinstance(repo, dict))
    total_forks = sum(repo.get("forks_count", 0) for repo in repos_data if isinstance(repo, dict))
    
    # Get languages
    languages = {}
    for repo in repos_data:
        if isinstance(repo, dict) and repo.get("language"):
            lang = repo["language"]
            languages[lang] = languages.get(lang, 0) + 1
    
    # Sort languages by count
    top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        "name": user_data.get("name", GITHUB_USERNAME),
        "bio": user_data.get("bio", ""),
        "followers": user_data.get("followers", 0),
        "following": user_data.get("following", 0),
        "public_repos": user_data.get("public_repos", 0),
        "total_stars": total_stars,
        "total_forks": total_forks,
        "top_languages": top_languages,
        "avatar_url": user_data.get("avatar_url", ""),
        "updated_at": datetime.now().strftime("%B %d, %Y at %H:%M UTC")
    }

def create_language_bars(languages: List[Tuple[str, int]], theme: str, y_offset: int = 0) -> str:
    """Create language usage bars"""
    if not languages:
        return ""
    
    colors_map = {
        "Python": "#3776ab",
        "TypeScript": "#3178c6",
        "JavaScript": "#f7df1e",
        "Java": "#b07219",
        "Kotlin": "#A97BFF",
        "HTML": "#e34c26",
        "CSS": "#563d7c",
        "Go": "#00ADD8",
        "Rust": "#dea584",
        "C++": "#f34b7d",
    }
    
    total = sum(count for _, count in languages)
    svg_parts = []
    
    for i, (lang, count) in enumerate(languages):
        percentage = (count / total) * 100
        y_pos = y_offset + i * 40
        bar_width = (percentage / 100) * 280
        color = colors_map.get(lang, COLORS[theme]["accent"])
        
        svg_parts.append(f'''
            <g transform="translate(0, {y_pos})">
                <text x="0" y="15" class="lang-name">{lang}</text>
                <text x="320" y="15" class="lang-percent">{percentage:.1f}%</text>
                <rect x="0" y="22" width="300" height="6" rx="3" fill="{COLORS[theme]['border']}"/>
                <rect x="0" y="22" width="{bar_width}" height="6" rx="3" fill="{color}">
                    <animate attributeName="width" from="0" to="{bar_width}" dur="1s" fill="freeze"/>
                </rect>
            </g>
        ''')
    
    return ''.join(svg_parts)

def create_stat_card(icon: str, value: str, label: str, x: int, y: int, theme: str) -> str:
    """Create a stat card with icon"""
    return f'''
        <g transform="translate({x}, {y})">
            <rect width="140" height="80" rx="8" fill="{COLORS[theme]['card_bg']}" stroke="{COLORS[theme]['border']}" stroke-width="1"/>
            <text x="20" y="30" class="stat-icon">{icon}</text>
            <text x="20" y="55" class="stat-value">{value}</text>
            <text x="20" y="70" class="stat-label">{label}</text>
        </g>
    '''

def generate_svg(data: Dict, theme: str = "dark") -> str:
    """Generate the complete SVG"""
    c = COLORS[theme]
    
    # Calculate total height based on content
    base_height = 680
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="900" height="{base_height}" viewBox="0 0 900 {base_height}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&amp;display=swap');
            
            * {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }}
            
            .title {{
                font-size: 32px;
                font-weight: 700;
                fill: {c['text_primary']};
            }}
            
            .subtitle {{
                font-size: 16px;
                font-weight: 400;
                fill: {c['text_secondary']};
            }}
            
            .section-title {{
                font-size: 18px;
                font-weight: 600;
                fill: {c['text_primary']};
            }}
            
            .stat-icon {{
                font-size: 24px;
            }}
            
            .stat-value {{
                font-size: 22px;
                font-weight: 700;
                fill: {c['text_primary']};
            }}
            
            .stat-label {{
                font-size: 12px;
                fill: {c['text_secondary']};
            }}
            
            .lang-name {{
                font-size: 14px;
                font-weight: 500;
                fill: {c['text_primary']};
            }}
            
            .lang-percent {{
                font-size: 13px;
                fill: {c['text_secondary']};
            }}
            
            .updated-text {{
                font-size: 11px;
                fill: {c['text_secondary']};
            }}
            
            .accent-text {{
                fill: {c['accent']};
                font-weight: 600;
            }}
            
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            .fade-in {{
                animation: fadeIn 0.6s ease-out forwards;
            }}
        </style>
        
        <linearGradient id="glow" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:{c['accent']};stop-opacity:0.3" />
            <stop offset="100%" style="stop-color:{c['accent']};stop-opacity:0" />
        </linearGradient>
    </defs>
    
    <!-- Background -->
    <rect width="900" height="{base_height}" fill="{c['bg']}" rx="12"/>
    
    <!-- Header with glow effect -->
    <rect x="0" y="0" width="900" height="140" fill="url(#glow)" opacity="0.3"/>
    
    <!-- Main Content -->
    <g transform="translate(40, 40)" class="fade-in">
        <!-- Title Section -->
        <text x="0" y="30" class="title">👋 Hey, I'm {data['name']}</text>
        <text x="0" y="60" class="subtitle">{data['bio'] or 'Full-Stack Developer • AI Enthusiast • Problem Solver'}</text>
        
        <!-- Decorative line -->
        <line x1="0" y1="85" x2="150" y2="85" stroke="{c['accent']}" stroke-width="3" stroke-linecap="round"/>
    </g>
    
    <!-- Stats Grid -->
    <g transform="translate(40, 160)">
        {create_stat_card("📦", str(data['public_repos']), "Repositories", 0, 0, theme)}
        {create_stat_card("⭐", str(data['total_stars']), "Stars Earned", 160, 0, theme)}
        {create_stat_card("🍴", str(data['total_forks']), "Forks", 320, 0, theme)}
        {create_stat_card("👥", str(data['followers']), "Followers", 480, 0, theme)}
        {create_stat_card("🔗", str(data['following']), "Following", 640, 0, theme)}
    </g>
    
    <!-- Languages Section -->
    <g transform="translate(40, 280)">
        <text x="0" y="0" class="section-title">🚀 Top Languages & Technologies</text>
        <g transform="translate(0, 25)">
            {create_language_bars(data['top_languages'], theme)}
        </g>
    </g>
    
    <!-- Current Focus -->
    <g transform="translate(40, 520)">
        <text x="0" y="0" class="section-title">💡 Currently Focused On</text>
        <text x="0" y="30" class="subtitle">Building <tspan class="accent-text">AI-powered applications</tspan> • Exploring <tspan class="accent-text">full-stack development</tspan></text>
        <text x="0" y="55" class="subtitle">Creating <tspan class="accent-text">secure & scalable systems</tspan> • Learning <tspan class="accent-text">cutting-edge technologies</tspan></text>
    </g>
    
    <!-- Footer -->
    <g transform="translate(40, {base_height - 40})">
        <text x="0" y="0" class="updated-text">Last updated: {data['updated_at']}</text>
        <text x="700" y="0" class="updated-text">Generated with ❤️ and Python</text>
    </g>
</svg>'''
    
    return svg

def main():
    """Main function to generate both light and dark SVGs"""
    print("🚀 Fetching GitHub data...")
    data = fetch_github_data()
    
    print(f"✅ Data fetched for {data['name']}")
    print(f"   📦 Repos: {data['public_repos']}")
    print(f"   ⭐ Stars: {data['total_stars']}")
    print(f"   👥 Followers: {data['followers']}")
    
    print("\n🎨 Generating SVGs...")
    
    # Generate dark mode
    dark_svg = generate_svg(data, "dark")
    with open("dark_mode.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    print("   ✅ dark_mode.svg created")
    
    # Generate light mode
    light_svg = generate_svg(data, "light")
    with open("light_mode.svg", "w", encoding="utf-8") as f:
        f.write(light_svg)
    print("   ✅ light_mode.svg created")
    
    print("\n✨ All done! SVGs generated successfully.")

if __name__ == "__main__":
    main()
