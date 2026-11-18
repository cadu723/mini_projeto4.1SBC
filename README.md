# Mini-Projeto 4 — Base de Doenças em Grafo de Propriedades (Memgraph + Cypher)

Equipe: Caio Eduardo e David Alves

Refaz o Mini-Projeto 3 (ontologia RDF/OWL de doenças, sintomas e tratamentos) como grafo
de propriedades, persistido no Memgraph (Docker) e consultado com Cypher.

## Modelo do grafo
40 nós e 70 relacionamentos.

| Rótulos do nó | Qtde | Propriedades |
|---|---|---|
| Doenca:DoencaInfecciosa:DoencaViral / DoencaBacteriana | 8 | id, nome, codigoCID, taxaLetalidade, periodoIncubacaoDias |
| Doenca:DoencaCronica | 2 | id, nome, codigoCID, taxaLetalidade |
| Sintoma:ManifestacaoClinica | 8 | id, nome, gravidade |
| Medicamento:Tratamento | 8 | id, nome, dosagemMg |
| TerapiaSuporte:Tratamento | 2 | id, nome |
| AgentePatogenico | 6 | id, nome |
| Medico:Pessoa | 2 | id, nome |
| Paciente:Pessoa | 4 | id, nome, idadePaciente, statusClinico |

Todos os nós de Doenca, Sintoma, Tratamento e AgentePatogenico também têm o rótulo EntidadeSaude.

| Relacionamento | Qtde |
|---|---|
| (Doenca)-[:CAUSADA_POR]->(AgentePatogenico) | 8 |
| (Doenca)-[:APRESENTA_SINTOMA]->(Sintoma) | 30 |
| (Doenca)-[:TRATADA_COM]->(Tratamento) | 18 |
| (Doenca)-[:EVOLUI_PARA]->(Doenca) | 2 |
| (Medicamento)-[:INTERAGE_COM]->(Medicamento) (nos dois sentidos) | 4 |
| (Paciente)-[:DIAGNOSTICADO_COM]->(Doenca) | 4 |
| (Paciente)-[:ATENDIDO_POR]->(Medico) | 4 |

### Do OWL (MP3) para o grafo de propriedades
- Hierarquia de classes (subClassOf): vira rótulos múltiplos no mesmo nó.
- owl:equivalentClass (Sintoma = ManifestacaoClinica): os dois rótulos em cada nó.
- owl:inverseOf: não há relacionamento inverso gravado; percorre-se a seta no sentido contrário.
- owl:TransitiveProperty (evoluiPara): caminho de tamanho variável `[:EVOLUI_PARA*1..2]`.
- owl:SymmetricProperty (interageCom): duas arestas, uma em cada sentido.
- Propriedades de dados: viram propriedades do nó (gravidadeSintoma virou `gravidade`).
- Não há reasoner no Memgraph: o que antes era inferido agora é explícito ou resolvido pela consulta.

## Como executar
1. `docker compose up -d` e `docker compose ps` (devem aparecer memgraph e memgraph-lab).
2. `pip install -r requirements.txt`
3. `python carga_memgraph.py` (cria a base do zero; esperado: 40 nós e 70 relacionamentos).
4. `python consultas_cypher.py`

Os updates (Parte 4) alteram a base. Para repetir a execução, rode a carga de novo antes.

Memgraph Lab: http://localhost:3000 | Bolt: bolt://localhost:7687

## Teste de persistência
`docker compose restart memgraph`, depois no Lab: `MATCH (n) RETURN count(n);` deve devolver 40.
Atenção: `docker compose down -v` apaga o volume e a base.

## Mapa de consultas MP3 → MP4
- g.triples 1.1 a 1.8 → Cypher 1.1, 1.3 a 1.8 e Travessia 2.3 (evoluiPara)
- SPARQL 2.1 → Cypher 1.2 | 2.2 → 3.1 | 2.3 → 1.9 | 2.4 → Travessias 2.1 e 2.2
- ASK 2.5 → Cypher 1.10 | CONSTRUCT 2.6 → Cypher 1.11
- Updates: 2.7 → 4.1 (SET de rótulo) | 2.8 → 4.2 (DELETE) | 2.9 → 4.3 (SET)
- Travessias com 2+ relacionamentos: 2.1, 2.2, 2.3 e 2.4

Os dados são didáticos e simplificados; não substituem orientação médica.
