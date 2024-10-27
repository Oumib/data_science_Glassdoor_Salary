import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 

# Charger les données
df = pd.read_csv('C:/Users/PC/Documents/ds_salaryGlassdoor/salary_data_cleaned.csv')
print(df.head())  # Affiche les premières lignes du DataFrame

# Vérifier les colonnes
print(df.columns)

# Fonction pour simplifier les titres des emplois
def title_simplifier(title):
    if 'data scientist' in title.lower():
        return 'data scientist'
    elif 'data engineer' in title.lower():
        return 'data engineer'
    elif 'analyst' in title.lower():
        return 'analyst'
    elif 'machine learning' in title.lower():
        return 'mle'
    elif 'manager' in title.lower():
        return 'manager'
    elif 'director' in title.lower():
        return 'director'
    else:
        return 'na'
    
# Fonction pour déterminer la séniorité
def seniority(title):
    if 'sr' in title.lower() or 'senior' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
        return 'senior'
    elif 'jr' in title.lower() or 'jr.' in title.lower():
        return 'jr'
    else:
        return 'na'

# Appliquer les fonctions de simplification
df['job_simp'] = df['Job Title'].apply(title_simplifier)
df['seniority'] = df['Job Title'].apply(seniority)

# Afficher les comptes des titres simplifiés
print(df.job_simp.value_counts())
print(df.seniority.value_counts())

# Fixer l'état de Los Angeles
df['job_state'] = df.job_state.apply(lambda x: x.strip() if x.strip().lower() != 'los angeles' else 'CA')
print(df.job_state.value_counts())

# Longueur de la description de l'emploi
df['desc_len'] = df['Job Description'].apply(lambda x: len(x))

# Compter les concurrents
df['num_comp'] = df['Competitors'].apply(lambda x: len(x.split(',')) if x != '-1' else 0)

# Convertir le salaire horaire en annuel
df['min_salary'] = df.apply(lambda x: x.min_salary*2 if x.hourly == 1 else x.min_salary, axis=1)
df['max_salary'] = df.apply(lambda x: x.max_salary*2 if x.hourly == 1 else x.max_salary, axis=1)

# Nettoyer le texte de l'entreprise
df['company_txt'] = df.company_txt.apply(lambda x: x.replace('\n', ''))

# Afficher les statistiques descriptives
print(df.describe())

# Créer un DataFrame pour les catégories
df_cat = df[['Location', 'Headquarters', 'Size', 'Type of ownership', 'Industry', 'Sector', 
             'Revenue', 'company_txt', 'job_state', 'same_state', 'python_yn', 
             'R_yn', 'spark', 'aws', 'excel', 'job_simp', 'seniority']]

# Graphique pour les types d'emplois simplifiés (job_simp)
job_simp_counts = df['job_simp'].value_counts()

plt.figure(figsize=(10, 6))  # Ajuste la taille du graphique
sns.barplot(x=job_simp_counts.index, y=job_simp_counts.values)

# Configure les étiquettes de l'axe x
plt.xticks(rotation=45)
plt.title('Number of Jobs by Simplified Job Title')
plt.xlabel('Simplified Job Title')
plt.ylabel('Number of Jobs')
plt.show()

# Graphique pour la séniorité
seniority_counts = df['seniority'].value_counts()

plt.figure(figsize=(10, 6))  # Ajuste la taille du graphique
sns.barplot(x=seniority_counts.index, y=seniority_counts.values)

# Configure les étiquettes de l'axe x
plt.xticks(rotation=45)
plt.title('Number of Jobs by Seniority Level')
plt.xlabel('Seniority Level')
plt.ylabel('Number of Jobs')
plt.show()
