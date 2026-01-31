# Regra: Proporcionalidade Paramétrica

**Contexto**: Ao alterar a geometria de um ambiente (Área/Altura), as quantidades de serviço e materiais devem variar de forma coerente.

**Regras de Cálculo**:
1.  **Fator de Escala (K)**: `K = Nova Área / Área Original`.
2.  **Serviços de Piso/Teto** (ex: Porcelanato, Pintura Teto):
    - `Nova Quantidade = Quantidade Original * K`.
    - Os consumos unitários de material (`base_qtd`) **NÃO** mudam (o consumo por m² é constante).
3.  **Serviços de Parede** (ex: Pintura Parede):
    - Deve-se considerar a variação do Perímetro e Altura se possível.
    - Simplificação aceitável: Variar proporcionalmente à `(Nova Altura / Altura Original) * (Raiz Quadrada da Nova Área / Raiz Quadrada da Área Original)`.
    - Ou usar um input explícito de "Nova Área de Parede".
4.  **Serviços Pontuais** (ex: Instalar Vaso Sanitário):
    - **NÃO** devem escalar automaticamente com a área, a menos que especificado (ex: 2 vasos em banheiro grande).
    - Por padrão: Manter quantidade original.

**Restrição de Engenharia**:
- Quantidades nunca podem ser negativas.
- Quantidades nunca podem ser zero se o serviço estiver listado (exceto demolição em obra nova).
