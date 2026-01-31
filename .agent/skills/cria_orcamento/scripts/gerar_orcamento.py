import csv
import argparse
import os

def load_services(kb_path):
    services = []
    csv_path = os.path.join(kb_path, "services.csv")
    if not os.path.exists(csv_path):
        print(f"Aviso: {csv_path} não encontrado.")
        return []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            services.append(row)
    return services

def suggest_services(prompt, services):
    suggestions = []
    # Simple keyword matching logic (placeholder for more advanced AI)
    prompt_lower = prompt.lower()
    
    keywords = {
        "banheiro": ["demolicao", "revestimento", "bacia", "lavatorio", "pintura", "porcelanato"],
        "cozinha": ["demolicao", "revestimento", "pia", "torneira", "pintura", "porcelanato"],
        "pintura": ["pintura"],
        "piso": ["pisos", "porcelanato", "demolicao"],
    }

    matched_keywords = []
    for key, values in keywords.items():
        if key in prompt_lower:
            matched_keywords.extend(values)
            
    if not matched_keywords:
        # Default fallback
        matched_keywords = ["pintura", "demolicao"]

    for svc in services:
        name = svc['name'].lower()
        if any(k in name for k in matched_keywords):
            suggestions.append(svc)
            
    return suggestions

def generate_markdown(prompt, suggestions, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Orçamento Preliminar: {prompt}\n\n")
        f.write("> Gerado automaticamente pela skill `cria_orcamento`\n\n")
        
        f.write("## Serviços Sugeridos\n\n")
        f.write("| ID do Serviço | Descrição | Quantidade Estimada | Unidade |\n")
        f.write("|---|---|---|---|\n")
        
        for s in suggestions:
            # Default quantity and unit (should be refined with more intelligence later)
            qtd = 1
            unit = "un" 
            f.write(f"| `{s['id']}` | {s['name']} | {qtd} | {unit} |\n")
            
        f.write("\n\n## Próximos Passos\n")
        f.write("1. Ajuste as quantidades na tabela acima.\n")
        f.write("2. Execute `/converter_md_reforma_ninja_em_json` para gerar o arquivo final.\n")
        
    print(f"Orçamento gerado em: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerar orçamento MD a partir de prompt")
    parser.add_argument("--prompt", required=True, help="Descrição do pedido")
    parser.add_argument("--kb_dir", required=True, help="Diretório da Knowledge Base")
    parser.add_argument("--output", required=True, help="Arquivo de saída MD")
    
    args = parser.parse_args()
    
    services = load_services(args.kb_dir)
    suggestions = suggest_services(args.prompt, services)
    generate_markdown(args.prompt, suggestions, args.output)
