from PIL import Image

DELIMITADOR = "1111111111111110"


def esconder_texto(caminho_imagem: str, texto: str, caminho_saida: str) -> None:
    """
    Grava o texto nos bits menos significativos (LSB) do canal vermelho (R)
    de cada pixel da imagem, adicionando um delimitador de fim de mensagem.
    
    :param caminho_imagem: Caminho da imagem de entrada (deve ser compatível com PNG).
    :param texto: Texto a ser ocultado na imagem.
    :param caminho_saida: Caminho para salvar a imagem resultante com esteganografia.
    """
    # Carrega a imagem garantindo modo RGB
    img = Image.open(caminho_imagem).convert("RGB")
    largura, altura = img.size
    capacidade_maxima = largura * altura

    # Converte o texto para sequência binária UTF-8 e anexa o delimitador
    texto_bytes = texto.encode("utf-8")
    bits = "".join(f"{byte:08b}" for byte in texto_bytes) + DELIMITADOR

    if len(bits) > capacidade_maxima:
        raise ValueError(
            f"Capacidade insuficiente: a mensagem necessita de {len(bits)} pixels, "
            f"mas a imagem possui apenas {capacidade_maxima} pixels."
        )

    pixels = img.load()
    bit_idx = 0
    total_bits = len(bits)

    # Itera pelos pixels da imagem substituindo o LSB do canal vermelho
    for y in range(altura):
        for x in range(largura):
            if bit_idx < total_bits:
                r, g, b = pixels[x, y]
                bit = int(bits[bit_idx])
                # Limpa o LSB de R com (r & ~1) e insere o bit da mensagem
                novo_r = (r & ~1) | bit
                pixels[x, y] = (novo_r, g, b)
                bit_idx += 1
            else:
                break
        if bit_idx >= total_bits:
            break

    # Salva em formato PNG para evitar perda de dados por compressão
    img.save(caminho_saida, format="PNG")


def extrair_texto(caminho_imagem: str) -> str:
    """
    Varre a imagem, lê os bits menos significativos (LSB) do canal vermelho
    e reconstrói o texto original até encontrar o delimitador de fim.
    
    :param caminho_imagem: Caminho da imagem com esteganografia.
    :return: Texto decodificado a partir dos bits extraídos.
    """
    img = Image.open(caminho_imagem).convert("RGB")
    largura, altura = img.size
    pixels = img.load()

    bits_extraidos = []
    delimitador_encontrado = False
    len_delimitador = len(DELIMITADOR)

    for y in range(altura):
        for x in range(largura):
            r, _, _ = pixels[x, y]
            bits_extraidos.append(str(r & 1))

            # Verifica se os últimos bits lidos correspondem ao delimitador
            if len(bits_extraidos) >= len_delimitador:
                if "".join(bits_extraidos[-len_delimitador:]) == DELIMITADOR:
                    delimitador_encontrado = True
                    break
        if delimitador_encontrado:
            break

    if not delimitador_encontrado:
        raise ValueError("Delimitador de fim de mensagem não foi encontrado na imagem.")

    # Remove o delimitador final
    bits_mensagem = "".join(bits_extraidos[:-len_delimitador])

    # Agrupa de 8 em 8 bits para formar os bytes originais
    bytes_dados = bytearray()
    for i in range(0, len(bits_mensagem), 8):
        byte_str = bits_mensagem[i:i + 8]
        if len(byte_str) == 8:
            bytes_dados.append(int(byte_str, 2))

    return bytes_dados.decode("utf-8")


if __name__ == "__main__":
    import sys
    if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("=" * 70)
    print(" DEMONSTRAÇÃO DE ESTEGANOGRAFIA EM IMAGENS PNG (LSB)")
    print("=" * 70)

    # 1. Criação de uma imagem de teste 100x100 com gradiente de cores
    largura, altura = 100, 100
    img_teste = Image.new("RGB", (largura, altura))
    pixels_teste = img_teste.load()
    for y in range(altura):
        for x in range(largura):
            pixels_teste[x, y] = (int(x * 255 / largura), int(y * 255 / altura), 180)

    caminho_original = "teste_original.png"
    caminho_esteganografia = "teste_esteganografia.png"
    img_teste.save(caminho_original, format="PNG")
    print(f"\n[1] Imagem de teste criada: '{caminho_original}' ({largura}x{altura} pixels)")

    # 2. Definição da mensagem secreta
    mensagem_secreta = (
        "Operação Confidencial 2026: Dados protegidos via Esteganografia LSB no canal R."
    )
    print(f"\n[2] Mensagem Secreta a ser ocultada:")
    print(f"    '{mensagem_secreta}'")

    # 3. Ocultação da mensagem na imagem
    esconder_texto(caminho_original, mensagem_secreta, caminho_esteganografia)
    print(f"\n[3] Mensagem escondida com sucesso em: '{caminho_esteganografia}'")
    print(f"    (Delimitador utilizado: '{DELIMITADOR}')")

    # 4. Extração e reconstrução da mensagem
    texto_recuperado = extrair_texto(caminho_esteganografia)
    print(f"\n[4] Texto extraído da imagem:")
    print(f"    '{texto_recuperado}'")

    # 5. Validação
    assert mensagem_secreta == texto_recuperado, "Erro: O texto recuperado é diferente do original!"
    print(f"\n[5] Validação de Correspondência:")
    print("    [SUCESSO] O texto extraído corresponde exatamente à mensagem secreta original!")
    print("=" * 70)
