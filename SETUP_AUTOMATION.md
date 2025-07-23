# 🤖 Configuration de l'Automatisation du Profil

## 🔑 **Secrets à configurer dans GitHub**

Allez dans **Settings** → **Secrets and variables** → **Actions** de votre repository et ajoutez :

### 1. `GH_TOKEN`
- Valeur : Votre Personal Access Token GitHub
- Comment l'obtenir :
  1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
  2. Generate new token (classic)
  3. Sélectionnez : `repo`, `read:user`, `user:email`
  4. Copiez le token généré

### 2. `WAKATIME_API_KEY` (Optionnel)
- Valeur : Votre clé API WakaTime
- Comment l'obtenir :
  1. Inscrivez-vous sur [wakatime.com](https://wakatime.com)
  2. Installez l'extension WakaTime dans VS Code
  3. Allez dans Settings → API Key
  4. Copiez votre clé

### 3. `EMAIL`
- Valeur : Votre email GitHub
- Exemple : `farytale54@gmail.com`

## 🏷️ **Étiquetage de vos repositories**

Pour que le script catégorise correctement vos projets, ajoutez des **topics** :

### Topics suggérés :
- **EFREI :** `efrei-project`, `school-assignment`, `education`
- **Jeux :** `game-development`, `godot`, `phaser`, `unity`
- **Personnel :** `personal-project`, `portfolio`, `creative`
- **Pro :** `professional`, `client-work`, `freelance`

### Comment ajouter des topics :
1. Allez sur votre repository
2. Cliquez sur l'icône ⚙️ à côté de "About"
3. Ajoutez les topics appropriés
4. Sauvegardez

## 🚀 **Test manuel**

Pour tester le script localement :

```bash
# Installer les dépendances
pip install requests python-dateutil

# Définir les variables d'environnement
set GITHUB_TOKEN=votre_token_ici
set WAKATIME_API_KEY=votre_cle_wakatime_ici

# Exécuter le script
python scripts/update_readme.py
```

## ⚡ **Déclenchement manuel**

Pour forcer une mise à jour :
1. Allez dans **Actions** de votre repository
2. Cliquez sur "🤖 Update Profile README"
3. Cliquez sur "Run workflow"

## 🎯 **Résultat attendu**

Le script va :
- ✅ Compter automatiquement vos projets par catégorie
- ✅ Afficher vos stats de code WakaTime
- ✅ Créer des sections organisées
- ✅ Mettre à jour le badge de nombre total de projets
- ✅ Conserver votre snake animation et le reste de votre contenu
