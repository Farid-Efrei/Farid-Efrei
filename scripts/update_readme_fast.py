#!/usr/bin/env python3
"""
🚀 Fairytale-Dev Profile Fast Updater - Version Debug
Version allégée pour diagnostic rapide
"""

import os
import requests
from datetime import datetime

def fast_update():
    """Version ultra-rapide pour debug"""
    print("🚀 Début du script rapide...")
    
    github_token = os.getenv('GITHUB_TOKEN')
    username = 'Farid-Efrei'
    
    if not github_token:
        print("❌ GITHUB_TOKEN manquant")
        return
        
    print(f"✅ Token trouvé: {github_token[:8]}...")
    
    # Test API GitHub simple
    try:
        headers = {'Authorization': f'token {github_token}'}
        print("📡 Test API GitHub...")
        
        # Requête simple pour tester
        response = requests.get(
            f'https://api.github.com/users/{username}', 
            headers=headers,
            timeout=30  # 30 secondes max
        )
        
        print(f"🌐 Status: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ API OK - User: {user_data.get('name', 'N/A')}")
            print(f"📊 Public repos: {user_data.get('public_repos', 0)}")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return
            
    except Exception as e:
        print(f"💥 Erreur API: {e}")
        return
    
    # Test récupération repos (limité)
    try:
        print("📋 Test récupération repos...")
        repos_url = f'https://api.github.com/users/{username}/repos?per_page=5'  # Seulement 5 pour tester
        
        response = requests.get(repos_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            repos = response.json()
            print(f"✅ Repos récupérés: {len(repos)}")
            for repo in repos[:3]:  # Afficher les 3 premiers
                print(f"  - {repo['name']} ({repo.get('language', 'N/A')})")
        else:
            print(f"❌ Erreur repos: {response.status_code}")
            
    except Exception as e:
        print(f"💥 Erreur repos: {e}")
        return
    
    # Génération README minimal
    print("📝 Génération README minimal...")
    
    readme_content = f"""# 🌟 Welcome to Fairytale-Dev's Universe! 🌟

<div align="center">
<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=36+&duration=3500&pause=900&color=6366F1&background=00000000&center=true&vCenter=true&multiline=true&width=950&height=360&lines=Hi%2C+I'm+Fary+%F0%9F%91%8B%E2%9C%A8;Fairytale-Dev+%F0%9F%A7%99%E2%80%8D%E2%99%82%EF%B8%8F%F0%9F%92%AB;Full-Stack+Developer+%F0%9F%9A%80+Little+Game+Dev+%F0%9F%8E%AE;Student+%26+Dreamer+%F0%9F%8C%9F%F0%9F%93%9A;Learning+from+Everyone+%26+Everything+%F0%9F%A7%A0%E2%9C%A8;AI+Enthusiast+%F0%9F%A4%96+Techno+Explorer+%F0%9F%94%A5%F0%9F%92%BB%F0%9F%8E%B2" alt="Typing SVG" />
</div>

<br> <br>

<div align="center">
  <img src="https://komarev.com/ghpvc/?username=Farid-Efrei&color=blueviolet&style=flat-square&label=Profile+Views" alt="Profile Views"/>
  <img src="https://img.shields.io/github/followers/Farid-Efrei?style=flat-square&color=blue&label=Followers" alt="Followers"/>
  <img src="https://img.shields.io/badge/Status-Coding%20%26%20Learning-brightgreen?style=flat-square" alt="Status"/>
</div>

<br>

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github.com/Farid-Efrei/Farid-Efrei/blob/output/github-contribution-grid-snake-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://github.com/Farid-Efrei/Farid-Efrei/blob/output/github-contribution-grid-snake.svg">
    <img alt="GitHub contribution snake animation" src="https://github.com/Farid-Efrei/Farid-Efrei/blob/output/github-contribution-grid-snake.svg">
  </picture>
</div>

---

## 🤖 **Auto-Update Status**

✅ **Script rapide exécuté avec succès !**  
📅 **Dernière mise à jour:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC  
🔧 **Mode:** Debug/Fast version

---

## 🧙‍♂️ **About Me - The Human Behind the Code**

*Contenu complet bientôt restauré...*

---

**✨ Made with ❤️ and lots of ☕ by Fairytale-Dev**

*"In a world full of bugs, be the feature that makes everything better."* 🐛➡️🦋

<!-- Fast update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC -->
"""

    try:
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("✅ README mis à jour avec succès!")
        
        # Vérification que le fichier a bien été écrit
        if os.path.exists('README.md'):
            file_size = os.path.getsize('README.md')
            print(f"📄 Fichier README.md: {file_size} bytes")
            
            # Lire les premières lignes pour confirmer
            with open('README.md', 'r', encoding='utf-8') as f:
                first_lines = f.read(200)
            print(f"📋 Début du fichier: {first_lines[:100]}...")
        else:
            print("❌ Fichier README.md non trouvé après écriture!")
            
        print("🎯 Script terminé en mode rapide")
        
    except Exception as e:
        print(f"💥 Erreur écriture: {e}")
        print(f"📁 Dossier courant: {os.getcwd()}")
        print(f"📂 Contenu du dossier: {os.listdir('.')}")

if __name__ == "__main__":
    fast_update()
