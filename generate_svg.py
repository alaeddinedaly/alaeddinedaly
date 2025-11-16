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

# ============================================================
# 🎨 CUSTOMIZE YOUR PROFILE HERE
# ============================================================
# Update these with YOUR information:

PERSONAL_INFO = {
    'location': 'Tunis, Tunisia 🇹🇳',
    'status': '🚀 Full-Stack Developer & AI Enthusiast',
    'company': 'Independent Developer',  # Or your company name
    'shell': 'Bash, Zsh, PowerShell',
    'ide': 'VSCode, IntelliJ IDEA, PyCharm',
    
    # Update with YOUR tech stack:
    'frontend': 'React ⚛️, TypeScript, Tailwind CSS 🎨, Next.js',
    'backend': 'Spring Boot ☕, Node.js 🟢, Express, Python 🐍',
    'database': 'PostgreSQL 🐘, MongoDB 🍃, MySQL, Redis 🔴',
    'languages_real': 'Arabic 🇹🇳, French 🇫🇷, English 🇺🇸',
    
    # Your focus areas:
    'focus_ai': 'Machine Learning, NLP, Generative AI, Computer Vision',
    'focus_security': 'JWT, OAuth, Authentication, Secure APIs',
    'focus_cloud': 'Docker 🐳, CI/CD, AWS, Linux 🐧',
    'currently': 'Building AI-powered applications & exploring Web3 🌐',
    
    # Your contact info:
    'email_personal': 'dalyalaeddine@gmail.com',
    'email_work': '',  # Leave empty if none
    'linkedin': 'linkedin.com/in/daly-ala-eddine',
    'portfolio': 'aladin-daly-dev.vercel.app',
}

# ============================================================

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
        "::::::::::::::----=++==-=-::------------",
        "::::::::::=+*%@@@#@@@@@@#%=-------------",
        "::::::::-+%#@@@@@@@@@@@@@@@#+----------=",
        ".::::::=%##@@@@@@@@@@@@@@@@@@*--------==",
        "...:::-%#@@@@##%%###@@@@@@@@@@%=----====",
        "....::+%@%+=-----===++*%%#@@@@@@+--===- ",
        "....:=#@=.::-----=====++*%#@@@@@@===-.  ",
        "....=#@+.::--------=====++*%@@@@@#=:    ",
        "....*@%:.:::::-=======++++++**#@@@.    :",
        "...:%%+...:-*#@%+===*#@@@@#%*+%@@@   .--",
        ":.::+%*:.=#@@@#%*=-+%%##%%###**@@@   .::",
        ":::.=%%:-%*++*%%*-.-*#@###%%%*+%@@.     ",
        ":-:.-%%--==*#@@#=.:-+*##@@@@#*+*@#-::::.",
        "::...=#-:+*###%+:.:-=++++++===++#*+=----",
        ".     *-...:---: .:-==++=----===*+*+====",
        "     +=.  ..:-=:=%*+%#*+*++==++=+*++----",
        "     *=: :--====%@%%%##%*++***++++++----",
        "     -=-:====-==++***%%%%%%%*++=+=+=-=--",
        "      -::-===*%%%%%%%%##%%%*++==+=---:--",
        "       .::--=**+++*****+++++++++=-===**+",
        " ....   .:---=---=****+++++++++*::-=++++",
        ".....    .==----=+++++++++++***=  .-----",
        "..:-:.    :==--==--++=++++*****..  .---=",
        ".:-====:...-++====++*+******%%+..   .-==",
        ":-====+=:::.=**%%%%%%%%%%%%%%*=:..   :==",
        "--==--==-::.:-=+**%%%%%%*%**+++-:..  .-=",
        ":::--==:. :::-----=*******+++=+=:::. .:=",
    ]

