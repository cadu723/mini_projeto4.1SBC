from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("", "")

def separar_secao(titulo):
    print("\n" + "=" * 85)
    print(f" {titulo}")
    print("=" * 85)

def executar_consultas():
    driver = GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as session:

        # =====================================================================
        # PARTE 1: CONSULTAS DIRETAS E FILTRAGEM
        # =====================================================================
        separar_secao("PARTE 1: CONSULTAS DIRETAS E FILTRAGEM EM CYPHER")

        print("\n[Cypher 1.1] Sintomas apresentados pela Dengue Clássica:")
        res1 = session.run("MATCH (d:Doenca {id: 'dengueClassica'})-[:APRESENTA_SINTOMA]->(s) RETURN s.nome AS sintoma")
        for r in res1:
            print(f"  -> {r['sintoma']}")

        print("\n[Cypher 1.2] Doenças com letalidade superior a 2.0% (ORDER BY DESC):")
        res2 = session.run("""
            MATCH (d:Doenca)
            WHERE d.taxaLetalidade > 2.0
            RETURN d.nome AS nome, d.codigoCID AS cid, d.taxaLetalidade AS letalidade
            ORDER BY letalidade DESC
        """)
        for r in res2:
            print(f"  -> {r['nome']} (CID: {r['cid']}) | Letalidade: {r['letalidade']}%")

        # =====================================================================
        #  DEMAIS CONSULTAS DO MP3 REESCRITAS EM CYPHER (somente leitura)
        # =====================================================================
        separar_secao("PARTE 1B: DEMAIS CONSULTAS DO MP3 EM CYPHER")

        print("\n[Cypher 1.3] (MP3 1.2) Doenças que apresentam Dispneia:")
        res = session.run("""
            MATCH (d:Doenca)-[:APRESENTA_SINTOMA]->(:Sintoma {id: 'dispneia'})
            RETURN d.nome AS doenca ORDER BY doenca
        """)
        for r in res:
            print(f"  -> {r['doenca']}")

        print("\n[Cypher 1.4] (MP3 1.3) 'Febre Alta' é sintoma de quais doenças? (seta percorrida no sentido contrário):")
        res = session.run("""
            MATCH (:Sintoma {id: 'febreAlta'})<-[:APRESENTA_SINTOMA]-(d:Doenca)
            RETURN d.nome AS doenca ORDER BY doenca
        """)
        for r in res:
            print(f"  -> {r['doenca']}")

        print("\n[Cypher 1.5] (MP3 1.5) Ficha da Rifampicina (propriedades, rótulos e relacionamentos):")
        r = session.run("""
            MATCH (m:Medicamento {id: 'rifampicina'})
            OPTIONAL MATCH (m)<-[:TRATADA_COM]-(d:Doenca)
            OPTIONAL MATCH (m)-[:INTERAGE_COM]-(o:Medicamento)
            RETURN m.nome AS nome, m.dosagemMg AS dosagem, labels(m) AS rotulos,
                   collect(DISTINCT d.nome) AS indicadaPara, collect(DISTINCT o.nome) AS interageCom
        """).single()
        print(f"  -> Nome: {r['nome']} | Dosagem: {r['dosagem']} mg")
        print(f"  -> Rótulos: {', '.join(r['rotulos'])}")
        print(f"  -> Indicada para: {', '.join(r['indicadaPara'])}")
        print(f"  -> Interage com: {', '.join(r['interageCom'])}")

        print("\n[Cypher 1.6] (MP3 1.6) Todas as doenças (a hierarquia aparece nos rótulos do nó):")
        res = session.run("MATCH (d:Doenca) RETURN d.nome AS nome, labels(d) AS rotulos ORDER BY nome")
        for r in res:
            print(f"  -> {r['nome']} | Rótulos: {', '.join(r['rotulos'])}")

        print("\n[Cypher 1.7] (MP3 1.7) Todos os sintomas:")
        res = session.run("MATCH (s:Sintoma) RETURN s.nome AS nome ORDER BY nome")
        for r in res:
            print(f"  -> {r['nome']}")

        print("\n[Cypher 1.8] (MP3 1.8) O que aponta para o Vírus da Dengue, e por qual relacionamento:")
        res = session.run("""
            MATCH (x)-[r]->(:AgentePatogenico {id: 'virusDengue'})
            RETURN x.nome AS origem, type(r) AS relacao ORDER BY origem
        """)
        for r in res:
            print(f"  -> {r['origem']} --[{r['relacao']}]--> Vírus da Dengue")

        print("\n[Cypher 1.9] (MP3 2.3) Doenças, agente etiológico (opcional) e classificação de risco:")
        res = session.run("""
            MATCH (d:Doenca)
            OPTIONAL MATCH (d)-[:CAUSADA_POR]->(a:AgentePatogenico)
            RETURN d.nome AS doenca,
                   coalesce(a.nome, 'Sem agente infeccioso registrado (doença crônica)') AS agente,
                   d.taxaLetalidade AS letalidade,
                   CASE WHEN d.taxaLetalidade >= 5.0 THEN 'ALTO RISCO' ELSE 'RISCO MODERADO/BAIXO' END AS risco
            ORDER BY letalidade DESC
        """)
        for r in res:
            print(f"  -> {r['doenca']} | Patógeno: {r['agente']} | [{r['risco']}]")

        print("\n[Cypher 1.10] (MP3 2.5, ASK) Existe interação entre Ibuprofeno e Losartana? (Cypher não tem ASK: usa-se count(*) > 0)")
        res = session.run("""
            MATCH (:Medicamento {id: 'ibuprofeno'})-[:INTERAGE_COM]-(:Medicamento {id: 'losartana'})
            RETURN count(*) > 0 AS interage
        """)
        print(f"  -> {res.single()['interage']}")

        print("\n[Cypher 1.11] (MP3 2.6, CONSTRUCT) Prescrições derivadas (Paciente -> Doença -> Tratamento) como relações diretas:")
        res = session.run("""
            MATCH (p:Paciente)-[:DIAGNOSTICADO_COM]->(:Doenca)-[:TRATADA_COM]->(t:Tratamento)
            RETURN p.nome AS paciente, t.nome AS tratamento ORDER BY paciente, tratamento
        """)
        for r in res:
            print(f"  -> {r['paciente']} --[PRESCRICAO_SUGERIDA]--> {r['tratamento']}")

        # =====================================================================
        # PARTE 2: TRAVESSIAS NO GRAFO (4+ Consultas com 2 ou mais relacionamentos encadeados)
        # =====================================================================
        separar_secao("PARTE 2: TRAVESSIAS NO GRAFO (MÚLTIPLOS RELACIONAMENTOS ENCADEADOS)")

        # Travessia 2.1 (2 saltos encadeados): Paciente -> DiagnosticadoCom -> Doença -> TratadaCom -> Tratamento
        print("\n[Travessia 2.1 - 2 saltos] Prontuário: Paciente -> Doença diagnosticada -> Tratamentos recomendados:")
        res3 = session.run("""
            MATCH (p:Paciente)-[:DIAGNOSTICADO_COM]->(d:Doenca)-[:TRATADA_COM]->(t:Tratamento)
            RETURN p.nome AS paciente, d.nome AS doenca, t.nome AS tratamento
            ORDER BY paciente
        """)
        for r in res3:
            print(f"  -> {r['paciente']} ({r['doenca']}) -> Conduta: {r['tratamento']}")

        # Travessia 2.2 (Multi-caminho): Paciente -> AtendidoPor -> Médico e Paciente -> DiagnosticadoCom -> Doença -> CausadaPor -> Agente
        print("\n[Travessia 2.2 - Multi-caminho] Relacionando Paciente, Médico Responsável e Agente Etiológico:")
        res4 = session.run("""
            MATCH (p:Paciente)-[:ATENDIDO_POR]->(m:Medico),
                  (p)-[:DIAGNOSTICADO_COM]->(d:Doenca)-[:CAUSADA_POR]->(a:AgentePatogenico)
            RETURN p.nome AS paciente, m.nome AS medico, d.nome AS doenca, a.nome AS agente
        """)
        for r in res4:
            print(f"  -> Paciente: {r['paciente']} | Médico: {r['medico']} | Doença: {r['doenca']} | Patógeno: {r['agente']}")

        # Travessia 2.3 (Caminho de comprimento variável / Transitividade): [:EVOLUI_PARA*1..2]
        print("\n[Travessia 2.3 - Caminho Variável] Cadeias de progressão clínica das doenças:")
        res5 = session.run("""
            MATCH path = (d1:Doenca)-[:EVOLUI_PARA*1..2]->(d2:Doenca)
            RETURN d1.nome AS origem, nodes(path) AS nos
        """)
        for r in res5:
            cadeia = [no["nome"] for no in r["nos"]]
            print(f"  -> Origem: {r['origem']} | Progressão: {' ==> '.join(cadeia)}")

        # Travessia 2.4 (Rede de interações cruzadas): Medicamento -> InterageCom -> Outro Medicamento <- TratadaCom <- Doença
        print("\n[Travessia 2.4 - Rede de Interações] Medicamento, sua interação e doenças afetadas:")
        res6 = session.run("""
            MATCH (m1:Medicamento)-[:INTERAGE_COM]->(m2:Medicamento)<-[:TRATADA_COM]-(d:Doenca)
            RETURN m1.nome AS remedio1, m2.nome AS remedio2, d.nome AS doencaAfetada
        """)
        for r in res6:
            print(f"  -> {r['remedio1']} interage com {r['remedio2']} (usada no tratamento da {r['doencaAfetada']})")

        # =====================================================================
        # PARTE 3: AGREGAÇÃO E TRIAGEM (Estilo MYCIN)
        # =====================================================================
        separar_secao("PARTE 3: TRIAGEM E AGREGAÇÃO EM CYPHER")

        print("\n[Cypher 3.1 - Triagem MYCIN] Paciente relata Febre Alta, Cefaleia e Mialgia:")
        res7 = session.run("""
            MATCH (d:Doenca)-[:APRESENTA_SINTOMA]->(s:Sintoma)
            WHERE s.id IN ['febreAlta', 'cefaleia', 'mialgia']
            WITH d, COUNT(s) AS sintomasCasados
            WHERE sintomasCasados >= 2
            RETURN d.nome AS doenca, sintomasCasados
            ORDER BY sintomasCasados DESC
        """)
        for r in res7:
            print(f"  -> Hipótese: {r['doenca']} ({r['sintomasCasados']} sintomas coincidentes)")

        # =====================================================================
        # PARTE 4: ATUALIZAÇÕES (UPDATES) COM EFEITO VISÍVEL NA SAÍDA
        # =====================================================================
        separar_secao("PARTE 4: ATUALIZAÇÕES (UPDATES) E TRANSAÇÕES")

        # Update 4.1: INSERT de rótulo dinâmico (Regra de Triagem Crítica para letalidade >= 5.0%)
        print("\n[Cypher Update 4.1] Promovendo pacientes graves a :PacienteTriagemCritica:")
        print("Status ANTES do update:")
        res_antes = session.run("MATCH (p:Paciente)-[:DIAGNOSTICADO_COM]->(d:Doenca) RETURN p.nome AS nome, d.taxaLetalidade AS let")
        for r in res_antes:
            print(f"  -> {r['nome']} (Letalidade da doença: {r['let']}%)")

        session.run("""
            MATCH (p:Paciente)-[:DIAGNOSTICADO_COM]->(d:Doenca)
            WHERE d.taxaLetalidade >= 5.0
            SET p:PacienteTriagemCritica
        """)

        print("\nStatus DEPOIS do update (Pacientes marcados como críticos):")
        res8 = session.run("MATCH (p:PacienteTriagemCritica) RETURN p.nome AS critico")
        for r in res8:
            print(f"  -> Identificado como Crítico: {r['critico']}")

        # Update 4.2: DELETE de relacionamento (Revisão de protocolo clínico)
        print("\n[Cypher Update 4.2] Removendo indicação de Paracetamol para a Dengue Clássica:")
        antes_trat = session.run("""
            MATCH (d:Doenca {id: 'dengueClassica'})-[:TRATADA_COM]->(t:Tratamento)
            RETURN t.nome AS tratamento
        """)
        print("Tratamentos ANTES do DELETE:", [r['tratamento'] for r in antes_trat])

        session.run("""
            MATCH (d:Doenca {id: 'dengueClassica'})-[r:TRATADA_COM]->(t:Tratamento {id: 'paracetamol'})
            DELETE r
        """)

        depois_trat = session.run("""
            MATCH (d:Doenca {id: 'dengueClassica'})-[:TRATADA_COM]->(t:Tratamento)
            RETURN t.nome AS tratamento
        """)
        print("Tratamentos DEPOIS do DELETE:", [r['tratamento'] for r in depois_trat])

        # Update 4.3: SET (Transição de status clínico de triagem para tratamento supervisionado)
        print("\n[Cypher Update 4.3] Atualizando status de pacientes em triagem para Tratamento Supervisionado:")
        print("Status ANTES do update:")
        for r in session.run("MATCH (p:Paciente) RETURN p.nome AS nome, p.statusClinico AS status ORDER BY nome"):
            print(f"  -> {r['nome']}: {r['status']}")
        print("Status DEPOIS do update:")
        session.run("""
            MATCH (p:Paciente {statusClinico: 'Em Triagem'})-[:ATENDIDO_POR]->(:Medico)
            SET p.statusClinico = 'Em Tratamento Supervisionado'
        """)
        res9 = session.run("MATCH (p:Paciente) RETURN p.nome AS nome, p.statusClinico AS status")
        for r in res9:
            print(f"  -> Paciente: {r['nome']} | Status Atualizado: {r['status']}")

if __name__ == "__main__":
    executar_consultas()
