# Laboratório de Segurança e Confiabilidade de Sistemas

Este repositório contém implementações práticas em Python demonstrando três pilares fundamentais da segurança da informação: **Hashing Seguro de Senhas**, **Criptografia Simétrica** e **Esteganografia em Imagens**.

---

## 📁 Módulos e Algoritmos

### 1. `hashing.py` — Hashing Seguro de Senhas
- **Conceito:** Armazenamento seguro de senhas através de funções hash criptográficas unidirecionais com *salt*.
- **Algoritmo / Biblioteca:** `bcrypt` (baseado no algoritmo Blowfish adaptado).
- **Características:**
  - Gera um *salt* aleatório único para cada senha (`bcrypt.gensalt()`), inviabilizando ataques baseados em tabelas pré-computadas (*Rainbow Tables*).
  - Possui fator de custo adaptável (*work factor*), tornando ataques de força bruta computacionalmente inviáveis.
  - As senhas em texto puro **nunca** são salvas; a validação é feita diretamente via `bcrypt.checkpw()`.

### 2. `criptografia.py` — Criptografia Simétrica
- **Conceito:** Garantia de confidencialidade e integridade para dados confidenciais (ex: informações financeiras).
- **Algoritmo / Biblioteca:** `Fernet` (da biblioteca `cryptography`).
- **Características:**
  - Utiliza cifra simétrica padrão **AES-128 em modo CBC** com chave de 128 bits e preenchimento PKCS7.
  - Inclui autenticação e verificação de integridade através de **HMAC-SHA256**.
  - Somente quem possui a mesma chave simétrica gerada consegue decifrar e recuperar os dados originais.

### 3. `esteganografia.py` — Esteganografia em Imagens
- **Conceito:** Ocultação da existência de uma mensagem secreta dentro de um arquivo de mídia (imagem digital).
- **Algoritmo / Biblioteca:** Esteganografia **LSB (*Least Significant Bit*)** utilizando a biblioteca `Pillow` (PIL).
- **Características:**
  - O texto é convertido em uma sequência de bits (UTF-8) e gravado no bit menos significativo do canal vermelho (*Red*) de cada pixel.
  - A alteração no valor do canal é imperceptível ao olho humano (variação de no máximo 1 unidade na intensidade).
  - Utiliza o delimitador sentinela `'1111111111111110'` ao final da sequência para indicar o término da mensagem durante a extração.
  - O formato **PNG** é mandatório por ser um formato sem perdas (*lossless*), preservando os bits exatos de cada pixel.

---

## 🚀 Como Executar

### 1. Pré-requisitos e Instalação

Certifique-se de ter o Python 3.9+ instalado. Em seguida, instale as dependências listadas no `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Executando os Scripts

Cada script possui um bloco de demonstração autocontido que valida o funcionamento das funções:

- **Teste de Hashing:**
  ```bash
  python hashing.py
  ```

- **Teste de Criptografia Simétrica:**
  ```bash
  python criptografia.py
  ```

- **Teste de Esteganografia:**
  ```bash
  python esteganografia.py
  ```