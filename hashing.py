import bcrypt


def cadastrar_usuario(senha: str) -> bytes:
    """
    Gera um salt aleatório e calcula o hash seguro da senha usando bcrypt.
    A senha em texto puro NUNCA deve ser armazenada em disco ou banco de dados.
    
    :param senha: Senha em texto puro informada pelo usuário.
    :return: Hash seguro contendo algoritmo, custo, salt e o hash resultante.
    """
    senha_bytes = senha.encode('utf-8')
    # Gera salt aleatório com fator de custo padrão (cost factor 12)
    salt = bcrypt.gensalt()
    # Gera o hash combinando a senha e o salt
    hash_senha = bcrypt.hashpw(senha_bytes, salt)
    return hash_senha


def verificar_login(senha: str, hash_salvo: bytes) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash armazenado usando bcrypt.checkpw().
    
    :param senha: Senha fornecida na tentativa de login.
    :param hash_salvo: Hash previamente gerado e armazenado.
    :return: True se a senha for válida, False caso contrário.
    """
    senha_bytes = senha.encode('utf-8')
    if isinstance(hash_salvo, str):
        hash_salvo = hash_salvo.encode('utf-8')
    return bcrypt.checkpw(senha_bytes, hash_salvo)


if __name__ == "__main__":
    import sys
    if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("=" * 60)
    print(" DEMONSTRAÇÃO DE HASHING SEGURO DE SENHAS (BCRYPT)")
    print("=" * 60)

    # 1. Simulação do cadastro do usuário
    usuario = "mariana.silva"
    senha_correta = "MinhaS3nh@Forte!2026"

    print(f"\n[CADASTRO] Cadastrando usuário: '{usuario}'")
    print(f"[CADASTRO] Senha informada (texto puro): '{senha_correta}'")

    hash_armazenado = cadastrar_usuario(senha_correta)
    print(f"[CADASTRO] Hash seguro gerado para armazenamento:\n  -> {hash_armazenado.decode('utf-8')}")
    print("  (Observe que o salt está embutido no próprio hash)")

    # 2. Teste de login com a senha correta
    print("\n" + "-" * 60)
    print("[TESTE 1] Tentativa de login com a SENHA CORRETA:")
    print(f"  Senha digitada: '{senha_correta}'")
    sucesso = verificar_login(senha_correta, hash_armazenado)
    print(f"  Resultado: {'ACESSO PERMITIDO (Autenticado com sucesso)' if sucesso else 'ACESSO NEGADO'}")

    # 3. Teste de login com a senha errada
    senha_errada = "SenhaErrada@123"
    print("\n" + "-" * 60)
    print("[TESTE 2] Tentativa de login com SENHA INCORRETA:")
    print(f"  Senha digitada: '{senha_errada}'")
    falha = verificar_login(senha_errada, hash_armazenado)
    print(f"  Resultado: {'ACESSO PERMITIDO' if falha else 'ACESSO NEGADO (Senha incorreta)'}")

    print("\n" + "=" * 60)
