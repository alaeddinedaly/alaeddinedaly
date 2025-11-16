#!/usr/bin/env python3
"""
ASCII Art GitHub Profile Generator
Creates a terminal-style profile with ASCII art and live stats
"""

import requests
import os
from datetime import datetime
from typing import Dict, List

# Configuration
GITHUB_USERNAME = "alaeddinedaly"
GITHUB_TOKEN = os.getenv('GH_TOKEN', '')

def fetch_github_stats() -> Dict:
    """Fetch comprehensive GitHub statistics"""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}
    
    print("📡 Fetching user data...")
    # User data
    user_url = f"https://api.github.com/users/{GITHUB_USERNAME}"
    user_response = requests.get(user_url, headers=headers)
    user_response.raise_for_status()
    user_data = user_response.json()
    
    print("📡 Fetching repositories...")
    # Repos
    repos_url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100"
    repos_response = requests.get(repos_url, headers=headers)
    repos_response.raise_for_status()
    repos = repos_response.json()
    
    # Calculate stats
    total_stars = sum(r.get('stargazers_count', 0) for r in repos if isinstance(r, dict))
    total_forks = sum(r.get('forks_count', 0) for r in repos if isinstance(r, dict))
    
    print("📡 Analyzing languages...")
    # Languages
    languages = {}
    for repo in repos[:20]:  # Limit to prevent rate limiting
        if isinstance(repo, dict) and not repo.get('fork', False):
            lang = repo.get('language')
            if lang:
                languages[lang] = languages.get(lang, 0) + 1
    
    top_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:4]
    lang_names = [lang for lang, _ in top_langs]
    
    # Count contributed repos
    contributed_repos = sum(1 for repo in repos if isinstance(repo, dict) and not repo.get('fork', False))
    
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
        'location': user_data.get('location', 'Tunisia'),
        'company': user_data.get('company', ''),
        'repos': user_data.get('public_repos', 0),
        'stars': total_stars,
        'forks': total_forks,
        'followers': user_data.get('followers', 0),
        'following': user_data.get('following', 0),
        'contributed_repos': contributed_repos,
        'languages': ', '.join(lang_names) if lang_names else 'Python, TypeScript, Java',
        'account_age': f"{years} years, {months} months, {days} days",
        'updated': datetime.now().strftime('%B %d, %Y at %H:%M UTC')
    }

def get_custom_avatar_art() -> List[str]:
    """Return custom ASCII art - you can customize this!"""
    # This is a generic developer avatar - customize it to look like you!
    return [
        "        @@@@@@@@@@        ",
        "      @@@@@@@@@@@@@@      ",
        "    @@@@@@@@@@@@@@@@@@    ",
        "   @@@@@@@@@@@@@@@@@@@@   ",
        "  @@@@@@@@  @@@@@@@@@@@@  ",
        "  @@@@@@@@  @@@@@@@@@@@@  ",
        " @@@@@@@@@@@@@@@@@@@@@@@@ ",
        " @@@@@@@@@@@@@@@@@@@@@@@@ ",
        " @@@@@@@@@@@@@@@@@@@@@@@@ ",
        "  @@@@@@@@@@@@@@@@@@@@@@  ",
        "  @@@@@@@@@@@@@@@@@@@@@@  ",
        "   @@@@@@@@@@@@@@@@@@@@   ",
        "    @@@@@@@@@@@@@@@@@@    ",
        "      @@@@@@@@@@@@@@      ",
        "        @@@@@@@@@@        ",
    ]

