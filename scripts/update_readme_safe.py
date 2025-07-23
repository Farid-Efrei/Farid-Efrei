#!/usr/bin/env python3
"""
Script d'automatisation sécurisé pour le README de profil GitHub
Ce script ajoute/met à jour des sections spécifiques sans écraser le contenu existant.
Utilise des marqueurs HTML pour identifier les zones à mettre à jour.
"""

import os
import requests
import json
from datetime import datetime
from typing import List, Dict, Any

# Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
USERNAME = 'Farid-Efrei'
README_PATH = 'README.md'

def get_github_repos() -> List[Dict[str, Any]]:
    """Récupère les repositories depuis l'API GitHub."""
    try:
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        url = f'https://api.github.com/users/{USERNAME}/repos'
        response = requests.get(url, headers=headers, params={'per_page': 100})
        response.raise_for_status()
        
        return response.json()
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des repos: {e}")
        return []

def categorize_projects(repos: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Catégorise les projets par type."""
    categories = {
        'game': [],
        'web': [],
        'mobile': [],
        'data': [],
        'ai': [],
        'other': []
    }
    
    # Mots-clés pour la catégorisation
    keywords = {
        'game': ['game', 'jeu', 'godot', 'phaser', 'unity', 'platformer', 'flappy'],
        'web': ['web', 'react', 'vue', 'angular', 'html', 'css', 'javascript', 'node'],
        'mobile': ['mobile', 'ionic', 'react-native', 'flutter', 'android', 'ios'],
        'data': ['data', 'excel', 'csv', 'pandas', 'numpy', 'croisement'],
        'ai': ['ai', 'ml', 'machine-learning', 'tensorflow', 'pytorch', 'neural']
    }
    
    for repo in repos:
        if repo['private'] or repo['fork']:
            continue
            
        name = repo['name'].lower()
        description = (repo['description'] or '').lower()
        topics = [topic.lower() for topic in repo.get('topics', [])]
        
        categorized = False
        for category, words in keywords.items():
            if any(word in name or word in description or word in topics for word in words):
                categories[category].append(repo)
                categorized = True
                break
        
        if not categorized:
            categories['other'].append(repo)
    
    return categories

def generate_auto_sections(categories: Dict[str, List[Dict[str, Any]]]) -> str:
    """Génère les sections automatisées."""
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    auto_content = f"""<!-- AUTO_UPDATE_START -->
## 🤖 **Auto-Update Status**

✅ **Automatisation active !**  
📅 **Dernière mise à jour:** {timestamp}  
🔧 **Mode:** Production - Mise à jour sécurisée

---

## 📂 **Projets par Catégorie** *(Auto-généré)*

<div align="center">

| 🎮 **Jeux** | 🌐 **Web** | 📱 **Mobile** | 📊 **Data** | 🤖 **AI** | 🔧 **Autres** |
|:---:|:---:|:---:|:---:|:---:|:---:|
| {len(categories['game'])} projets | {len(categories['web'])} projets | {len(categories['mobile'])} projets | {len(categories['data'])} projets | {len(categories['ai'])} projets | {len(categories['other'])} projets |

</div>

### 🎮 **Développement de Jeux**
"""
    
    # Ajouter les projets de jeux
    if categories['game']:
        for repo in categories['game'][:3]:  # Top 3
            auto_content += f"""
- **[{repo['name']}]({repo['html_url']})** - {repo['description'] or 'Projet de jeu'}
  - ⭐ {repo['stargazers_count']} stars | 🍴 {repo['forks_count']} forks
  - 📅 Mis à jour: {repo['updated_at'][:10]}"""
    else:
        auto_content += "\n- *Aucun projet de jeu détecté pour le moment*"
    
    auto_content += "\n\n### 📊 **Projets Data & Python**"
    
    # Ajouter les projets data
    if categories['data']:
        for repo in categories['data'][:3]:  # Top 3
            auto_content += f"""
- **[{repo['name']}]({repo['html_url']})** - {repo['description'] or 'Projet data'}
  - ⭐ {repo['stargazers_count']} stars | 🍴 {repo['forks_count']} forks
  - 📅 Mis à jour: {repo['updated_at'][:10]}"""
    else:
        auto_content += "\n- *Aucun projet data détecté pour le moment*"
    
    # Statistiques rapides
    total_repos = sum(len(repos) for repos in categories.values())
    total_stars = sum(sum(repo['stargazers_count'] for repo in repos) for repos in categories.values())
    
    auto_content += f"""

---

### 📈 **Statistiques Rapides** *(Auto-généré)*

<div align="center">

| 📦 **Repositories** | ⭐ **Total Stars** | 🔥 **Catégories** | 🚀 **Projets Actifs** |
|:---:|:---:|:---:|:---:|
| {total_repos} | {total_stars} | 6 | {len([r for repos in categories.values() for r in repos if (datetime.now() - datetime.fromisoformat(r['updated_at'].replace('Z', '+00:00'))).days < 30])} |

</div>

*Dernière synchronisation: {timestamp}*
<!-- AUTO_UPDATE_END -->"""
    
    return auto_content

def update_readme_safely(auto_content: str):
    """Met à jour le README en préservant le contenu manuel."""
    try:
        # Lire le README actuel
        with open(README_PATH, 'r', encoding='utf-8') as f:
            current_content = f.read()
        
        # Trouver les marqueurs de début et fin
        start_marker = '<!-- AUTO_UPDATE_START -->'
        end_marker = '<!-- AUTO_UPDATE_END -->'
        
        start_index = current_content.find(start_marker)
        end_index = current_content.find(end_marker)
        
        if start_index != -1 and end_index != -1:
            # Remplacer seulement la section automatisée
            before_auto = current_content[:start_index]
            after_auto = current_content[end_index + len(end_marker):]
            new_content = before_auto + auto_content + after_auto
        else:
            # Ajouter la section automatisée à la fin
            new_content = current_content + '\n\n' + auto_content
        
        # Sauvegarder le nouveau contenu
        with open(README_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ README mis à jour avec succès (mode sécurisé)")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour du README: {e}")
        return False

def main():
    """Fonction principale."""
    print("🚀 Démarrage de l'automatisation sécurisée du README...")
    
    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN non trouvé dans les variables d'environnement")
        return
    
    # Récupérer les repositories
    print("📡 Récupération des repositories...")
    repos = get_github_repos()
    
    if not repos:
        print("❌ Aucun repository trouvé")
        return
    
    print(f"✅ {len(repos)} repositories trouvés")
    
    # Catégoriser les projets
    print("🏷️ Catégorisation des projets...")
    categories = categorize_projects(repos)
    
    # Générer le contenu automatisé
    print("🔄 Génération du contenu automatisé...")
    auto_content = generate_auto_sections(categories)
    
    # Mettre à jour le README de manière sécurisée
    print("💾 Mise à jour sécurisée du README...")
    if update_readme_safely(auto_content):
        print("🎉 Automatisation terminée avec succès !")
    else:
        print("❌ Échec de l'automatisation")

if __name__ == '__main__':
    main()
