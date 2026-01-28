"""
Orçamento Sintético SINAPI
Sistema para geração de orçamentos resumidos (sintéticos) baseados na tabela SINAPI

Diferença Analítico vs Sintético:
- Analítico: detalha todos os insumos (cimento,  areia, pedreiro, etc.)
- Sintético: apresenta apenas os serviços/itens finais e custo total
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional


class OrcamentoSintetico:
    """Gerador de orçamentos sintéticos para apresentação ao cliente"""
    
    def __init__(self, titulo_obra: str, cliente: str, bdi: float = 0.25):
        """
        Args:
            titulo_obra: Nome do projeto/obra
            cliente: Nome do cliente
            bdi: Taxa de BDI (padrão 25%)
        """
        self.titulo = titulo_obra
        self.cliente = cliente
        self.bdi = bdi
        self.data_geracao = datetime.now().strftime("%d/%m/%Y")
        
        # Estrutura: Grupo → Itens
        self.grupos = {}
    
    def adicionar_grupo(self, nome_grupo: str):
        """Cria um novo grupo de serviços (ex: 'Alvenaria', 'Revestimentos')"""
        if nome_grupo not in self.grupos:
            self.grupos[nome_grupo] = []
    
    def adicionar_servico(
        self, 
        grupo: str,
        descricao: str,
        unidade: str,
        quantidade: float,
        preco_unitario: float
    ):
        """
        Adiciona serviço a um grupo
        
        Args:
            grupo: Nome do grupo (precisa existir, criado com adicionar_grupo)
            descricao: Descrição completa do serviço
            unidade: Unidade (M2, M3, ML, UN, etc.)
            quantidade: Quantidade do serviço
            preco_unitario: Preço unitário (custo direto + BDI já aplicado)
        """
        if grupo not in self.grupos:
            raise ValueError(f"Grupo '{grupo}' não existe. Crie com adicionar_grupo() primeiro.")
        
        self.grupos[grupo].append({
            "descricao": descricao,
            "unidade": unidade,
            "quantidade": quantidade,
            "preco_unitario": preco_unitario,
            "total": quantidade * preco_unitario
        })
    
    def gerar_planilha(self) -> pd.DataFrame:
        """Gera planilha sintética para apresentação"""
        linhas = []
        
        # Cabeçalho
        linhas.append({
            "item": "",
            "descricao": f"ORÇAMENTO SINTÉTICO - {self.titulo}",
            "unidade": "",
            "quantidade": "",
            "preco_unit": "",
            "total": ""
        })
        linhas.append({
            "item": "",
            "descricao": f"Cliente: {self.cliente}",
            "unidade": "",
            "quantidade": "",
            "preco_unit": "",
            "total": ""
        })
        linhas.append({
            "item": "",
            "descricao": f"Data: {self.data_geracao}",
            "unidade": "",
            "quantidade": "",
            "preco_unit": "",
            "total": ""
        })
        linhas.append({})  # Linha vazia
        
        # Cabeçalho de colunas
        linhas.append({
            "item": "ITEM",
            "descricao": "DESCRIÇÃO",
            "unidade": "UND",
            "quantidade": "QUANT",
            "preco_unit": "PREÇO UNIT (R$)",
            "total": "TOTAL (R$)"
        })
        
        # Itens por grupo
        item_numero = 1
        total_geral = 0.0
        
        for grupo_nome, servicos in self.grupos.items():
            # Linha de grupo
            linhas.append({
                "item": "",
                "descricao": f"═══ {grupo_nome.upper()} ═══",
                "unidade": "",
                "quantidade": "",
                "preco_unit": "",
                "total": ""
            })
            
            subtotal_grupo = 0.0
            
            for servico in servicos:
                linhas.append({
                    "item": f"{item_numero}",
                    "descricao": servico["descricao"],
                    "unidade": servico["unidade"],
                    "quantidade": f"{servico['quantidade']:.2f}",
                    "preco_unit": f"{servico['preco_unitario']:.2f}",
                    "total": f"{servico['total']:.2f}"
                })
                
                subtotal_grupo += servico["total"]
                item_numero += 1
            
            # Subtotal do grupo
            linhas.append({
                "item": "",
                "descricao": f"Subtotal - {grupo_nome}",
                "unidade": "",
                "quantidade": "",
                "preco_unit": "",
                "total": f"R$ {subtotal_grupo:,.2f}"
            })
            linhas.append({})  # Linha vazia
            
            total_geral += subtotal_grupo
        
        # Total geral
        linhas.append({
            "item": "",
            "descricao": "TOTAL GERAL DA OBRA",
            "unidade": "",
            "quantidade": "",
            "preco_unit": "",
            "total": f"R$ {total_geral:,.2f}"
        })
        
        return pd.DataFrame(linhas)
    
    def exportar_excel(self, caminho_arquivo: str):
        """Exporta para Excel formatado"""
        df = self.gerar_planilha()
        
        with pd.ExcelWriter(caminho_arquivo, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name="Orçamento", index=False)
        
        print(f"✅ Orçamento sintético exportado para: {caminho_arquivo}")
    
    def imprimir_resumo(self):
        """Imprime resumo no console"""
        print(f"\n{'='*70}")
        print(f"ORÇAMENTO SINTÉTICO - {self.titulo}")
        print(f"Cliente: {self.cliente}")
        print(f"Data: {self.data_geracao}")
        print(f"BDI: {self.bdi*100:.1f}%")
        print(f"{'='*70}\n")
        
        total_geral = 0.0
        
        for grupo_nome, servicos in self.grupos.items():
            print(f"\n┌─ {grupo_nome.upper()} ─────────────────────────")
            subtotal = 0.0
            
            for i, servico in enumerate(servicos, 1):
                print(f"│ {i}. {servico['descricao']}")
                print(f"│    {servico['quantidade']:.2f} {servico['unidade']} × R$ {servico['preco_unitario']:.2f} = R$ {servico['total']:,.2f}")
                subtotal += servico['total']
            
            print(f"└─ Subtotal: R$ {subtotal:,.2f}\n")
            total_geral += subtotal
        
        print(f"{'='*70}")
        print(f"TOTAL GERAL: R$ {total_geral:,.2f}")
        print(f"{'='*70}\n")


# ===== TEMPLATE PADRÃO DE REFORMA RESIDENCIAL =====

def orcamento_reforma_apartamento_padrao(
    area_reforma_m2: float = 70,
    padrao: str = "normal",  # popular, normal, alto
    cliente: str = "Cliente"
) -> OrcamentoSintetico:
    """
    Template de orçamento sintético para reforma de apartamento
    
    Args:
        area_reforma_m2: Área a reformar
        padrao: Padrão de acabamento (popular, normal, alto)
        cliente: Nome do cliente
    
    Returns:
        OrcamentoSintetico preenchido
    """
    # Preços por m² (com BDI incluído) - Referência 2026
    precos_m2 = {
        "popular": {
            "pisos": 80,
            "paredes": 60,
            "pintura": 35,
            "eletrica": 85,
            "hidraulica": 95,
            "banheiro": 450,  # por banheiro completo
            "cozinha": 650  # por cozinha completa
        },
        "normal": {
            "pisos": 140,
            "paredes": 110,
            "pintura": 55,
            "eletrica": 130,
            "hidraulica": 140,
            "banheiro": 850,
            "cozinha": 1200
        },
        "alto": {
            "pisos": 250,
            "paredes": 200,
            "pintura": 85,
            "eletrica": 180,
            "hidraulica": 200,
            "banheiro": 1800,
            "cozinha": 2500
        }
    }
    
    p = precos_m2.get(padrao, precos_m2["normal"])
    
    # Criar orçamento
    orc = OrcamentoSintetico(
        titulo_obra=f"Reforma Apartamento {area_reforma_m2:.0f}m² - Padrão {padrao.title()}",
        cliente=cliente,
        bdi=0.28
    )
    
    # Grupo 1: Demolição e Preparo
    orc.adicionar_grupo("Demolição e Preparo")
    orc.adicionar_servico("Demolição e Preparo", "Demolição de revestimentos e pisos antigos", "M2", area_reforma_m2, 25)
    orc.adicionar_servico("Demolição e Preparo", "Remoção de entulho e limpeza", "M3", area_reforma_m2 * 0.08, 180)
    
    # Grupo 2: Instalações
    orc.adicionar_grupo("Instalações Elétricas e Hidráulicas")
    orc.adicionar_servico("Instalações Elétricas e Hidráulicas", "Instalação elétrica completa (Fiação, quadro, disjuntores)", "M2", area_reforma_m2, p["eletrica"])
    orc.adicionar_servico("Instalações Elétricas e Hidráulicas", "Instalação hidráulica (Água fria, água quente, esgoto)", "M2", area_reforma_m2, p["hidraulica"])
    
    # Grupo 3: Revestimentos
    orc.adicionar_grupo("Pisos e Revestimentos")
    orc.adicionar_servico("Pisos e Revestimentos", f"Piso em porcelanato (padrão {padrao})", "M2", area_reforma_m2, p["pisos"])
    orc.adicionar_servico("Pisos e Revestimentos", f"Revestimento de paredes banheiro/cozinha", "M2", area_reforma_m2 * 0.3, p["paredes"])
    
    # Grupo 4: Pintura
    orc.adicionar_grupo("Pintura e Acabamentos")
    orc.adicionar_servico("Pintura e Acabamentos", "Pintura acrílica premium (2 demãos)", "M2", area_reforma_m2 * 2.5, p["pintura"])
    orc.adicionar_servico("Pintura e Acabamentos", "Rodapés e acabamentos gerais", "ML", area_reforma_m2 * 0.6, 45)
    
    # Grupo 5: Cozinha e Banheiros
    orc.adicionar_grupo("Cozinha e Banheiros")
    orc.adicionar_servico("Cozinha e Banheiros", f"Reforma completa de cozinha (padrão {padrao})", "UN", 1, p["cozinha"])
    orc.adicionar_servico("Cozinha e Banheiros", f"Reforma completa de banheiro (padrão {padrao})", "UN", 1, p["banheiro"])
    
    return orc


# ===== EXEMPLO DE USO =====

if __name__ == "__main__":
    print("\n╔═══════════════════════════════════════════════════════════╗")
    print("║  SISTEMA DE ORÇAMENTO SINTÉTICO SINAPI                   ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    # Exemplo 1: Orçamento manual
    print("\n[1] Orçamento Manual - Reforma Banheiro")
    print("─" * 60)
    
    orc1 = OrcamentoSintetico("Reforma Banheiro Social", "João Silva", bdi=0.25)
    
    orc1.adicionar_grupo("Demolição")
    orc1.adicionar_servico("Demolição", "Demolição de azulejos e piso", "M2", 6.5, 35)
    
    orc1.adicionar_grupo("Instalações")
    orc1.adicionar_servico("Instalações", "Troca completa de tubulação hidráulica", "CJ", 1, 850)
    orc1.adicionar_servico("Instalações", "Instalação elétrica (pontos + ducha)", "CJ", 1, 420)
    
    orc1.adicionar_grupo("Revestimentos")
    orc1.adicionar_servico("Revestimentos", "Porcelanato antiderrapante 60x60", "M2", 6.5, 145)
    orc1.adicionar_servico("Revestimentos", "Porcelanato parede efeito mármore", "M2", 18, 165)
    
    orc1.adicionar_grupo("Louças e Metais")
    orc1.adicionar_servico("Louças e Metais", "Conjunto de louças (vaso, pia, box)", "CJ", 1, 1850)
    orc1.adicionar_servico("Louças e Metais", "Metais cromados linha intermediária", "CJ", 1, 980)
    
    orc1.imprimir_resumo()
    # orc1.exportar_excel("orcamento_banheiro.xlsx")
    
    # Exemplo 2: Template automático
    print("\n\n[2] Orçamento Automático - Template Apartamento")
    print("─" * 60)
    
    orc2 = orcamento_reforma_apartamento_padrao(
        area_reforma_m2=85,
        padrao="normal",
        cliente="Maria Oliveira"
    )
    
    orc2.imprimir_resumo()
    # orc2.exportar_excel("orcamento_apartamento_85m2.xlsx")
    
    print("\n✅ Orçamentos sintéticos gerados com sucesso!")
    print("💡 Descomente as linhas .exportar_excel() para salvar em arquivo.\n")
