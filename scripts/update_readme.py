#!/usr/bin/env python3
"""
🤖 Fairytale-Dev Profile Auto-Updater
Génère automatiquement le README avec catégorisation et stats
"""

import os
import requests
import json
from datetime import datetime
from typing import Dict, List, Any

class FairyTaleProfileUpdater:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.wakatime_key = os.getenv('WAKATIME_API_KEY')
        self.username = 'Farid-Efrei'
        
        # Catégories de projets
        self.categories = {
            'efrei': {
                'name': '🎓 EFREI Projects',
                'topics': ['efrei-project', 'school-assignment', 'education'],
                'emoji': '🎓',
                'color': 'blue'
            },
            'personal': {
                'name': '🚀 Personal Projects', 
                'topics': ['personal-project', 'portfolio', 'creative'],
                'emoji': '🚀',
                'color': 'green'
            },
            'games': {
                'name': '🎮 Game Development',
                'topics': ['game-development', 'godot', 'phaser', 'unity'],
                'emoji': '🎮', 
                'color': 'purple'
            },
            'professional': {
                'name': '🏢 Professional',
                'topics': ['professional', 'client-work', 'freelance'],
                'emoji': '🏢',
                'color': 'orange'
            }
        }
        
    def get_repositories(self) -> List[Dict]:
        """Récupère tous les repositories de l'utilisateur"""
        headers = {'Authorization': f'token {self.github_token}'}
        url = f'https://api.github.com/users/{self.username}/repos'
        
        all_repos = []
        page = 1
        
        while True:
            response = requests.get(f'{url}?page={page}&per_page=100', headers=headers)
            repos = response.json()
            
            if not repos:
                break
                
            all_repos.extend(repos)
            page += 1
            
        return all_repos
    
    def categorize_repos(self, repos: List[Dict]) -> Dict[str, List[Dict]]:
        """Catégorise les repositories selon leurs topics"""
        categorized = {cat: [] for cat in self.categories.keys()}
        uncategorized = []
        
        for repo in repos:
            if repo['fork'] or repo['archived']:
                continue
                
            topics = repo.get('topics', [])
            categorized_repo = False
            
            for cat_key, cat_info in self.categories.items():
                if any(topic in topics for topic in cat_info['topics']):
                    categorized[cat_key].append({
                        'name': repo['name'],
                        'description': repo['description'] or 'No description',
                        'language': repo['language'],
                        'stars': repo['stargazers_count'],
                        'forks': repo['forks_count'],
                        'url': repo['html_url'],
                        'updated': repo['updated_at']
                    })
                    categorized_repo = True
                    break
                    
            if not categorized_repo and not repo['private']:
                uncategorized.append(repo)
                
        return categorized, uncategorized
    
    def get_wakatime_stats(self) -> str:
        """Récupère les stats Wakatime"""
        if not self.wakatime_key:
            return "<!-- Wakatime stats unavailable -->"
            
        try:
            headers = {'Authorization': f'Bearer {self.wakatime_key}'}
            url = 'https://wakatime.com/api/v1/users/current/stats/last_7_days'
            
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if 'data' in data:
                languages = data['data']['languages'][:5]  # Top 5
                total_time = data['data']['human_readable_total']
                
                wakatime_section = f"""
## ⏱️ **This Week's Coding Time**

**Total:** {total_time}

"""
                for lang in languages:
                    name = lang['name']
                    percent = lang['percent']
                    time = lang['text']
                    bar_length = int(percent / 5)  # Barre sur 20 caractères
                    bar = '█' * bar_length + '░' * (20 - bar_length)
                    wakatime_section += f"**{name}** `{time}` {bar} {percent:.1f}%\n"
                    
                return wakatime_section
                
        except Exception as e:
            print(f"Erreur Wakatime: {e}")
            
        return "<!-- Wakatime stats unavailable -->"
    
    def generate_project_section(self, categorized_repos: Dict) -> str:
        """Génère la section des projets catégorisés"""
        section = """
## 🗂️ **Project Categories**

<div align="center">

"""
        # Tableaux de stats par catégorie
        headers = []
        counts = []
        
        for cat_key, repos in categorized_repos.items():
            if repos:  # Si il y a des repos dans cette catégorie
                cat_info = self.categories[cat_key]
                headers.append(f"| {cat_info['name']} ")
                counts.append(f"| ![{cat_info['emoji']}](https://img.shields.io/badge/Projects-{len(repos)}-{cat_info['color']}?style=for-the-badge) ")
        
        headers.append("|")
        counts.append("|")
        
        section += "".join(headers) + "\n"
        section += "|:---:" * (len(headers) - 1) + "|\n"
        section += "".join(counts) + "\n\n"
        section += "</div>\n\n"
        
        # Détail de chaque catégorie
        for cat_key, repos in categorized_repos.items():
            if not repos:
                continue
                
            cat_info = self.categories[cat_key]
            section += f"### {cat_info['emoji']} **{cat_info['name']}**\n\n"
            
            # Top 3 repos de chaque catégorie
            top_repos = sorted(repos, key=lambda x: x['stars'], reverse=True)[:3]
            
            for repo in top_repos:
                section += f"""
<details>
<summary><b>{repo['name']}</b> ⭐ {repo['stars']} 🍴 {repo['forks']}</summary>

**Description:** {repo['description']}  
**Language:** `{repo['language'] or 'Mixed'}`  
**Last Update:** {repo['updated'][:10]}

[![View Repo](https://img.shields.io/badge/View-Repository-blue?style=for-the-badge&logo=github)]({repo['url']})

</details>

"""
                
        return section
    
    def generate_full_readme(self, categorized_repos: Dict) -> str:
        """Génère le README complet"""
        wakatime_stats = self.get_wakatime_stats()
        project_section = self.generate_project_section(categorized_repos)
        
        # Compter les projets totaux
        total_projects = sum(len(repos) for repos in categorized_repos.values())
        
        readme_template = f"""# 🌟 Welcome to Fairytale-Dev's Universe! 🌟

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=32&duration=3000&pause=1000&color=6366F1&background=00000000&center=true&vCenter=true&multiline=true&width=650&height=140&lines=Hi%2C+I'm+Farid+%F0%9F%91%8B;Fairytale-Dev+%E2%9C%A8;Full-Stack+Developer+%F0%9F%9A%80;Game+Developer+%F0%9F%8E%AE;Student+%26+Dreamer+%F0%9F%8C%9F" alt="Typing SVG" />
</div>

<br><br>

<div align="center">
  <img src="https://komarev.com/ghpvc/?username=Farid-Efrei&color=blueviolet&style=flat-square&label=Profile+Views" alt="Profile Views"/>
  <img src="https://img.shields.io/github/followers/Farid-Efrei?style=flat-square&color=blue&label=Followers" alt="Followers"/>
  <img src="https://img.shields.io/badge/Projects-{total_projects}-brightgreen?style=flat-square&label=Total" alt="Total Projects"/>
  <img src="https://img.shields.io/badge/Status-Coding%20%26%20Learning-brightgreen?style=flat-square" alt="Status"/>
</div>

---

## 🧙‍♂️ **About Me**

```typescript
const fairytaleDev = {{
    name: "Farid",
    aliases: ["Fairytale-Dev", "Fairytale-Efrei"],
    role: "Étudiant Développeur Passionné",
    school: "EFREI Paris",
    mindset: "Idéaliste & Créatif",
    
    passions: [
        "🎮 Game Development",
        "📱 Mobile Apps", 
        "🧠 Psychology & UX",
        "🌱 RSE & Sustainable Tech",
        "✨ Beautiful & Useful Applications"
    ],
    
    currentFocus: "Creating digital experiences that blend fun, utility & meaning",
    dream: "Building applications that make a positive impact on the world 🌍"
}};
```

---

## 🛠️ **Tech Arsenal**

<div align="center">

### 🎯 **Favorites & Mastered**
<p>
  <img src="https://skillicons.dev/icons?i=react,nodejs,typescript,tailwind,vue,ionic&theme=dark" alt="Tech Stack"/>
</p>

### 🚀 **Currently Exploring**
<p>
  <img src="https://skillicons.dev/icons?i=angular,java,godot,phaser&theme=dark" alt="Learning"/>
</p>

### 🔧 **Tools & Platforms**
<p>
  <img src="https://skillicons.dev/icons?i=git,github,vscode,figma,firebase,vercel&theme=dark" alt="Tools"/>
</p>

</div>

{wakatime_stats}

---

{project_section}

---

## 📊 **GitHub Analytics**

<div align="center">
  <img height="180em" src="https://github-readme-stats.vercel.app/api?username=Farid-Efrei&show_icons=true&theme=tokyonight&include_all_commits=true&count_private=true&hide_border=true"/>
  <img height="180em" src="https://github-readme-stats.vercel.app/api/top-langs/?username=Farid-Efrei&layout=compact&langs_count=8&theme=tokyonight&hide_border=true"/>
</div>

<div align="center">
  <img src="https://github-readme-streak-stats.herokuapp.com/?user=Farid-Efrei&theme=tokyonight&hide_border=true" alt="Streak Stats"/>
</div>

---

## 🌱 **Current Learning Journey**

<div align="center">

### 🎯 **2025 Goals**

| 🎮 **Game Dev** | 📱 **Mobile** | 🌐 **Web** | 🧠 **Soft Skills** |
|:---:|:---:|:---:|:---:|
| Advanced Godot | React Native Pro | Angular Mastery | Psychology Applied to UX |
| Unity Basics | iOS Development | Java Backend | Team Leadership |
| Game AI | Cross-Platform | Microservices | Project Management |

</div>

---

## 🌟 **Philosophy & Values**

<div align="center">

> ### *"Créer des expériences numériques qui allient plaisir, utilité et sens"*
> ### *"Building digital experiences that blend fun, utility & meaning"*

</div>

---

## 📬 **Let's Connect!**

<div align="center">

### 🤝 **Open to collaborate on:**
- 🎮 **Game Development** projects
- 📱 **Mobile Applications** with social impact
- 🌱 **Sustainable Tech** initiatives  
- 🎨 **Creative UI/UX** challenges

<p>
  <a href="mailto:farid.efrei@gmail.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/>
  </a>
  <a href="https://linkedin.com/in/farid-efrei">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
  </a>
  <a href="https://github.com/Farid-Efrei">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  </a>
</p>

</div>

---

<div align="center">

### 🎪 **Fun Facts About Me**

🎨 I believe every line of code is a brushstroke in a digital masterpiece  
🌙 Night owl developer - best ideas come after midnight  
📚 Psychology enthusiast - fascinated by human behavior  
🎮 Retro gaming lover - pixel art is my aesthetic  
☕ Coffee-driven development - powered by caffeine & creativity  
🌍 Dream to create apps that make the world a little better  

---

### 🏆 **Achievement Unlocked!**
*You've discovered the Fairytale-Dev universe! 🌟*

![Snake animation](https://github.com/Farid-Efrei/Farid-Efrei/blob/output/github-contribution-grid-snake.svg)

---

**✨ Made with ❤️ and lots of ☕ by Fairytale-Dev**

*"In a world full of bugs, be the feature that makes everything better."* 🐛➡️🦋

<!-- Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC -->

</div>"""

        return readme_template

    def run(self):
        """Exécute la mise à jour complète"""
        print("🤖 Démarrage de la mise à jour automatique...")
        
        # Récupération des repositories
        repos = self.get_repositories()
        print(f"📊 Trouvé {len(repos)} repositories")
        
        # Catégorisation
        categorized, uncategorized = self.categorize_repos(repos)
        print(f"🏷️ Catégorisé {sum(len(cat) for cat in categorized.values())} repositories")
        
        # Génération du README
        readme_content = self.generate_full_readme(categorized)
        
        # Sauvegarde
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
            
        print("✅ README mis à jour avec succès!")
        
        # Affichage des repos non catégorisés pour info
        if uncategorized:
            print(f"⚠️ {len(uncategorized)} repositories non catégorisés:")
            for repo in uncategorized[:5]:  # Afficher seulement les 5 premiers
                print(f"  - {repo['name']}")

if __name__ == "__main__":
    updater = FairyTaleProfileUpdater()
    updater.run()
