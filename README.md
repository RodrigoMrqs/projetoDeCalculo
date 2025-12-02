# Sistema de Otimização de Lucros para Agricultura Familiar

## Sobre o Projeto

Sistema web full stack desenvolvido para auxiliar pequenos agricultores familiares na tomada de decisão sobre qual cultura plantar para maximizar seus lucros, utilizando **cálculo diferencial** e **modelagem matemática**.

O projeto foi desenvolvido como trabalho acadêmico para a disciplina de **Resolução Diferencial de Problemas** do curso de Ciência da Computação do Centro Universitário do Estado do Pará (CESUPA).

### Objetivo

Aplicar conceitos de **derivadas**, **pontos críticos** e **otimização matemática** para resolver um problema real da agricultura familiar brasileira: a dificuldade de identificar qual cultura oferece maior rentabilidade dado um tamanho de área disponível.

---

## Fundamentação Científica

Este sistema é baseado no artigo científico:

**Título:** "Otimização da produtividade agrícola e altos lucros em pequenas propriedades: uma abordagem integrada de modelagem matemática e agricultura familiar"

**Autores:** Silva, C. M. et al.

**Publicação:** Revista Caderno Pedagógico, v.21, n.3, p. 01-24, 2024.

**Link:** [DOI: 10.54033/cadpedv21n3-094](https://doi.org/10.54033/cadpedv21n3-094)

### Dados Extraídos do Artigo

O artigo apresenta um estudo de caso em uma propriedade rural de 5 hectares em Mari-PB, com cultivo de:

- **Milho:** Lucro de R$ 70.262,27/ano
- **Feijão:** Lucro de R$ 40.593,61/ano
- **Macaxeira:** Lucro de R$ 77.468,64/ano
- **Batata-doce:** Lucro de R$ 75.692,15/ano

---

## Modelagem Matemática

### Função Objetivo

O sistema utiliza um modelo de **lucro quadrático** com rendimentos marginais decrescentes:

```
L(x) = ax - bx²
```

**Onde:**
- `L(x)` = Lucro esperado em função da área x (em hectares)
- `a` = Lucro por hectare (extraído do artigo)
- `b` = θ × a (coeficiente de rendimentos decrescentes)
- `θ` = Parâmetro ajustável (padrão: 0.05)

### Otimização por Derivadas

**1. Primeira Derivada (Condição Necessária):**
```
L'(x) = a - 2bx
```

**2. Ponto Crítico (L'(x) = 0):**
```
x* = a / (2b)
```

**3. Segunda Derivada (Condição Suficiente):**
```
L''(x) = -2b < 0  ⟹  x* é um MÁXIMO
```

**4. Lucro Máximo:**
```
L(x*) = a·x* - b·(x*)²
L(x*) = a² / (4b)
```

### Interpretação

- O ponto ótimo `x*` representa a **área ideal** para maximizar o lucro
- Quando `L''(x) < 0`, confirmamos que é um **ponto de máximo**
- Para áreas maiores que `x*`, os rendimentos decrescentes começam a reduzir o lucro

---

### Como o Sistema Resolve

O sistema oferece:

✅ **Recomendação clara:** Qual cultura plantar para maximizar lucro
✅ **Justificativa matemática:** Cálculos transparentes com derivadas
✅ **Comparação visual:** Gráficos intuitivos de lucros esperados
✅ **Análise de cenários:** Simulação com diferentes áreas e parâmetros
✅ **Histórico:** Registro de simulações anteriores

### 📈 Métricas de Sucesso

- Aumentar lucro em **15-25%** através de decisões baseadas em dados
- Reduzir incerteza na escolha de culturas
- Fornecer dados concretos para planejamento financeiro
- Facilitar acesso a crédito rural com projeções fundamentadas

### Impacto Esperado

- **Econômico:** Aumento de renda familiar
- **Social:** Permanência no campo com dignidade
- **Educacional:** Democratização de ferramentas de otimização
- **Regional:** Fortalecimento da agricultura familiar

---

## Arquitetura do Sistema

### Stack Tecnológica

#### Backend
- **Python 3.12+**
- **Flask** 
- **SQLite** 
- **SymPy** 
- **NumPy** 
- **Matplotlib + Seaborn** 

#### Frontend
- **HTML5 + CSS3**
- **Jinja2**
- Design responsivo

## Instalação e Execução

### Pré-requisitos

- Python 3.12 ou superior
- pip (gerenciador de pacotes Python)
- Navegador web moderno

### Passo 1: Clone/Download do Projeto

```bash
# Via Git
git clone https://github.com/seu-usuario/projetoDeCalculo.git
cd projetoDeCalculo

# OU baixe o ZIP e extraia
```

### Passo 2: Crie um Ambiente Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instale as Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Execute a Aplicação

```bash
python app.py
```

### Passo 5: Acesse no Navegador

Abra seu navegador e acesse:

```
http://127.0.0.1:5000/
```

---

## Como Usar

### Tela Inicial

Na tela inicial você verá:
- **Dados padrão** extraídos do artigo científico
- **Formulário** com dois parâmetros ajustáveis:
  - **Área total disponível (ha):** Tamanho da propriedade em hectares
  - **Theta (θ):** Coeficiente de rendimentos decrescentes (0.01 a 0.10)

### Ajuste os Parâmetros

**Área Total (A):**
- Valor padrão: 5 hectares
- Insira a área disponível em sua propriedade
- Exemplo: 3.5 hectares

**Theta (θ):**
- Valor padrão: 0.05
- Valores menores (0.01-0.03): Rendimentos decrescem lentamente
- Valores maiores (0.07-0.10): Rendimentos decrescem rapidamente
- Recomendado: Manter entre 0.04 e 0.06

### Clique em "Rodar Modelo"

O sistema irá:
1. Calibrar os parâmetros matemáticos
2. Calcular lucros para cada cultura
3. Aplicar derivadas para encontrar pontos ótimos
4. Gerar gráficos comparativos
5. Salvar o cenário no banco de dados

### Analise os Resultados

**Recomendação Principal:**
- Nome da cultura mais lucrativa
- Lucro estimado em R$

**Tabela de Análise Matemática:**
- Ponto ótimo (x*) para cada cultura
- Lucro ótimo L(x*)
- Segunda derivada L''(x*)
- Classificação (Máximo/Mínimo)
- Lucro na área A especificada

**Gráficos:**
- **Gráfico de barras:** Compara lucros entre culturas
- **Gráfico de otimização:** Mostra a função L(x) e o ponto ótimo

**Análise SymPy:**
- Derivadas simbólicas
- Pontos críticos
- Classificação matemática

**Histórico:**
- Últimas 10 simulações realizadas

### Realize Novas Simulações

- Clique em "Nova Simulação" para testar outros cenários
- Experimente diferentes valores de área e theta
- Compare os resultados no histórico

---

## Validação por artigo

**Entradas:**
- Área: 5 ha
- Theta: 0.05

**Resultado Esperado:**
- **Melhor cultura:** Macaxeira
- **Lucro estimado:** R$ 77391.17
- **Ponto ótimo:** x* = 500 ha

**Interpretação:** 
Para 1 hectares, a macaxeira oferece o melhor retorno. No entanto, o ponto ótimo seria em 500 ha, indicando que há espaço para expansão se houver terra disponível.

**Dados do artigo**
  - **Lucro estimado:** R$ 77468.64

**Conclusão**
Devido as limitações do software e de inconsistencias com a variavel theta = 0, foi realizado o teste que mais se aproxima dos dados presentes no artigo, tendo um erro de 0.1%

---
## Estrutura do Banco de Dados

### Tabela: scenarios

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER | Chave primária (auto-incremento) |
| `created_at` | TIMESTAMP | Data/hora da simulação |
| `area` | REAL | Área total em hectares |
| `theta` | REAL | Coeficiente theta utilizado |
| `profits` | TEXT | JSON com lucros por cultura |
| `best` | TEXT | Nome da melhor cultura |

### Exemplo de Registro

```json
{
  "id": 1,
  "created_at": "2024-12-02 15:30:45",
  "area": 5.0,
  "theta": 0.05,
  "profits": {
    "Milho": 316181.215,
    "Feijao": 182720.743,
    "Macaxeira": 348707.88,
    "Batata-doce": 340765.675
  },
  "best": "Macaxeira"
}
```

---

## Tratamento de Erros

### Erros Comuns e Soluções

**1. `TemplateNotFound: index.html`**

**Problema:** Arquivos HTML não estão na pasta `templates/`

**Solução:**
```bash
mkdir templates
move index.html templates/
move results.html templates/
```

**2. `ModuleNotFoundError: No module named 'flask'`**

**Problema:** Dependências não instaladas

**Solução:**
```bash
pip install -r requirements.txt
```

**3. Gráfico não é exibido**

**Problema:** Pasta `static/` não existe

**Solução:**
```bash
mkdir static
```

**4. Erro ao salvar no banco**

**Problema:** Permissões ou banco corrompido

**Solução:**
```bash
# Apague o banco e deixe recriar
rm projeto.db
python app.py
```

### Logs de Erro

O Flask exibe logs detalhados no terminal. Em caso de erro:

1. Leia a mensagem completa no terminal
2. Verifique a linha do erro (`File "...", line X`)
3. Consulte a seção de erros comuns acima
4. Se persistir, abra uma issue no GitHub

---

## Configurações Avançadas

### Alterar Porta do Servidor

Edite `app.py`:

```python
if __name__ == '__main__':
    app.run(debug=True, port=8080)  # Mude para 8080 ou outra porta
```

### Modo Produção

Para deployment, use um servidor WSGI como Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Personalizar Dados

Para usar dados de outra região ou culturas diferentes, edite `utils.py`:

```python
DEFAULT_DATA = {
    'Arroz': {'P': 45000.00},
    'Soja': {'P': 85000.00},
    # ... suas culturas
}
```

---

## Limitações

### Limitações Atuais

1. **Modelo Simplificado:** Usa função quadrática; reais podem ser mais complexos
2. **Dados Estáticos:** Baseado em um único estudo de caso
3. **Sem Clima:** Não considera variações climáticas
4. **Sem Mercado:** Não considera flutuação de preços
5. **Área Única:** Não otimiza mix de culturas

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

```
MIT License

Copyright (c) 2024 Paulo [Seu Sobrenome]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📚 Referências

1. **Silva, C. M. et al.** (2024). Otimização da produtividade agrícola e altos lucros em pequenas propriedades: uma abordagem integrada de modelagem matemática e agricultura familiar. *Revista Caderno Pedagógico*, v.21, n.3, p. 01-24. DOI: 10.54033/cadpedv21n3-094

2. **Stewart, J.** (2015). *Cálculo - Volume 1*. 8ª ed. São Paulo: Cengage Learning.

3. **Hillier, F. S.; Lieberman, G. J.** (2013). *Introdução à Pesquisa Operacional*. 9ª ed. Porto Alegre: AMGH.

4. **IBGE** (2017). *Censo Agropecuário 2017*. Instituto Brasileiro de Geografia e Estatística.

5. **EMBRAPA** (2023). *Agricultura Familiar no Brasil*. Empresa Brasileira de Pesquisa Agropecuária.