from typing import List, Dict

#"bd" em memoria
usuarios = {}

def criar_perfil(nome: str, 
                 idade: int, 
                 interesses: List[str]) -> Dict:
    """
    Cria um perfil de usuário e armazena no banco de dados em memória.
    """
    if nome in usuarios:
        raise ValueError(f"Já existe um perfil com o nome '{nome}'.")
    
    #dados do usuario
    perfil = {
        "nome": nome,
        "idade": idade,
        "interesses": interesses
    }
    usuarios[nome] = perfil
    return perfil

def obter_perfil(nome: str) -> Dict:
    """
    Retorna o perfil de um usuário pelo nome.
    """
    perfil = usuarios.get(nome)
    if not perfil:
        raise ValueError(f"Perfil com o nome '{nome}' não encontrado.")
    return perfil

def atualizar_perfil(nome: str, idade: int = None, interesses: List[str] = None) -> Dict:
    """
    Atualiza informações do perfil de um usuário existente.
    """
    if nome not in usuarios:
        raise ValueError(f"Perfil com o nome '{nome}' não encontrado.")
    
    perfil = usuarios[nome]
    if idade is not None:
        perfil["idade"] = idade
    if interesses is not None:
        perfil["interesses"] = interesses
    
    usuarios[nome] = perfil
    return perfil

def listar_perfis() -> List[Dict]:
    """
    Lista todos os perfis de usuários cadastrados.
    """
    return list(usuarios.values())
