from cryptography.fernet import Fernet


def gerar_chave() -> bytes:
    """
    Gera uma chave criptográfica simétrica segura.
    O Fernet utiliza o algoritmo AES-128 em modo CBC com autenticação HMAC-SHA256.
    """
    return Fernet.generate_key()


def cifrar_dados(dados: str, chave: bytes) -> bytes:
    """
    Cifra uma string contendo dados confidenciais usando a chave simétrica.
    
    :param dados: Texto em claro a ser protegido.
    :param chave: Chave simétrica Fernet de 32 bytes (codificada em URL-safe base64).
    :return: Token cifrado contendo IV, texto cifrado e HMAC.
    """
    fernet = Fernet(chave)
    return fernet.encrypt(dados.encode('utf-8'))


def decifrar_dados(dados_cifrados: bytes, chave: bytes) -> str:
    """
    Decifra o token criptografado usando a chave simétrica correspondente.
    
    :param dados_cifrados: Token gerado pelo Fernet.
    :param chave: Mesma chave simétrica usada na cifragem.
    :return: Texto original em claro.
    """
    fernet = Fernet(chave)
    dados_decifrados = fernet.decrypt(dados_cifrados)
    return dados_decifrados.decode('utf-8')


if __name__ == "__main__":
    import sys
    if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("=" * 70)
    print(" DEMONSTRAÇÃO DE CRIPTOGRAFIA SIMÉTRICA (FERNET / AES)")
    print("=" * 70)

    # 1. Geração de chave simétrica
    chave = gerar_chave()
    print(f"\n[1] Chave Simétrica Gerada (Fernet/Base64):")
    print(f"    {chave.decode('utf-8')}")

    # 2. Dados financeiros sensíveis fictícios
    dados_financeiros = (
        "Titular: Roberto C. Albuquerque | "
        "Cartão: 5412 7519 8243 9012 | "
        "Validade: 11/30 | "
        "CVV: 847 | "
        "Saldo Disponível: R$ 38.450,90"
    )

    print(f"\n[2] Dado Original (Texto Claro):")
    print(f"    {dados_financeiros}")

    # 3. Cifragem dos dados
    dados_cifrados = cifrar_dados(dados_financeiros, chave)
    print(f"\n[3] Dado Cifrado (Criptograma seguro):")
    print(f"    {dados_cifrados.decode('utf-8')}")

    # 4. Decifragem dos dados com a chave correta
    dados_recuperados = decifrar_dados(dados_cifrados, chave)
    print(f"\n[4] Dado Decifrado (Recuperado com a chave correta):")
    print(f"    {dados_recuperados}")

    # 5. Validação de integridade e confidencialidade
    assert dados_financeiros == dados_recuperados, "Erro: Os dados decifrados não conferem com o original!"
    print(f"\n[5] Confirmação de Integridade:")
    print("    [SUCESSO] O texto decifrado é idêntico ao dado original.")
    print("=" * 70)
