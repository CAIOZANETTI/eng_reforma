import csv
import os

CSV_PATH = r"d:\github\eng_reforma\obra_ninja\csv\lista_reforma\lista_reforma_ranking.csv"
OUTPUT_DIR = r"d:\github\eng_reforma\ranking_test_ott"

# Base Costs per m2 (Estimated for 2025 Market)
COST_DB = {
    "Popular": 1200.00,
    "Médio": 2200.00,
    "Luxo": 3800.00,
    "Comercial": 2500.00
}

def parse_currency(val):
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    rows = []
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [name.strip() for name in reader.fieldnames]
        for row in reader:
            rows.append(row)

    # --- Generate Synthetic Report ---
    synthetic_md = "# Relatório Sintético de Orçamento (Estimativa)\n\n"
    synthetic_md += "| Item | Descrição (Tipo/Ambiente) | Padrão | Unid. | Qtd (Area) | Custo Unit. (Est.) | Custo Total |\n"
    synthetic_md += "|:---:|:---|:---|:---:|:---:|:---:|:---:|\n"

    total_general = 0.0

    processed_data = []

    for row in rows:
        try:
            row_id = row['id']
            tipo = row['tipo']
            ambiente = row['área (ambiente)']
            area_str = row['area_m2']
            acabamento = row.get('acabamento (popular / médio / luxo / comercial)', 'Popular').strip().capitalize()
            descricao = row.get('descrição da reforma (sem ampliação)', '')

            try:
                area = float(area_str)
            except:
                area = 0.0

            # Determine Unit Price
            unit_price = COST_DB.get(acabamento, 1500.00) # Default backup
            
            # Simple heuristic adjustment for very small areas (fixed overhead)
            # If area < 5m2, increase unit price by 30% to account for logistics/overhead
            if area > 0 and area < 5:
                unit_price *= 1.3

            total_price = area * unit_price
            total_general += total_price

            processed_data.append({
                "id": row_id,
                "desc": f"{tipo} - {ambiente}",
                "acabamento": acabamento,
                "area": area,
                "unit_price": unit_price,
                "total_price": total_price,
                "full_desc": descricao
            })

            synthetic_md += f"| {row_id} | {tipo} - {ambiente} | {acabamento} | m² | {area:.2f} | {parse_currency(unit_price)} | {parse_currency(total_price)} |\n"

        except Exception as e:
            print(f"Error processing row {row.get('id')}: {e}")

    synthetic_md += f"| | **TOTAL GERAL** | | | | | **{parse_currency(total_general)}** |\n"

    with open(os.path.join(OUTPUT_DIR, "relatorio_sinapi_sintetico.md"), "w", encoding="utf-8") as f:
        f.write(synthetic_md)

    # --- Generate Analytic Report ---
    analytic_md = "# Relatório Analítico de Orçamento (Estimativa)\n\n"
    analytic_md += "> **Nota**: Valores baseados em estimativas de mercado por padrão de acabamento. A composição detalhada é ilustrativa baseada na descrição do serviço.\n\n"

    for item in processed_data:
        analytic_md += f"## {item['id']}. {item['desc']}\n"
        analytic_md += f"**Custo Estimado**: {parse_currency(item['total_price'])}  \n"
        analytic_md += f"**Área**: {item['area']:.2f} m² | **Padrão**: {item['acabamento']} | **Ref. Unit**: {parse_currency(item['unit_price'])}/m²\n\n"
        
        analytic_md += "| Composição do Serviço (Extraído da Descrição) | Unid. | Qtd |\n"
        analytic_md += "|:---|:---:|:---:|\n"
        
        # Split description into "services"
        services = [s.strip() for s in item['full_desc'].split(',')]
        if not services or services == ['']:
            services = ["Execução de reforma conforme padrão"]

        for svc in services:
             analytic_md += f"| {svc.capitalize()} | vb | 1.0 |\n"
        
        analytic_md += "\n---\n\n"

    with open(os.path.join(OUTPUT_DIR, "relatorio_sinapi_analitico.md"), "w", encoding="utf-8") as f:
        f.write(analytic_md)

    print(f"Reports generated in {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
