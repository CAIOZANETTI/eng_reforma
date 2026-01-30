rules >  não criar tabelas durante o workflow trabalhar com os dados existentes

renomear as skill pode ser verbo projeto> projetar, custo > custear, 
outro ponto é remover os numeros dos skills

ajuste na skill do ibge
reforma_ibge_ranking, na verdade o ibge é o senso que mostra a quantidade de imoveis no brasil não esta relacionado com reforma, esta relacionado com a diversidade dos imoveis e sua quantidade
analise e entenda e mude essa skill o nome correto deve ser imoveis_ibge_ranking, Top 100 tipos de reforma, seria tipos de imoveis!!

ajuste o workflow geral do sistema é :
1 skill do ibge pode gerar n combinações com base no estudo real de moradia do brasil
2 skill de projeto faz em cima dessas moradias do ibge n opções de reforma para cada tipo de imovel
3 skill de escopo detalha os serviços da reforma estilo eap ou wbs ( incluir recurso do pmbok)
4 skill de quantificar quantifica o escopo
5 skill de custear inclui os custos de cada item com base nas tabelas disponiveis
6 skill converte em json conforme o padrao do obra ninja seguindo as tabelas de material e espaços
7 skill de empreiteiro mostra as varias formas que esse prompt pode ser escrito para ter esse resultado


workflow
uma_reforma_aleatoria_json_obra_ninja >  1,2,3,4,5,6 ( gerar um json e .md) explicando o processo

atualizar o plano_implementacao_agentes.md
