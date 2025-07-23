# 🤖 GitHub Profile Automation Setup

## 📋 **Ce qu'on va automatiser :**

### 1. 🏷️ **Catégorisation automatique des projets**
### 2. 📊 **Widgets personnalisés**  
### 3. ⏱️ **Intégration Wakatime**
### 4. 🏆 **Badges dynamiques**
### 5. 🔄 **Mise à jour automatique du README**

---

## 🛠️ **Étape 1 : Configuration Wakatime**

### Installation :
1. **Crée un compte** sur [wakatime.com](https://wakatime.com)
2. **Installe l'extension** Wakatime dans VS Code
3. **Récupère ton API key** dans Settings > API Key
4. **Ajoute dans GitHub Secrets** : `WAKATIME_API_KEY`

---

## 🔧 **Étape 2 : GitHub Actions**

### Créer le dossier : `.github/workflows/`

---

## 🏷️ **Étape 3 : Topics pour catégorisation**

### Ajoute ces topics à tes repositories :

**Projets EFREI :**
- `efrei-project`
- `school-assignment`
- `education`

**Projets Personnels :**
- `personal-project`
- `portfolio`
- `creative`

**Game Development :**
- `game-development`
- `godot`
- `phaser`
- `unity`

**Professionnels :**
- `professional`
- `client-work`
- `freelance`

---

## 📊 **Étape 4 : Configuration des secrets GitHub**

### Dans ton repository `Farid-Efrei`, ajoute ces secrets :

1. `WAKATIME_API_KEY` - Ton API key Wakatime
2. `GH_TOKEN` - Token GitHub avec permissions repos
3. `EMAIL` - Ton email pour les commits auto

---

## 🎯 **Étape 5 : Script de catégorisation**

Le script va :
- Scanner tous tes repositories
- Les classer par topics
- Générer automatiquement les sections
- Mettre à jour le README

---

## 🚀 **Résultat final :**

- ✅ **README mis à jour** toutes les 6 heures
- ✅ **Stats Wakatime** en temps réel  
- ✅ **Projets catégorisés** automatiquement
- ✅ **Badges dynamiques** pour chaque repo
- ✅ **Progression tracking** par catégorie
