# py2do
Aplicativo 2DO simples para linha de comando. Suporta os seguintes comandos:

```
$: a texto_da_tarefa t:tag1,tag2,...    # Adiciona registro, informações após 't:'
                                          e separadas por vírgulas tornam-se TAGs

$: la                                   # Lista tudo, sem filtros

$: lp                                   # Lista registros pendentes

$: lc                                   # Lista registros concluidos

$: c 1,2,3,5-7...                       # Marca registros com os respectivos números como concluidos

$: p 1,2,3,8...                         # Marca registros com os respectivos números como pendentes

```

Os comandos 'c' (tarefas concluídas) e 'p' (tarefas pendentes) aceitam números isolados e intervalos numéricos.


