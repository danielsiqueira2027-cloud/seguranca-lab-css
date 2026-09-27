# Relatório Técnico — Rotinas de Proteção e Ocultação de Dados

**Disciplina:** Confiabilidade e Segurança de Sistemas
**Repositório:** https://github.com/danielsiqueira2027-cloud/seguranca-lab-css

## 1. Objetivo

Implementar e demonstrar, em Python, três rotinas fundamentais de segurança da informação: hashing seguro de senhas, criptografia simétrica de dados sensíveis e ocultação de informação via esteganografia LSB em imagens.

## 2. Módulo de Hashing (hashing.py)

**Problema:** senhas nunca devem ser armazenadas em texto puro, pois um vazamento de banco de dados exporia diretamente as credenciais dos usuários.

**Solução:** utilizamos o algoritmo **bcrypt**, e não um hash simples (como MD5 ou SHA-256 puro), por dois motivos:

- O bcrypt é um algoritmo de **hashing adaptativo**, projetado especificamente para senhas: ele incorpora um fator de custo (`cost factor`) que torna o cálculo deliberadamente lento, dificultando ataques de força bruta e tabelas rainbow.
- O bcrypt já injeta e armazena o **salt** dentro do próprio hash resultante, eliminando a necessidade de gerenciar essa informação separadamente e garantindo que duas senhas idênticas gerem hashes diferentes.

**Fluxo implementado:**

1. `cadastrar_usuario()` gera um salt aleatório (`bcrypt.gensalt()`) e calcula o hash da senha (`bcrypt.hashpw()`).
2. `verificar_login()` usa `bcrypt.checkpw()` para comparar a senha informada com o hash salvo, sem nunca descriptografar o hash (bcrypt é unidirecional).

**Resultado do teste:** login com senha correta retornou acesso permitido; login com senha incorreta retornou acesso negado — validando que o mecanismo protege corretamente as credenciais.

## 3. Módulo de Criptografia (criptografia.py)

**Problema:** dados sensíveis (ex: financeiros) armazenados ou transmitidos precisam ser reversíveis apenas por quem possui a chave correta — diferente de senhas, que nunca precisam ser recuperadas.

**Solução:** utilizamos criptografia **simétrica** via **Fernet**, da biblioteca `cryptography`, que implementa **AES-128 em modo CBC** combinado com autenticação **HMAC-SHA256**. Essa combinação garante:

- **Confidencialidade:** o dado cifrado é ilegível sem a chave.
- **Integridade e autenticidade:** o HMAC detecta qualquer alteração no texto cifrado, prevenindo ataques de manipulação.

**Fluxo implementado:**

1. `gerar_chave()` cria uma chave simétrica de 32 bytes.
2. `cifrar_dados()` transforma o texto original em um token cifrado.
3. `decifrar_dados()` reverte o processo usando a mesma chave.

**Resultado do teste:** o dado financeiro fictício foi cifrado, transformado em um token ilegível, e corretamente recuperado ao decifrar — comprovado por `assert` de igualdade entre original e decifrado.

## 4. Módulo de Esteganografia (esteganografia.py)

**Problema:** em certos cenários, além de proteger o conteúdo de uma mensagem, é necessário ocultar a própria existência da comunicação.

**Solução:** implementamos esteganografia por **LSB (Least Significant Bit)**, manipulando o bit menos significativo do canal vermelho (R) de cada pixel de uma imagem PNG. Como esse bit tem impacto visual imperceptível na cor do pixel, a imagem permanece visualmente idêntica ao olho humano, mas carrega informação embutida a nível binário.

**Fluxo implementado:**

1. `esconder_texto()` converte o texto para binário (UTF-8) e substitui o LSB de cada pixel sequencialmente, adicionando um delimitador binário (`1111111111111110`) para marcar o fim da mensagem.
2. `extrair_texto()` varre a imagem lendo o LSB de cada pixel até encontrar o delimitador, reconstruindo os bytes e decodificando o texto original.

**Resultado do teste:** uma imagem de teste 100x100 foi gerada, uma frase foi ocultada e depois extraída com sucesso, com correspondência exata ao texto original.

## 5. Conclusão

Os três módulos demonstram, na prática, os três pilares complementares da proteção de dados: **hashing** (proteção irreversível de credenciais), **criptografia** (proteção reversível de dados sensíveis) e **esteganografia** (ocultação da própria existência da informação). Todos os testes foram executados com sucesso, validando o funcionamento correto de cada implementação.
