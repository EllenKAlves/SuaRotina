from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from users import criar_perfil, obter_perfil, atualizar_perfil, listar_perfis
app = FastAPI()

# Modelos para entrada e saída
class CriarPerfilRequest(BaseModel):
    nome: str
    idade: int
    interesses: List[str]

class AtualizarPerfilRequest(BaseModel):
    idade: int = None
    interesses: List[str] = None

@app.post("/perfis")
def criar_perfil_endpoint(dados: CriarPerfilRequest):
    try:
        perfil = criar_perfil(dados.nome, dados.idade, dados.interesses)
        return perfil
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/perfis/{nome}")
def obter_perfil_endpoint(nome: str):
    try:
        perfil = obter_perfil(nome)
        return perfil
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.put("/perfis/{nome}")
def atualizar_perfil_endpoint(nome: str, dados: AtualizarPerfilRequest):
    try:
        perfil = atualizar_perfil(nome, idade=dados.idade, interesses=dados.interesses)
        return perfil
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/perfis")
def listar_perfis_endpoint():
    return listar_perfis()

#modelo de entrada
class DadosUsuario(BaseModel):
    nome: str
    idade: int
    horarios_livres: List[str]
    interesses: List[str]

#gera a rotina
def gerar_rotina(nome: str, idade: int, horarios_livres: List[str], interesses: List[str]) -> Dict:
    #estimativa de duração das att
    atividades_disponiveis = {
        "esporte": [("Corrida", 60), ("Caminhada", 30), ("Yoga", 45)],
        "arte": [("Pintura", 90), ("Tocar instrumento", 60), ("Fotografia", 30)],
        "leitura": [("Leitura de ficção", 45), ("Leitura técnica", 60)],
        "tecnologia": [("Programação", 120), ("Explorar novas ferramentas", 60)],
        "culinária": [("Aprender uma nova receita", 120), ("Cozinhar um prato saudável", 90)],
    }
    
    rotina = []
    horarios_ocupados = []  #horarios ocupados
    
    #processando td horario livre
    for horario in horarios_livres:
        #horarios  p/ min
        hora, minuto = map(int, horario.split(":"))
        minutos_inicio = hora * 60 + minuto
        
        #atividades compativeis
        for interesse in interesses:
            if interesse in atividades_disponiveis:
                for atividade, duracao in atividades_disponiveis[interesse]:
                    minutos_fim = minutos_inicio + duracao
                    
                    #checando conflitos de horarios
                    conflito = any(
                        inicio < minutos_fim and minutos_inicio < fim 
                        for inicio, fim in horarios_ocupados
                    )
                    
                    if not conflito:
                        #add att e dps ja bloqueia o horario
                        rotina.append({
                            "horario_inicio": horario,
                            "horario_fim": f"{minutos_fim // 60:02}:{minutos_fim % 60:02}",
                            "atividade": atividade
                        })
                        horarios_ocupados.append((minutos_inicio, minutos_fim))
                        break  #coloca so uma att por horario p n ter conflito
    
    return {"nome": nome, "rotina": rotina}

#rota p sugestao de rotina
@app.post("/sugestao_rotina")
def sugestao_rotina(dados: DadosUsuario):
    #validação pelo Pydantic
    if not dados.horarios_livres or not dados.interesses:
        raise HTTPException(status_code=400, detail="Horários livres ou interesses não podem estar vazios.")
   
    resultado = gerar_rotina(
        nome=dados.nome,
        idade=dados.idade,
        horarios_livres=dados.horarios_livres,
        interesses=dados.interesses
    )
    return resultado