def create_readme(stats: Dict, ascii_art: List[str]) -> str:
    """Generate the complete README with ASCII art and stats"""
    
    # Pad ASCII art lines to consistent width
    max_ascii_width = max(len(line) for line in ascii_art) if ascii_art else 26
    padded_ascii = [line.ljust(max_ascii_width) for line in ascii_art]
    
    # Create the stats sections
    lines = []
    
    # Header line
    header = f"{stats['login']}@github"
    separator = "—" * 80
    lines.append(f"{' ' * max_ascii_width}  {header}—{separator[:77-len(header)]}")
    
    # Info sections with ASCII art on the left
    info_lines = [
        ("OS:", f"{stats['location']} | Full-Stack Developer"),
        ("Uptime:", stats['account_age']),
        ("Host:", stats['company'] if stats['company'] else "Independent Developer"),
        ("Shell:", "Bash, Zsh, PowerShell"),
        ("IDE:", "VSCode, IntelliJ IDEA, PyCharm"),
        ("", ""),
        ("Languages.Programming:", stats['languages']),
        ("Languages.Framework:", "React, Spring Boot, Node.js, Express"),
        ("Languages.Database:", "PostgreSQL, MongoDB, Redis"),
        ("Languages.Real:", "Arabic, French, English"),
        ("", ""),
        ("Focus.AI:", "Machine Learning, NLP, Computer Vision"),
        ("Focus.Backend:", "REST APIs, Microservices, Authentication"),
        ("Focus.Frontend:", "React, TypeScript, Modern CSS"),
        ("Focus.Tools:", "Git, Docker, CI/CD, Linux"),
    ]
    
    # Combine ASCII art with info
    for i, (label, value) in enumerate(info_lines):
        ascii_line = padded_ascii[i] if i < len(padded_ascii) else ' ' * max_ascii_width
        if label:
            dots = '.' * max(1, 25 - len(label))
            lines.append(f"{ascii_line}  .{label}{dots}{value}")
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
        ("Email.Work:", "work@company.com (optional)"),
        ("LinkedIn:", "linkedin.com/in/yourprofile"),
        ("GitHub:", f"github.com/{stats['login']}"),
        ("Portfolio:", "yourportfolio.com"),
        ("Twitter:", "@yourhandle"),
    ]
    
    for label, value in contact_lines:
        dots = '.' * max(1, 25 - len(label))
        lines.append(f"{' ' * max_ascii_width}  .{label}{dots}{value}")
    
    # GitHub Stats section
    lines.append("")
    lines.append(f"{' ' * max_ascii_width}  — GitHub Stats—{separator[:66]}")
    
    # Format numbers with commas
    repos_str = f"{stats['repos']}"
    contrib_str = f"{{Contributed: {stats['contributed_repos']}}}"
    stars_str = f"Stars: {stats['stars']}"
    
    stats_lines = [
        (f"Repos:", f"{repos_str} {contrib_str} | {stars_str}"),
        (f"Commits:", f"~{stats['repos'] * 25} (estimated) | Followers: {stats['followers']}"),
        (f"Forks:", f"{stats['forks']} | Following: {stats['following']}"),
    ]
    
    for label, value in stats_lines:
        dots = '.' * max(1, 25 - len(label))
        lines.append(f"{' ' * max_ascii_width}  .{label}{dots}{value}")
    
    # Footer
    lines.append("")
    lines.append(f"{' ' * max_ascii_width}  Last updated: {stats['updated']}")
    lines.append(f"{' ' * max_ascii_width}  Generated with ❤️ by GitHub Actions")
    
    # Wrap in code block for monospace rendering
    readme = "```\n" + "\n".join(lines) + "\n```"
    
    # Add badges and additional info below
    readme += f"""

---

<div align="center">

### 🔗 Connect With Me

[![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=for-the-badge&logo=google-chrome&logoColor=white)](https://alaeddinedaly.github.io/portfolio)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/yourprofile)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:your.email@example.com)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/{stats['login']})

</div>

---

<details>
<summary>📊 Detailed GitHub Statistics</summary>

<br>

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username={stats['login']}&show_icons=true&theme=radical&hide_border=true&bg_color=0D1117" alt="GitHub Stats"/>
</p>

<p align="center">
  <img src="https://github-readme-streak-stats.herokuapp.com/?user={stats['login']}&theme=radical&hide_border=true&background=0D1117" alt="GitHub Streak"/>
</p>

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username={stats['login']}&layout=compact&theme=radical&hide_border=true&bg_color=0D1117" alt="Top Languages"/>
</p>

</details>

---

<div align="center">
  <sub>⚡ This profile auto-updates daily via GitHub Actions</sub>
</div>
"""
    
    return readme

def main():
    """Main execution function"""
    try:
        print("=" * 60)
        print("🚀 GitHub Profile ASCII Generator")
        print("=" * 60)
        
        stats = fetch_github_stats()
        
        print(f"\n✅ Stats fetched!")
        print(f"   👤 {stats['name']} (@{stats['login']})")
        print(f"   📦 Repos: {stats['repos']}")
        print(f"   ⭐ Stars: {stats['stars']}")
        print(f"   👥 Followers: {stats['followers']}")
        
        print("\n🎨 Using custom ASCII art...")
        ascii_art = get_custom_avatar_art()
        
        print("📝 Generating README...")
        readme = create_readme(stats, ascii_art)
        
        print("💾 Writing README.md...")
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme)
        
        print("\n" + "=" * 60)
        print("✅ SUCCESS! README.md created")
        print("=" * 60)
        
        print("\n💡 Next steps:")
        print("   1. Update contact info in the script")
        print("   2. Customize the ASCII art in get_custom_avatar_art()")
        print("   3. Adjust info_lines with your real data")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()
