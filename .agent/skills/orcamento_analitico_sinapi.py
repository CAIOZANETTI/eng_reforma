"""
Orçamento Analítico SINAPI  
Sistema especializado para consulta e composição de orçamentos detalhados baseados na tabela SINAPI (Caixa Econômica Federal)

Este módulo permite:
1. Consultar preços de insumos (materiais e mão de obra)
2. Montar composições de custos unitários (CPU)
3. Gerar orçamento analítico completo
4. Aplicar BDI e impostos
"""

import pandas as pd
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import requests


class SINAPIConsultor:
    """Consulta dados da tabela SINAPI (Caixa Econômica Federal)"""
    
    def __init__(self, estado: str = "SP", referencia: str = None):
        """
        Inicializa consultor SINAPI
        
        Args:
            estado: Sigla do estado (SP, RJ, MG, etc.)
            referencia: Mês/ano de referência (MM/AAAA). Se None, usa mês atual
        """
        self.estado = estado
        self.referencia = referencia or datetime.now().strftime("%m/%Y")
        self.base_url = "https://www.caixa.gov.br/site/Paginas/downloads.aspx"
        
        # Em produção real, carregar de planilha SINAPI oficial
        # Aqui usamos estrutura de exemplo
        self.insumos = self._carregar_base_insumos()
        self.composicoes = self._carregar_composicoes()
    
    def _carregar_base_insumos(self) -> pd.DataFrame:
        """Carrega base de insumos SINAPI (simulação)"""
        # Em produção: ler de planilha Excel oficial SINAPI
        # Estrutura típica: Código, Descrição, Unidade, Preço Mediano
        
        dados_exemplo = {
            "codigo": ["88309", "00000374", "00004956", "00009553", "04020"],
            "descricao": [
                "PEDREIRO COM ENCARGOS COMPLEMENTARES",
                "SERVENTE COM ENCARGOS COMPLEMENTARES",
                "CIMENTO PORTLAND COMPOSTO CP II-32",
                "AREIA MEDIA - POSTO JAZIDA/FORNECEDOR (RETIRADO NA JAZIDA, SEM TRANSPORTE)",
                "TIJOLO CERAMICO FURADO 10X20X20CM (6 FUROS)"
            ],
            "unidade": ["H", "H", "KG", "M3", "UN"],
            "preco_mediano": [28.50, 19.20, 0.78, 85.00, 0.95]
        }
        
        return pd.DataFrame(dados_exemplo)
    
    def _carregar_composicoes(self) -> Dict:
        """Carrega composições de custos unitários (CPU) SINAPI"""
        # Estrutura: código da composição → lista de insumos com coeficientes
        
        return {
            "87879": {  # ALVENARIA DE VEDACAO DE BLOCOS CERAMICOS FURADOS
                "descricao": "ALVENARIA DE VEDACAO DE BLOCOS CERAMICOS FURADOS NA HORIZONTAL DE 10X20X20 CM (ESPESSURA 10 CM) DE PAREDES COM AREA LIQUIDA MAIOR OU IGUAL A 6 M² SEM VÃOS E ARGAMASSA DE ASSENTAMENTO COM PREPARO EM BETONEIRA. AF_06/2014",
                "unidade": "M2",
                "insumos": [
                    {"codigo": "88309", "coeficiente": 0.9},  # Pedreiro
                    {"codigo": "00000374", "coeficiente": 0.9},  # Servente
                    {"codigo": "04020", "coeficiente": 26.5},  # Tijolo
                    {"codigo": "00004956", "coeficiente": 8.0},  # Cimento
                    {"codigo": "00009553", "coeficiente": 0.024}  # Areia
                ]
            },
            "74209/003": {  # CONCRETO FCK=20MPA
                "descricao": "CONCRETO FCK = 20MPA, TRAÇO 1:2,7:3 (CIMENTO/ AREIA MEDIA/ BRITA 1) - PREPARO MECANICO COM BETONEIRA 400 L. AF_07/2016",
                "unidade": "M3",
                "insumos": [
                    {"codigo": "88309", "coeficiente": 4.5},
                    {"codigo": "00000374", "coeficiente": 9.0},
                    {"codigo": "00004956", "coeficiente": 348.0},
                    {"codigo": "00009553", "coeficiente": 0.55}
                ]
            }
        }
    
    def consultar_insumo(self, codigo: str = None, descricao: str = None) -> pd.DataFrame:
        """
        Consulta insumo por código ou descrição
        
        Args:
            codigo: Código SINAPI do insumo
            descricao: Parte da descrição para busca
        
        Returns:
            DataFrame com resultados
        """
        if codigo:
            return self.insumos[self.insumos['codigo'] == codigo]
        elif descricao:
            mask = self.insumos['descricao'].str.contains(descricao, case=False, na=False)
            return self.insumos[mask]
        else:
            return self.insumos
    
    def calcular_composicao(self, codigo_composicao: str) -> Dict:
        """
        Calcula custo unitário de uma composição
        
        Args:
            codigo_composicao: Código SINAPI da composição
        
        Returns:
            Dicionário com detalhamento e custo total
        """
        if codigo_composicao not in self.composicoes:
            raise ValueError(f"Composição {codigo_composicao} não encontrada")
        
        comp = self.composicoes[codigo_composicao]
        detalhamento = []
        custo_total = 0.0
        
        for insumo in comp["insumos"]:
            dados_insumo = self.consultar_insumo(codigo=insumo["codigo"])
            if dados_insumo.empty:
                continue
            
            preco_unit = dados_insumo.iloc[0]["preco_mediano"]
            coef = insumo["coeficiente"]
            custo_parcial = preco_unit * coef
            custo_total += custo_parcial
            
            detalhamento.append({
                "codigo": insumo["codigo"],
                "descricao": dados_insumo.iloc[0]["descricao"],
                "unidade": dados_insumo.iloc[0]["unidade"],
                "coeficiente": coef,
                "preco_unitario": preco_unit,
                "custo_parcial": custo_parcial
            })
        
        return {
            "codigo": codigo_composicao,
            "descricao": comp["descricao"],
            "unidade": comp["unidade"],
            "insumos": detalhamento,
            "custo_unitario_total": custo_total
        }


