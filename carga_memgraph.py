from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("", "")

def carregar_base():
    driver = GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as session:
        # 1. Limpa a base anterior
        session.run("MATCH (n) DETACH DELETE n")
        print("Base limpa no Memgraph. Iniciando carga do Grafo de Propriedades...")

        # 2. Criação de Agentes Patogênicos
        session.run("""
            CREATE (:AgentePatogenico {id: 'virusDengue', nome: 'Vírus da Dengue (DENV)'}),
                   (:AgentePatogenico {id: 'virusInfluenza', nome: 'Vírus Influenza A (H1N1)'}),
                   (:AgentePatogenico {id: 'virusSarsCov2', nome: 'Coronavírus SARS-CoV-2'}),
                   (:AgentePatogenico {id: 'baciloKoch', nome: 'Bacilo de Koch (Mycobacterium tuberculosis)'}),
                   (:AgentePatogenico {id: 'meningococo', nome: 'Meningococo (Neisseria meningitidis)'}),
                   (:AgentePatogenico {id: 'pneumococo', nome: 'Pneumococo (Streptococcus pneumoniae)'})
        """)

        # 3. Criação de Sintomas / Manifestações Clínicas
        session.run("""
            CREATE (:Sintoma:ManifestacaoClinica {id: 'febreAlta', nome: 'Febre Alta', gravidade: 'Moderada'}),
                   (:Sintoma:ManifestacaoClinica {id: 'cefaleia', nome: 'Cefaleia (Dor de Cabeça)', gravidade: 'Leve'}),
                   (:Sintoma:ManifestacaoClinica {id: 'mialgia', nome: 'Mialgia (Dor Muscular)', gravidade: 'Moderada'}),
                   (:Sintoma:ManifestacaoClinica {id: 'anosmia', nome: 'Anosmia (Perda de Olfato)', gravidade: 'Leve'}),
                   (:Sintoma:ManifestacaoClinica {id: 'dispneia', nome: 'Dispneia (Falta de Ar)', gravidade: 'Alta'}),
                   (:Sintoma:ManifestacaoClinica {id: 'tosseSeca', nome: 'Tosse Seca Persistente', gravidade: 'Leve'}),
                   (:Sintoma:ManifestacaoClinica {id: 'hemorragia', nome: 'Hemorragia Mucosa', gravidade: 'Crítica'}),
                   (:Sintoma:ManifestacaoClinica {id: 'rigidezNuca', nome: 'Rigidez na Nuca', gravidade: 'Crítica'})
        """)

        # 4. Criação de Medicamentos e Terapias de Suporte
        session.run("""
            CREATE (:Medicamento:Tratamento {id: 'paracetamol', nome: 'Paracetamol', dosagemMg: 750}),
                   (:Medicamento:Tratamento {id: 'dipirona', nome: 'Dipirona Sódica', dosagemMg: 500}),
                   (:Medicamento:Tratamento {id: 'oseltamivir', nome: 'Oseltamivir (Tamiflu)', dosagemMg: 75}),
                   (:Medicamento:Tratamento {id: 'amoxicilina', nome: 'Amoxicilina', dosagemMg: 500}),
                   (:Medicamento:Tratamento {id: 'rifampicina', nome: 'Rifampicina', dosagemMg: 600}),
                   (:Medicamento:Tratamento {id: 'ceftriaxona', nome: 'Ceftriaxona', dosagemMg: 1000}),
                   (:Medicamento:Tratamento {id: 'losartana', nome: 'Losartana Potássica', dosagemMg: 50}),
                   (:Medicamento:Tratamento {id: 'ibuprofeno', nome: 'Ibuprofeno', dosagemMg: 400}),
                   (:TerapiaSuporte:Tratamento {id: 'hidratacaoVenosa', nome: 'Hidratação Venosa Intensiva'}),
                   (:TerapiaSuporte:Tratamento {id: 'oxigenoterapia', nome: 'Oxigenoterapia por Cateter Nasal'})
        """)

        # 5. Criação de Doenças
        session.run("""
            CREATE (:Doenca:DoencaInfecciosa:DoencaViral {id: 'dengueClassica', nome: 'Dengue Clássica', codigoCID: 'A90', taxaLetalidade: 0.5, periodoIncubacaoDias: 6}),
                   (:Doenca:DoencaInfecciosa:DoencaViral {id: 'dengueAlarme', nome: 'Dengue com Sinais de Alarme', codigoCID: 'A90', taxaLetalidade: 2.5, periodoIncubacaoDias: 6}),
                   (:Doenca:DoencaInfecciosa:DoencaViral {id: 'dengueGrave', nome: 'Dengue Grave (Hemorrágica)', codigoCID: 'A91', taxaLetalidade: 12.0, periodoIncubacaoDias: 6}),
                   (:Doenca:DoencaInfecciosa:DoencaViral {id: 'influenzaA', nome: 'Gripe Influenza A', codigoCID: 'J09', taxaLetalidade: 1.2, periodoIncubacaoDias: 3}),
                   (:Doenca:DoencaInfecciosa:DoencaViral {id: 'covid19', nome: 'COVID-19', codigoCID: 'U07.1', taxaLetalidade: 2.8, periodoIncubacaoDias: 5}),
                   (:Doenca:DoencaInfecciosa:DoencaBacteriana {id: 'tuberculose', nome: 'Tuberculose Pulmonar', codigoCID: 'A15', taxaLetalidade: 7.5, periodoIncubacaoDias: 30}),
                   (:Doenca:DoencaInfecciosa:DoencaBacteriana {id: 'pneumoniaBacteriana', nome: 'Pneumonia Bacteriana Aguda', codigoCID: 'J15', taxaLetalidade: 5.4, periodoIncubacaoDias: 4}),
                   (:Doenca:DoencaInfecciosa:DoencaBacteriana {id: 'meningiteBacteriana', nome: 'Meningite Meningocócica', codigoCID: 'A39.0', taxaLetalidade: 18.5, periodoIncubacaoDias: 4}),
                   (:Doenca:DoencaCronica {id: 'hipertensao', nome: 'Hipertensão Arterial Sistêmica', codigoCID: 'I10', taxaLetalidade: 0.4}),
                   (:Doenca:DoencaCronica {id: 'asmaGrave', nome: 'Asma Brônquica Grave', codigoCID: 'J45', taxaLetalidade: 0.8})
        """)

        # 6. Criação de Médicos e Pacientes
        session.run("""
            CREATE (:Medico:Pessoa {id: 'med_helena', nome: 'Dra. Helena Vasconcelos (Infectologista)'}),
                   (:Medico:Pessoa {id: 'med_carlos', nome: 'Dr. Carlos Eduardo (Clínico Geral)'}),
                   (:Paciente:Pessoa {id: 'pac_lucas', nome: 'Lucas Andrade', idadePaciente: 24, statusClinico: 'Em Triagem'}),
                   (:Paciente:Pessoa {id: 'pac_mariana', nome: 'Mariana Costa', idadePaciente: 68, statusClinico: 'Em Triagem'}),
                   (:Paciente:Pessoa {id: 'pac_roberto', nome: 'Roberto Almeida', idadePaciente: 55, statusClinico: 'Em Triagem'}),
                   (:Paciente:Pessoa {id: 'pac_clara', nome: 'Clara Nogueira', idadePaciente: 31, statusClinico: 'Em Observação'})
        """)

        # 7. Criação dos Relacionamentos (um comando por execução)
        rel_causada_por = [
            ("dengueClassica", "virusDengue"),
            ("dengueAlarme", "virusDengue"),
            ("dengueGrave", "virusDengue"),
            ("influenzaA", "virusInfluenza"),
            ("covid19", "virusSarsCov2"),
            ("tuberculose", "baciloKoch"),
            ("pneumoniaBacteriana", "pneumococo"),
            ("meningiteBacteriana", "meningococo"),
        ]
        for doenca_id, agente_id in rel_causada_por:
            session.run("""
                MATCH (d:Doenca {id: $d_id}), (a:AgentePatogenico {id: $a_id})
                CREATE (d)-[:CAUSADA_POR]->(a)
            """, d_id=doenca_id, a_id=agente_id)

        rel_sintomas = [
            ("dengueClassica", ["febreAlta", "cefaleia", "mialgia"]),
            ("dengueAlarme", ["febreAlta", "cefaleia", "mialgia", "hemorragia"]),
            ("dengueGrave", ["febreAlta", "hemorragia", "dispneia"]),
            ("influenzaA", ["febreAlta", "tosseSeca", "mialgia", "cefaleia"]),
            ("covid19", ["febreAlta", "tosseSeca", "dispneia", "cefaleia"]),
            ("tuberculose", ["tosseSeca", "febreAlta", "dispneia"]),
            ("pneumoniaBacteriana", ["febreAlta", "dispneia", "tosseSeca"]),
            ("meningiteBacteriana", ["febreAlta", "cefaleia", "rigidezNuca"]),
            ("hipertensao", ["cefaleia"]),
            ("asmaGrave", ["dispneia", "tosseSeca"]),
        ]
        for doenca_id, sintomas_ids in rel_sintomas:
            session.run("""
                MATCH (d:Doenca {id: $d_id}), (s:Sintoma)
                WHERE s.id IN $s_ids
                CREATE (d)-[:APRESENTA_SINTOMA]->(s)
            """, d_id=doenca_id, s_ids=sintomas_ids)

        rel_tratamentos = [
            ("dengueClassica", ["paracetamol", "dipirona", "hidratacaoVenosa"]),
            ("dengueAlarme", ["hidratacaoVenosa", "dipirona"]),
            ("dengueGrave", ["hidratacaoVenosa", "oxigenoterapia"]),
            ("influenzaA", ["oseltamivir", "paracetamol"]),
            ("covid19", ["dipirona", "oxigenoterapia"]),
            ("tuberculose", ["rifampicina"]),
            ("pneumoniaBacteriana", ["amoxicilina", "oxigenoterapia"]),
            ("meningiteBacteriana", ["ceftriaxona", "hidratacaoVenosa"]),
            ("hipertensao", ["losartana"]),
            ("asmaGrave", ["oxigenoterapia"]),
        ]
        for doenca_id, trat_ids in rel_tratamentos:
            session.run("""
                MATCH (d:Doenca {id: $d_id}), (t:Tratamento)
                WHERE t.id IN $t_ids
                CREATE (d)-[:TRATADA_COM]->(t)
            """, d_id=doenca_id, t_ids=trat_ids)

        # Progressão clínica e interações medicamentosas (ambos os sentidos para simetria explícita no LPG)
        evolucoes = [("dengueClassica", "dengueAlarme"), ("dengueAlarme", "dengueGrave")]
        for origem, destino in evolucoes:
            session.run("""
                MATCH (d1:Doenca {id: $o}), (d2:Doenca {id: $d})
                CREATE (d1)-[:EVOLUI_PARA]->(d2)
            """, o=origem, d=destino)

        interacoes = [("paracetamol", "rifampicina"), ("losartana", "ibuprofeno")]
        for m1, m2 in interacoes:
            session.run("""
                MATCH (a:Medicamento {id: $m1}), (b:Medicamento {id: $m2})
                CREATE (a)-[:INTERAGE_COM]->(b), (b)-[:INTERAGE_COM]->(a)
            """, m1=m1, m2=m2)

        # Atendimentos e Diagnósticos
        atendimentos = [
            ("pac_lucas", "dengueClassica", "med_helena"),
            ("pac_mariana", "meningiteBacteriana", "med_helena"),
            ("pac_roberto", "tuberculose", "med_carlos"),
            ("pac_clara", "hipertensao", "med_carlos"),
        ]
        for pac_id, doenca_id, med_id in atendimentos:
            session.run("""
                MATCH (p:Paciente {id: $p_id}), (d:Doenca {id: $d_id}), (m:Medico {id: $m_id})
                CREATE (p)-[:DIAGNOSTICADO_COM]->(d), (p)-[:ATENDIDO_POR]->(m)
            """, p_id=pac_id, d_id=doenca_id, m_id=med_id)

        session.run("MATCH (n) WHERE n:AgentePatogenico OR n:Doenca OR n:Sintoma OR n:Tratamento SET n:EntidadeSaude")
        res_nos = session.run("MATCH (n) RETURN count(n) AS total_nos").single()["total_nos"]
        res_rels = session.run("MATCH ()-[r]->() RETURN count(r) AS total_rels").single()["total_rels"]
        print(f"Carga concluída com sucesso no Memgraph! Nós criados: {res_nos} | Relacionamentos criados: {res_rels}")

if __name__ == "__main__":
    carregar_base()
