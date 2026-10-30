import pandas as pd
import mygene

cna_path = r"C:\Users\jiyad\Desktop\PROJECT\CPTAC\raw_data\rcc_cptac_gdc\data_cna.txt"
cna = pd.read_csv(cna_path, sep='\t')
entrez_ids = cna['Entrez_Gene_Id'].dropna().astype(int).unique().tolist()
print(f"{len(entrez_ids)} unique Entrez IDs to map")

mg = mygene.MyGeneInfo()
result = mg.querymany(entrez_ids, scopes='entrezgene', fields='symbol', species='human')

mapping = pd.DataFrame(result)
mapping = mapping[~mapping.get('notfound', False).fillna(False)]
mapping = mapping.dropna(subset=['symbol'])[['query', 'symbol']]
mapping.columns = ['entrez_id', 'gene_symbol']
mapping['entrez_id'] = mapping['entrez_id'].astype(int)
mapping = mapping.drop_duplicates('entrez_id')

out_path = r"C:\Users\jiyad\Desktop\PROJECT\CPTAC\raw_data\rcc_cptac_gdc\entrez_to_symbol.csv"
mapping.to_csv(out_path, index=False)
print(f"Mapped {len(mapping)} / {len(entrez_ids)} Entrez IDs -> saved to {out_path}")