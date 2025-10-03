# 💻 Trabalho 1 - Sistemas Operacionais 

Este repositório contém as resoluções das 3 questões do **Trabalho 1** da disciplina de Sistemas Operacionais (IFCE - Campus Maracanaú), ministrada pelo professor **Daniel Ferreira**.

---

## 📌 Questões

### Questão 1
Simulação de algoritmos de escalonamento de processos:  
- **RR (Round Robin)** com diferentes quantuns.  
- Comparação com **FCFS (First Come, First Served)** e **SJF (Shortest Job First)** não-preemptivo.  
- Cálculo e comparação das métricas: tempo médio de espera, tempo médio de retorno e vazão.  
- Geração de tabelas e gráficos para análise dos resultados.

### Questão 2
Simulação de **5 programadores** que precisam compilar seus códigos com recursos limitados:  
- Um compilador (acesso exclusivo).  
- Um banco de dependências (máx. 2 acessos simultâneos).  
- Sincronização com **threads e semáforos**.  
- Impressão contínua do estado de cada programador, evitando **deadlocks** e **inanimação**.

### Questão 3
Simulação de protocolo em **hospital veterinário**:  
- Sala de repouso que só pode conter **cachorros** ou **gatos**, nunca os dois ao mesmo tempo.  
- Estados possíveis: `EMPTY`, `DOGS`, `CATS`.  
- Fila de espera organizada por ordem de chegada (**FIFO**).  
- Geração de uma **timeline JSON** com a evolução dos estados.

---

## 📦 Requisitos

- Python **3.9+**
- Bibliotecas externas:
  - [pandas](https://pandas.pydata.org/)
  - [matplotlib](https://matplotlib.org/)

### Instalação das dependências

Na raiz do projeto, execute:

```bash
pip install -r requirements.txt