def create_readme(stats: Dict, ascii_art: List[str]) -> str:
    """Generate the complete README with ASCII art and stats"""
    
    # Pad ASCII art lines to consistent width
    max_ascii_width = max(len(line) for line in ascii_art) if ascii_art else 26
    padded_ascii = [line.ljust(max_ascii_width) for line in ascii_art]
    
    # Create the stats sections
    lines = []
    
    # Header line - MORE COLORFUL!
    header = f"👨‍💻 {stats['login']}@github"
    separator = "━" * 80
    lines.append(f"{' ' * max_ascii_width}  {header} {separator[:75-len(header)]}")
    
    # Info sections with ASCII art on the left - MORE COLORFUL!
    info_lines = [
        ("🌍 Location:", PERSONAL_INFO['location']),
        ("⏰ Uptime:", stats['account_age']),
        ("💼 Status:", PERSONAL_INFO['status']),
        ("🏢 Company:", PERSONAL_INFO['company']),
        ("🐚 Shell:", PERSONAL_INFO['shell']),
        ("⚡ IDE:", PERSONAL_INFO['ide']),
        ("", ""),
        ("💻 Languages:", stats['languages']),
        ("🎨 Frontend:", PERSONAL_INFO['frontend']),
        ("🔧 Backend:", PERSONAL_INFO['backend']),
        ("🗄️  Database:", PERSONAL_INFO['database']),
        ("🌐 Speaking:", PERSONAL_INFO['languages_real']),
        ("", ""),
        ("🤖 AI/ML:", PERSONAL_INFO['focus_ai']),
        ("🔐 Security:", PERSONAL_INFO['focus_security']),
        ("☁️  Cloud:", PERSONAL_INFO['focus_cloud']),
        ("🎯 Currently:", PERSONAL_INFO['currently']),
    ]
    
    # Combine ASCII art with info
    for i, (label, value) in enumerate(info_lines):
        ascii_line = padded_ascii[i] if i < len(padded_ascii) else ' ' * max_ascii_width
        if label:
            dots = '.' * max(1, 25 - len(label))
            lines.append(f"{ascii_line}  .{label}{dots}{value}")
        else:
            lines.append(f"{ascii_line}  .")
    
    # Fill remaining ASCII art lines WITHOUT the dot
    for i in range(len(info_lines), len(padded_ascii)):
        lines.append(padded_ascii[i])
    
    # Contact section - MORE COLORFUL!
    lines.append("")
    lines.append(f"{' ' * max_ascii_width}  ━━ 📫 Contact ━━{separator[:65]}")
    
    contact_lines = [
        ("📧 Email:", PERSONAL_INFO['email_personal']),
    ]
    
    if PERSONAL_INFO['email_work']:
        contact_lines.append(("💼 Work:", PERSONAL_INFO['email_work']))
    
    contact_lines.extend([
        ("💼 LinkedIn:", PERSONAL_INFO['linkedin']),
        ("🐙 GitHub:", f"github.com/{stats['login']}"),
        ("🌐 Portfolio:", PERSONAL_INFO['portfolio']),
        ("🐦 Twitter:", PERSONAL_INFO['twitter']),
    ])
    
    for label, value in contact_lines:
        dots = '.' * max(1, 25 - len(label))
        lines.append(f"{' ' * max_ascii_width}  .{label}{dots}{value}")
    
    # GitHub Stats section - MORE COLORFUL!
    lines.append("")
    lines.append(f"{' ' * max_ascii_width}  ━━ 📊 GitHub Stats ━━{separator[:60]}")
    
    # Format numbers with commas
    repos_str = f"📦 {stats['repos']}"
    contrib_str = f"{{✨ Contributed: {stats['contributed_repos']}}}"
    stars_str = f"⭐ Stars: {stats['stars']}"
    
    stats_lines = [
        (f"📚 Repositories:", f"{repos_str} {contrib_str} | {stars_str}"),
        (f"💾 Commits:", f"~{stats['repos'] * 25} (estimated) | 👥 Followers: {stats['followers']}"),
        (f"🔱 Forks:", f"{stats['forks']} | 🔗 Following: {stats['following']}"),
        (f"🔥 Streak:", "Building daily! 💪"),
    ]
    
    for label, value in stats_lines:
        dots = '.' * max(1, 25 - len(label))
        lines.append(f"{' ' * max_ascii_width}  .{label}{dots}{value}")
    
    # Footer - MORE COLORFUL!
    lines.append("")
    lines.append(f"{' ' * max_ascii_width}  🕐 Last updated: {stats['updated']}")
    lines.append(f"{' ' * max_ascii_width}  🤖 Generated with ❤️  by GitHub Actions")
    
    # Wrap in code block for monospace rendering
    readme = "```\n" + "\n".join(lines) + "\n```"
    
    # Add colorful badges and sections OUTSIDE the code block
    readme += f"""

---

<div align="center">

## 🚀 Tech Stack & Tools

### Languages
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)
![Kotlin](https://img.shields.io/badge/Kotlin-7F52FF?style=for-the-badge&logo=kotlin&logoColor=white)

### Frontend
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

### Backend
![Spring](https://img.shields.io/badge/Spring-6DB33F?style=for-the-badge&logo=spring&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![Express](https://img.shields.io/badge/Express.js-000000?style=for-the-badge&logo=express&logoColor=white)

### Database & Tools
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

</div>

---

<div align="center">

### 🔗 Connect With Me

[![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=for-the-badge&logo=google-chrome&logoColor=white)]({PERSONAL_INFO['portfolio']})
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://{PERSONAL_INFO['linkedin']})
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:{PERSONAL_INFO['email_personal']})
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/{stats['login']})
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/{PERSONAL_INFO['twitter'].replace('@', '')})

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
