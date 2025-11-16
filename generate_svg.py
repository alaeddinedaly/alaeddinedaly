#!/usr/bin/env python3
"""
ASCII Art GitHub Profile Generator
Creates a terminal-style profile with ASCII art and live stats
"""

import requests
import os
from datetime import datetime
from typing import Dict, List
from PIL import Image
import io

# Configuration
GITHUB_USERNAME = "alaeddinedaly"
GITHUB_TOKEN = os.getenv('GH_TOKEN', '')

# ASCII art characters for image conversion
ASCII_CHARS = ['@', '#', '%', '*', '+', '=', '-', ':', '.', ' ']

def fetch_github_stats() -> Dict:
    """Fetch comprehensive GitHub statistics"""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}
    
    # User data
    user_url = f"https://api.github.com/users/{GITHUB_USERNAME}"
    user_data = requests.get(user_url, headers=headers).json()
    
    # Repos
    repos_url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100"
    repos = requests.get(repos_url, headers=headers).json()
    
    # Calculate stats
    total_stars = sum(r.get('stargazers_count', 0) for r in repos if isinstance(r, dict))
    total_forks = sum(r.get('forks_count', 0) for r in repos if isinstance(r, dict))
    
    # Languages
    languages = {}
    for repo in repos:
        if isinstance(repo, dict):
            lang_url = repo.get('languages_url')
            if lang_url:
                lang_data = requests.get(lang_url, headers=headers).json()
                for lang, bytes_count in lang_data.items():
                    languages[lang] = languages.get(lang, 0) + bytes_count
    
    top_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:4]
    lang_names = [lang for lang, _ in top_langs]
    
    # Get total commits (approximate from events)
    events_url = f"https://api.github.com/users/{GITHUB_USERNAME}/events/public?per_page=100"
    events = requests.get(events_url, headers=headers).json()
    
    # Count contributed repos
    contributed_repos = set()
    for repo in repos:
        if isinstance(repo, dict) and not repo.get('fork', False):
            contributed_repos.add(repo['name'])
    
    # Calculate account age
    created_at = datetime.strptime(user_data['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    age_delta = datetime.now() - created_at
    years = age_delta.days // 365
    months = (age_delta.days % 365) // 30
    days = (age_delta.days % 365) % 30
    
    return {
        'name': user_data.get('name', GITHUB_USERNAME),
        'login': user_data.get('login', GITHUB_USERNAME),
        'bio': user_data.get('bio', ''),
        'location': user_data.get('location', 'Unknown'),
        'company': user_data.get('company', ''),
        'repos': user_data.get('public_repos', 0),
        'stars': total_stars,
        'forks': total_forks,
        'followers': user_data.get('followers', 0),
        'following': user_data.get('following', 0),
        'contributed_repos': len(contributed_repos),
        'languages': ', '.join(lang_names) if lang_names else 'Not available',
        'account_age': f"{years} years, {months} months, {days} days",
        'avatar_url': user_data.get('avatar_url'),
        'updated': datetime.now().strftime('%B %d, %Y at %H:%M UTC')
    }

def download_and_convert_avatar(url: str, width: int = 40) -> List[str]:
    """Download avatar and convert to ASCII art"""
    try:
        response = requests.get(url)
        img = Image.open(io.BytesIO(response.content))
        
        # Convert to grayscale
        img = img.convert('L')
        
        # Resize maintaining aspect ratio
        aspect_ratio = img.height / img.width
        new_height = int(aspect_ratio * width * 0.55)  # 0.55 to account for character height
        img = img.resize((width, new_height))
        
        # Convert to ASCII
        pixels = img.getdata()
        ascii_lines = []
        
        for i in range(0, len(pixels), width):
            line = ''
            for pixel in pixels[i:i+width]:
                line += ASCII_CHARS[pixel // 25]
            ascii_lines.append(line)
        
        return ascii_lines
    except Exception as e:
        print(f"Error converting avatar: {e}")
        # Return a simple placeholder
        return [
            "  @@@@@@@@@@  ",
            " @@@@@@@@@@@@ ",
            "@@@@@@@@@@@@@@",
            "@@@@@@@@@@@@@@",
            "@@@@@@@@@@@@@@",
            "@@@@@@@@@@@@@@",
            " @@@@@@@@@@@@ ",
            "  @@@@@@@@@@  "
        ] * 5

def create_readme(stats: Dict, ascii_art: List[str]) -> str:
    """Generate the complete README with ASCII art and stats"""
    
    # Pad ASCII art lines to consistent width
    max_ascii_width = max(len(line) for line in ascii_art) if ascii_art else 50
    padded_ascii = [line.ljust(max_ascii_width) for line in ascii_art]
    
    # Create the stats sections
    lines = []
    
    # Header line
    header = f"{stats['login']}@github"
    separator = "—" * 80
    lines.append(f"{' ' * max_ascii_width}  {header}—{separator[:77-len(header)]}")
    
    # Info sections with ASCII art on the left
    info_lines = [
        ("OS:", f"Tunis, Tunisia | {stats['location']}"),
        ("Uptime:", stats['account_age']),
        ("Host:", stats['company'] if stats['company'] else "Independent Developer"),
        ("Shell:", "Python, TypeScript, Java, Kotlin"),
        ("IDE:", "Your preferred IDEs here"),
        ("", ""),
        ("Languages.Programming:", stats['languages']),
        ("Languages.Framework:", "React, Spring, Node.js (update as needed)"),
        ("Languages.Real:", "Arabic, French, English (update as needed)"),
        ("", ""),
        ("Projects.AI:", "Storyboard Generator, NexusDown"),
        ("Projects.Backend:", "Secure File Service"),
        ("Projects.Frontend:", "Portfolio Website"),
        ("Projects.Tools:", "Zip-it Compression Tool"),
    ]
    
    # Combine ASCII art with info
    for i, (label, value) in enumerate(info_lines):
        ascii_line = padded_ascii[i] if i < len(padded_ascii) else ' ' * max_ascii_width
        if label:
            lines.append(f"{ascii_line}  .{label}{'.' * (25-len(label))}{value}")
        else:
            lines.append(f"{ascii_line}  .")
    
    # Fill remaining ASCII art lines
    for i in range(len(info_lines), len(padded_ascii)):
        lines.append(f"{padded_ascii[i]}  .")
    
    # Contact section
    lines.append("")
    lines.append(f"{' ' * max_ascii_width}  — Contact—{separator[:71]}")
    
    contact_lines = [
        ("Email.Personal:", "your.email@example.com"),
        ("Email.Work:", "work.email@company.com (if applicable)"),
        ("LinkedIn:", "linkedin.com/in/yourprofile"),
        ("Twitter:", "@yourhandle"),
        ("Portfolio:", "alaeddinedaly.github.io/portfolio"),
    ]
    
    for label, value in contact_lines:
        lines.append(f"{' ' * max_ascii_width}  .{label}{'.' * (25-len(label))}{value}")
    
    # GitHub Stats section
    lines.append("")
    lines.append(f"{' ' * max_ascii_width}  — GitHub Stats—{separator[:66]}")
    
    stats_lines = [
        (f"Repos:", f"{stats['repos']} {{Contributed: {stats['contributed_repos']}}} | Stars: {stats['stars']}"),
        (f"Commits:", f"~{stats['repos'] * 20} (estimated) | Followers: {stats['followers']}"),
        (f"Forks:", f"{stats['forks']} | Following: {stats['following']}"),
    ]
    
    for label, value in stats_lines:
        lines.append(f"{' ' * max_ascii_width}  .{label}{'.' * (25-len(label))}{value}")
    
    # Footer
    lines.append("")
    lines.append(f"{' ' * max_ascii_width}  Last updated: {stats['updated']}")
    
    # Wrap in code block for monospace rendering
    readme = "```\n" + "\n".join(lines) + "\n```"
    
    # Add badges and additional info below
    readme += f"""

---

<div align="center">

### 🔗 Quick Links

[![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=for-the-badge&logo=google-chrome&logoColor=white)](https://alaeddinedaly.github.io/portfolio)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/yourprofile)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:your.email@example.com)

</div>

---

<details>
<summary>📊 Detailed GitHub Statistics</summary>

<br>

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username={stats['login']}&show_icons=true&theme=radical&hide_border=true" alt="GitHub Stats"/>
</p>

<p align="center">
  <img src="https://github-readme-streak-stats.herokuapp.com/?user={stats['login']}&theme=radical&hide_border=true" alt="GitHub Streak"/>
</p>

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username={stats['login']}&layout=compact&theme=radical&hide_border=true" alt="Top Languages"/>
</p>

</details>

---

<div align="center">
  <sub>⚡ This profile updates automatically every day via GitHub Actions</sub>
</div>
"""
    
    return readme

def main():
    """Main execution function"""
    print("🚀 Fetching GitHub statistics...")
    stats = fetch_github_stats()
    
    print(f"✅ Stats fetched for {stats['name']}")
    print(f"   Repos: {stats['repos']} | Stars: {stats['stars']} | Followers: {stats['followers']}")
    
    print("\n🎨 Converting avatar to ASCII art...")
    ascii_art = download_and_convert_avatar(stats['avatar_url'])
    
    print("📝 Generating README...")
    readme = create_readme(stats, ascii_art)
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)
    
    print("✅ README.md created successfully!")
    print("\n💡 Don't forget to update:")
    print("   - Email addresses")
    print("   - Social media links")
    print("   - IDE information")
    print("   - Languages and frameworks")

if __name__ == "__main__":
    main()
