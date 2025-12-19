import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("="*60)
print("ANALYSE CLIENTS AVEC CATÉGORISATION ADAPTATIVE")
print("="*60)

# 1. Agrégation
client_aggregated = dataset.groupby('id_seqClient').agg({
    'nbr_commande_livrees': 'sum',
    'nbr_commande_non_livrees': 'sum'
}).reset_index()

client_aggregated['total_commandes'] = (
    client_aggregated['nbr_commande_livrees'] + 
    client_aggregated['nbr_commande_non_livrees']
)

client_aggregated['taux_livraison'] = (
    client_aggregated['nbr_commande_livrees'] / 
    client_aggregated['total_commandes'] * 100
)

# 2. Top 10
top10 = client_aggregated.nlargest(10, 'total_commandes').copy()

# 3. CATÉGORISATION ADAPTATIVE (basée sur VOS données)
def categoriser_client_adaptative(row, top10_data):
    """Catégorisation basée sur les percentiles de VOS données"""
    
    # Calculer les seuils basés sur VOS données
    taux_75 = top10_data['taux_livraison'].quantile(0.75)  # 75ème percentile
    taux_50 = top10_data['taux_livraison'].quantile(0.50)  # Médiane
    volume_75 = top10_data['total_commandes'].quantile(0.75)
    volume_50 = top10_data['total_commandes'].quantile(0.50)
    
    # Catégorisation
    if row['taux_livraison'] >= taux_75 and row['total_commandes'] >= volume_75:
        return 'EXCELLENCE'  # Meilleurs des meilleurs
    elif row['taux_livraison'] >= taux_75:
        return 'HAUTE PERFORMANCE'
    elif row['total_commandes'] >= volume_75:
        return 'GROS VOLUME'
    elif row['taux_livraison'] >= taux_50 and row['total_commandes'] >= volume_50:
        return 'BON ÉQUILIBRE'
    elif row['taux_livraison'] >= taux_50:
        return 'PERFORMANCE MOYENNE'
    elif row['total_commandes'] >= volume_50:
        return 'VOLUME MOYEN'
    else:
        return 'STANDARD'

# Appliquer la catégorisation
top10['categorie'] = top10.apply(
    lambda row: categoriser_client_adaptative(row, top10), 
    axis=1
)

# 4. AFFICHER LES SEUILS CALCULÉS
print("\n📊 SEUILS CALCULÉS (basés sur VOS données):")
print(f"• Médiane taux: {top10['taux_livraison'].median():.1f}%")
print(f"• 75ème percentile taux: {top10['taux_livraison'].quantile(0.75):.1f}%")
print(f"• Médiane volume: {top10['total_commandes'].median():.0f} commandes")
print(f"• 75ème percentile volume: {top10['total_commandes'].quantile(0.75):.0f} commandes")

print("\n🏷️  CATÉGORIES APPLIQUÉES:")
print(top10[['id_seqClient', 'total_commandes', 'taux_livraison', 'categorie']].to_string())

# 5. VISUALISATION CORRIGÉE
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Graphique 1: Barres avec catégories
ax1 = axes[0, 0]
x_pos = range(len(top10))

# Couleurs par catégorie
couleurs_cat = {
    'EXCELLENCE': '#9b59b6',  # Violet
    'HAUTE PERFORMANCE': '#3498db',  # Bleu
    'GROS VOLUME': '#2ecc71',  # Vert
    'BON ÉQUILIBRE': '#f1c40f',  # Jaune
    'PERFORMANCE MOYENNE': '#e67e22',  # Orange
    'VOLUME MOYEN': '#e74c3c',  # Rouge
    'STANDARD': '#95a5a6'  # Gris
}

for i, (_, row) in enumerate(top10.iterrows()):
    ax1.bar(i, row['total_commandes'], 
            color=couleurs_cat[row['categorie']],
            alpha=0.8, edgecolor='black')

ax1.set_xlabel('Clients')
ax1.set_ylabel('Total commandes')
ax1.set_title('TOP 10 CLIENTS - VOLUME PAR CATÉGORIE', fontweight='bold')
ax1.set_xticks(x_pos)
ax1.set_xticklabels([f'C{int(id)}' for id in top10['id_seqClient']], rotation=45)
ax1.grid(True, alpha=0.3, axis='y')

# Graphique 2: Taux de livraison
ax2 = axes[0, 1]
for i, (_, row) in enumerate(top10.iterrows()):
    ax2.bar(i, row['taux_livraison'], 
            color=couleurs_cat[row['categorie']],
            alpha=0.8, edgecolor='black')

ax2.set_xlabel('Clients')
ax2.set_ylabel('Taux de livraison (%)')
ax2.set_title('PERFORMANCE PAR CATÉGORIE', fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels([f'C{int(id)}' for id in top10['id_seqClient']], rotation=45)
ax2.set_ylim([0, 105])
ax2.grid(True, alpha=0.3, axis='y')

# Graphique 3: Répartition catégories
ax3 = axes[1, 0]
categorie_counts = top10['categorie'].value_counts()
bars = ax3.bar(range(len(categorie_counts)), categorie_counts.values,
              color=[couleurs_cat[cat] for cat in categorie_counts.index])

ax3.set_xlabel('Catégorie')
ax3.set_ylabel('Nombre de clients')
ax3.set_title('RÉPARTITION DES CATÉGORIES DANS LE TOP 10', fontweight='bold')
ax3.set_xticks(range(len(categorie_counts)))
ax3.set_xticklabels(categorie_counts.index, rotation=45, ha='right')

# Ajouter les valeurs
for bar in bars:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}', ha='center', va='bottom')

# Graphique 4: Matrice avec catégories
ax4 = axes[1, 1]
for categorie in top10['categorie'].unique():
    data_cat = top10[top10['categorie'] == categorie]
    ax4.scatter(data_cat['total_commandes'], data_cat['taux_livraison'],
               s=150, alpha=0.7, edgecolors='black', linewidth=1,
               color=couleurs_cat[categorie], label=categorie)

ax4.set_xlabel('Volume total de commandes')
ax4.set_ylabel('Taux de livraison (%)')
ax4.set_title('MATRICE VOLUME vs PERFORMANCE PAR CATÉGORIE', fontweight='bold')
ax4.grid(True, alpha=0.3)
ax4.legend(loc='best')

plt.suptitle('ANALYSE TOP 10 CLIENTS - CATÉGORISATION ADAPTATIVE', 
             fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()

print("\n" + "="*60)
print("✅ ANALYSE TERMINÉE AVEC CATÉGORISATION ADAPTATIVE")
print("="*60)