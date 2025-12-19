import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("="*60)
print("ANALYSE TOP 10 CLIENTS - VERSION AGRÉGÉE")
print("="*60)

# DIAGNOSTIC
print(f"📊 Données reçues: {len(dataset)} lignes")
print(f"📈 Exemple de données:")
print(dataset.head())

# ============================================
# 1. AGRÉGATION MANUELLE DES DONNÉES
# ============================================
print("\n🔢 Agrégation des données en cours...")

# Regrouper par client et SOMMER les commandes
client_aggregated = dataset.groupby('id_seqClient').agg({
    'nbr_commande_livrees': 'sum',
    'nbr_commande_non_livrees': 'sum'
}).reset_index()

print(f"✅ Clients uniques après agrégation: {len(client_aggregated)}")

# Calculer les totaux et taux
client_aggregated['total_commandes'] = (
    client_aggregated['nbr_commande_livrees'] + 
    client_aggregated['nbr_commande_non_livrees']
)

client_aggregated['taux_livraison'] = (
    client_aggregated['nbr_commande_livrees'] / 
    client_aggregated['total_commandes'] * 100
)

# ============================================
# 2. TOP 10 AVEC CATÉGORISATION
# ============================================
# Sélectionner Top 10 par volume
top10 = client_aggregated.nlargest(10, 'total_commandes').copy()

# Catégorisation
def categoriser_client(row):
    if row['taux_livraison'] >= 90 and row['total_commandes'] >= 50:
        return 'Premium'
    elif row['taux_livraison'] >= 80:
        return 'Fidèle'
    elif row['total_commandes'] >= 30:
        return 'Actif'
    else:
        return 'Standard'

top10['categorie'] = top10.apply(categoriser_client, axis=1)

# ============================================
# 3. DASHBOARD COMPACT (3 VISUELS)
# ============================================
fig = plt.figure(figsize=(18, 10))

# Graphique 1: Barres empilées + Taux (gauche)
ax1 = plt.subplot(2, 2, 1)
x_pos = range(len(top10))
bar_width = 0.6

bars_livrees = ax1.bar(x_pos, top10['nbr_commande_livrees'], bar_width,
                       color='#2ecc71', alpha=0.8, label='Livrées')
bars_non_livrees = ax1.bar(x_pos, top10['nbr_commande_non_livrees'], bar_width,
                           bottom=top10['nbr_commande_livrees'],
                           color='#e74c3c', alpha=0.8, label='Non-livrées')

ax1.set_xlabel('Clients')
ax1.set_ylabel('Nombre de commandes')
ax1.set_title('TOP 10 CLIENTS - VOLUME DE COMMANDES', fontweight='bold')
ax1.set_xticks(x_pos)
ax1.set_xticklabels([f'C{int(id)}' for id in top10['id_seqClient']], rotation=45)
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# Ajouter les totaux
for i, total in enumerate(top10['total_commandes']):
    ax1.text(i, total + 0.5, str(int(total)), 
            ha='center', va='bottom', fontweight='bold')

# Graphique 2: Taux de livraison (haut droit)
ax2 = plt.subplot(2, 2, 2)
colors_cat = {'Premium': '#9b59b6', 'Fidèle': '#3498db', 
              'Actif': '#2ecc71', 'Standard': '#f1c40f'}

for i, (_, row) in enumerate(top10.iterrows()):
    ax2.bar(i, row['taux_livraison'], color=colors_cat[row['categorie']], 
            alpha=0.8, edgecolor='black')

ax2.set_xlabel('Clients')
ax2.set_ylabel('Taux de livraison (%)')
ax2.set_title('PERFORMANCE ET CATÉGORISATION', fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels([f'C{int(id)}' for id in top10['id_seqClient']], rotation=45)
ax2.set_ylim([0, 105])
ax2.grid(True, alpha=0.3, axis='y')

# Ajouter les valeurs de taux
for i, taux in enumerate(top10['taux_livraison']):
    ax2.text(i, taux + 2, f'{taux:.1f}%', 
            ha='center', va='bottom', fontweight='bold')

# Légende des catégories
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=colors_cat[cat], label=cat) 
                   for cat in ['Premium', 'Fidèle', 'Actif', 'Standard']]
ax2.legend(handles=legend_elements, loc='upper right')

# Graphique 3: Camembert répartition (bas gauche)
ax3 = plt.subplot(2, 2, 3)
categorie_counts = top10['categorie'].value_counts()
ax3.pie(categorie_counts.values, labels=categorie_counts.index,
        autopct='%1.1f%%', colors=[colors_cat[cat] for cat in categorie_counts.index],
        startangle=90)
ax3.set_title('RÉPARTITION DES TOP 10 PAR CATÉGORIE', fontweight='bold')

# Graphique 4: Matrice Volume vs Performance (bas droit)
ax4 = plt.subplot(2, 2, 4)
scatter = ax4.scatter(top10['total_commandes'], top10['taux_livraison'],
                     c=range(len(top10)), cmap='viridis', s=200, alpha=0.7,
                     edgecolors='black')

# Ajouter les labels des clients
for i, (_, row) in enumerate(top10.iterrows()):
    ax4.annotate(f"C{int(row['id_seqClient'])}", 
                (row['total_commandes'], row['taux_livraison']),
                xytext=(5, 5), textcoords='offset points', fontsize=9)

ax4.set_xlabel('Volume total de commandes')
ax4.set_ylabel('Taux de livraison (%)')
ax4.set_title('MATRICE VOLUME vs PERFORMANCE', fontweight='bold')
ax4.grid(True, alpha=0.3)

# Lignes de référence
ax4.axhline(y=80, color='orange', linestyle='--', alpha=0.5, label='Seuil 80%')
ax4.axvline(x=top10['total_commandes'].median(), color='green', 
            linestyle='--', alpha=0.5, label='Médiane volume')

ax4.legend()

# ============================================
# 4. TABLEAU SYNTHÈSE (sans erreur)
# ============================================
print("\n📋 TABLEAU SYNTHÈSE TOP 10:")
print("-"*60)
print(f"{'Client':<10} {'Total':<8} {'Livrées':<10} {'Taux %':<10} {'Catégorie':<12}")
print("-"*60)

for _, row in top10.iterrows():
    print(f"C{int(row['id_seqClient']):<9} "
          f"{int(row['total_commandes']):<8} "
          f"{int(row['nbr_commande_livrees']):<10} "
          f"{row['taux_livraison']:<10.1f} "
          f"{row['categorie']:<12}")

print("-"*60)

# Stats globales
print(f"\n📊 STATISTIQUES GLOBALES:")
print(f"• Taux moyen Top 10: {top10['taux_livraison'].mean():.1f}%")
print(f"• Volume moyen: {top10['total_commandes'].mean():.0f} commandes")
print(f"• Clients Premium: {(top10['categorie'] == 'Premium').sum()}")
print(f"• Clients Fidèles: {(top10['categorie'] == 'Fidèle').sum()}")

plt.suptitle('DASHBOARD ANALYSE TOP 10 CLIENTS - NORTHWIND', 
             fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()

print("\n✅ Dashboard généré avec succès!")
    
   