class OrcamentoAnalitico:
    """Monta orçamentos analíticos completos"""
    
    def __init__(self, consultor: SINAPIConsultor, bdi: float = 0.25):
        """
        Args:
            consultor: Instância de SINAPIConsultor
            bdi: Taxa de BDI (Benefícios e Despesas Indiretas) em decimal (0.25 = 25%)
        """
        self.consultor = consultor
        self.bdi = bdi
        self.itens = []
    
    def adicionar_item(self, codigo_composicao: str, quantidade: float, descricao_custom: str = None):
        """
        Adiciona item ao orçamento
        
        Args:
            codigo_composicao: Código SINAPI
            quantidade: Quantidade a orçar
            descricao_custom: Descrição personalizada (opcional)
        """
        comp = self.consultor.calcular_composicao(codigo_composicao)
        
        self.itens.append({
            "codigo": codigo_composicao,
            "descricao": descricao_custom or comp["descricao"],
            "unidade": comp["unidade"],
            "quantidade": quantidade,
            "custo_unitario": comp["custo_unitario_total"],
            "custo_total": comp["custo_unitario_total"] * quantidade,
            "composicao": comp
        })
    
    def gerar_orcamento(self, aplicar_bdi: bool = True) -> pd.DataFrame:
        """
        Gera planilha de orçamento
        
        Args:
            aplicar_bdi: Se True, aplica BDI ao custo total
        
        Returns:
            DataFrame com orçamento completo
        """
        df = pd.DataFrame(self.itens)
        
        # Calcular subtotais
        custo_direto_total = df["custo_total"].sum()
        
        if aplicar_bdi:
            bdi_valor = custo_direto_total * self.bdi
            preco_venda = custo_direto_total * (1 + self.bdi)
        else:
            bdi_valor = 0
            preco_venda = custo_direto_total
        
        # Adicionar linha de totais
        resumo = pd.DataFrame([
            {"descricao": "CUSTO DIRETO TOTAL", "custo_total": custo_direto_total},
            {"descricao": f"BDI ({self.bdi*100:.1f}%)", "custo_total": bdi_valor},
            {"descricao": "PREÇO DE VENDA TOTAL", "custo_total": preco_venda}
        ])
        
        return pd.concat([
            df[["codigo", "descricao", "unidade", "quantidade", "custo_unitario", "custo_total"]],
            resumo
        ], ignore_index=True)
    
    def exportar_excel(self, caminho_arquivo: str):
        """Exporta orçamento para Excel"""
        df = self.gerar_orcamento()
        df.to_excel(caminho_arquivo, index=False, sheet_name="Orçamento Analítico")
        print(f"Orçamento exportado para: {caminho_arquivo}")
    
    def exportar_json(self, caminho_arquivo: str):
        """Exporta orçamento detalhado em JSON (com composições)"""
        dados = {
            "data_geracao": datetime.now().isoformat(),
            "estado": self.consultor.estado,
            "referencia_sinapi": self.consultor.referencia,
            "bdi": self.bdi,
            "itens": self.itens,
            "resumo": {
                "custo_direto": sum(item["custo_total"] for item in self.itens),
                "bdi_valor": sum(item["custo_total"] for item in self.itens) * self.bdi,
                "preco_venda": sum(item["custo_total"] for item in self.itens) * (1 + self.bdi)
            }
        }
        
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        
        print(f"Orçamento JSON exportado para: {caminho_arquivo}")


# ===== EXEMPLO DE USO =====

if __name__ == "__main__":
    # Inicializar consultor
    consultor = SINAPIConsultor(estado="SP", referencia="01/2026")
    
    # Consultar insumos
    print("=== CONSULTA DE INSUMOS ===")
    resultado = consultor.consultar_insumo(descricao="PEDREIRO")
    print(resultado)
    print()
    
    # Calcular composição
    print("=== COMPOSIÇÃO: AL VENARIA DE BLOCOS ===")
    comp = consultor.calcular_composicao("87879")
    print(f"Descrição: {comp['descricao']}")
    print(f"Custo Unitário: R$ {comp['custo_unitario_total']:.2f}/{comp['unidade']}")
    print("\nInsumos:")
    for insumo in comp["insumos"]:
        print(f"  - {insumo['descricao']}: {insumo['coeficiente']} {insumo['unidade']} × R$ {insumo['preco_unitario']:.2f} = R$ {insumo['custo_parcial']:.2f}")
    print()
    
    # Montar orçamento analítico
    print("=== ORÇAMENTO ANALÍTICO ===")
    orcamento = OrcamentoAnalitico(consultor, bdi=0.28)
    
    # Adicionar itens
    orcamento.adicionar_item("87879", quantidade=120.5, descricao_custom="Alvenaria de vedação - Paredes Internas")
    orcamento.adicionar_item("74209/003", quantidade=5.5, descricao_custom="Concreto estrutural - Pilares")
    
    # Gerar e exibir
    df_orcamento = orcamento.gerar_orcamento()
    print(df_orcamento.to_string(index=False))
    print()
    
    # Exportar
    # orcamento.exportar_excel("orcamento_reforma.xlsx")
    # orcamento.exportar_json("orcamento_reforma.json")
    
    print("\n✅ Orçamento analítico gerado com sucesso!")
