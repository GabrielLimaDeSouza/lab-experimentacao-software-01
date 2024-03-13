# Relatório Final

Relatório final para o trabalho de LAB sobre mineração de repositórios do GitHub

## Introdução:

Para a realização do trabalho, foi realizado uma análise abrangente das principais características de sistemas open-source populares, com foco em repositórios hospedados no GitHub. O objetivo foi entender como esses projetos são desenvolvidos, a frequência de contribuições externas, lançamento de releases, atualizações, linguagens de programação utilizadas e a taxa de fechamento de issues. Para atingir esse objetivo, foi coletado dados de 1.000 repositórios com o maior número de estrelas no GitHub. Para isso, foram feitas seis perguntas para o presente trabalho com hipóteses informais que visam responder essas perguntas:

### RQ 01 - Sistemas populares são maduros/antigos?

**HI 01** - Sistemas populares provavelmente serão mais antigos, indicando maturidade e estabilidade.

### RQ 02 - Sistemas populares recebem muita contribuição externa?

**HI 02** - Sistemas populares são mais propensos a receber uma quantidade significativa de `pull requests`, dado seu alcance e comunidade ativa.

### RQ 03 - Sistemas populares lançam releases com frequência?

**HI 03** - Sistemas populares podem lançar releases mais frequentes devido à necessidade de atualizações regulares para atender às expectativas da comunidade.

### RQ 04 - Sistemas populares são atualizados com frequência?

**HI 04** - Sistemas populares provavelmente são atualizados com mais frequência para manter sua relevância e correções de segurança.

### RQ 05 - Sistemas populares são escritos nas linguagens mais populares?

**HI 05** - Projetos populares podem ser mais diversificados em termos de linguagens de programação, refletindo a variedade de interesses da comunidade.

### RQ 06 - Sistemas populares possuem um alto percentual de issues fechadas?

**HI 06** - Sistemas populares podem ter uma taxa de fechamento de issues mais alta devido a uma comunidade ativa.

## Metodologia:

Para o desenvolvimento do trabalho, foi utilizado a metodologia ágil Scrum, dividindo a pesquisa em Sprints:

#### **Sprint 1:**

1. Realização das consultas GraphQL para 100 repositórios, obtendo todos os dados/métricas necessários para responder às RQs.
2. Desenvolvimento de script em Python para a automação das requisições, utilizando:
    - A biblioteca [Pandas](https://pandas.pydata.org/) para manipulação de dados;
    - O [python-dotenv](https://pypi.org/project/python-dotenv/) para armazenar o Token de Acesso do GitHub de forma segura.

#### **Sprint 2:**

1. Implementação de paginação para a consulta GraphQL, abrangendo 1.000 repositórios.
2. Exportação dos dados em arquivo .csv utilizando:
    - A biblioteca [Pandas](https://pandas.pydata.org/) para a salvar os dados para o arquivo .csv;
    - O [Matplotlib](https://matplotlib.org/) para a geração de gráficos representativos dos dados obtidos.
3. Desenvolvimento da primeira versão do relatório, incluindo a definição das hipóteses informais levantadas nas RQs.

## Resultados Obtidos

Esta seção é destinada a tentar responder as perguntas levantadas com base nos resultados obtidos com a mineração dos 1000 repositórios do GitHub mais populares. Para auxiliar a resposta das perguntas e ilustrar melhor os resultados, foram criados gráficos Boxplot e de Dispersão.

#### **RQ 01 - Sistemas populares são maduros/antigos?**

[Gráfico de Boxplot de idade]

Com base na análise do gráfico de boxplot da idade dos repositórios de sistemas open-source populares, podemos inferir que a maioria desses sistemas não necessariamente se caracteriza como madura ou antiga. A mediana da idade dos repositórios é aproximadamente 8 anos, indicando que metade dos sistemas populares tem menos de 8 anos, enquanto a outra metade tem mais de 8 anos. Os quartis mostram que a maioria dos sistemas (50%) possui uma idade variando entre 6 e 10 anos, com o primeiro quartil em torno de 6 anos e o terceiro quartil em cerca de 10 anos. Isso sugere que o tempo de desenvolvimento e a acumulação de funcionalidades podem, de fato, contribuir para a popularidade desses sistemas.

[Gráfico de Dispersão de idade]

Ao analisar o gráfico de dispersão da idade em relação ao número de estrelas, observamos uma variação mais ampla. Sistemas com idades entre 5 e 11 anos tendem a ter mais estrelas, corroborando a ideia de que o tempo de desenvolvimento e a acumulação de funcionalidades podem influenciar positivamente a popularidade. No entanto, o gráfico de dispersão também revela que alguns projetos novos podem se tornar populares rapidamente. Alguns sistemas mais recentes, apesar de sua juventude, apresentam um alto número de estrelas, indicando que a novidade e a utilidade também podem desempenhar um papel crucial na popularidade de um sistema open-source.

É importante ressaltar que a idade do repositório não é o único indicador de maturidade em um sistema open-source. Outros fatores, como atividade de desenvolvimento, comunidade de usuários e qualidade do código, desempenham papéis significativos nessa avaliação. O gráfico revela uma diversidade considerável de idades entre os sistemas populares, com alguns sendo relativamente novos, enquanto outros existem há mais de uma década. Essa variedade demonstra a dinâmica e a evolução contínua do ecossistema de software open-source.

#### **RQ 02 - Sistemas populares recebem muita contribuição externa?**

[Gráfico de Boxplot de última atualização]

[Gráfico de Dispersão de última atualização]

Sistemas open-source populares geralmente recebem uma quantidade significativa de contribuição externa, e o gráfico de dispersão fornecido corrobora essa afirmação. Em alguns casos, o número de `pull request` ultrapassa 10000.

Observamos uma correlação positiva entre a popularidade (quantificada pelo número de estrelas) e a quantidade de `pull requests` aceitas pelos sistemas. Isso significa que os sistemas mais populares tendem a receber mais `pull requests` aceitas. Essa relação sugere um alto nível de contribuição externa nos projetos mais populares, refletindo uma comunidade ativa e engajada de desenvolvedores.

Embora essa correlação seja evidente, há também exceções notáveis. Alguns pontos no gráfico representam sistemas menos populares que receberam um número significativo de `pull requests`. Essas exceções podem ser atribuídas a diversos fatores, como campanhas de contribuição, interesse em funcionalidades específicas ou uma comunidade particularmente engajada em um projeto específico.

#### **RQ 03 - Sistemas populares lançam releases com frequência?**

[Gráfico de Boxplot do número de releases]

[Gráfico de Dispersão do número de releases]

Na análise dos dados referentes aos lançamentos de releases nos projetos open-source populares, é possível observar uma tendência predominante: a maioria dos projetos com maior número de estrelas possui um número relativamente baixo de releases, concentrando-se principalmente entre 0 e 200 lançamentos. No entanto, é possível perceber que alguns sistemas mais populares lançaram um volume consideravelmente maior de releases.

Esses resultados sugerem algumas interpretações significativas. Primeiramente, torna-se evidente que a maioria dos sistemas open-source populares não segue uma frequência elevada de lançamentos de releases. Isso pode ser atribuído a práticas mais criteriosas de análise e validação do código desenvolvido, que incluem a realização de rotinas de testes e a manutenção de uma boa qualidade do código. No entanto, observamos exceções a essa tendência, indicando que certos projetos podem optar por um ritmo de lançamento mais acelerado. Essa decisão pode ser motivada tanto por necessidades imediatas, como correções de bugs ou implementação de novas funcionalidades, quanto por uma escolha deliberada da equipe de desenvolvimento.

Diversos fatores podem influenciar a frequência de lançamentos de releases. A natureza do projeto desempenha um papel significativo, onde projetos com ciclos de desenvolvimento mais longos tendem a lançar releases com menos frequência. Além disso, a dinâmica da comunidade e as prioridades da equipe de desenvolvimento também podem afetar essa frequência, visto que diferentes grupos podem ter expectativas distintas em relação aos lançamentos.

#### **RQ 04 - Sistemas populares são atualizados com frequência?**

[Gráfico de Boxplot do tempo até a última atualização]

[Gráfico de Dispersão do tempo até a última atualização]

A análise dos dados revela um padrão incerto na frequência de atualização dos sistemas open-source populares em relação à sua popularidade. Não há uma relação direta entre a quantidade de atualizações e a popularidade dos projetos. Eles podem apresentar uma variedade de tempos de atualização, que vão desde dias até anos, indicando uma grande diversidade nesse aspecto.

A frequência de atualização dos sistemas open-source populares não está diretamente ligada à sua popularidade. Vários fatores podem influenciar essa frequência, incluindo a natureza do projeto, seu ciclo de desenvolvimento, a atividade da comunidade e os recursos disponíveis para a equipe de desenvolvimento.

#### **RQ 05 - Sistemas populares são escritos nas linguagens mais populares?**

[Gráfico de Boxplot da linguagem primária dos repositórios]

[Gráfico de Dispersão da linguagem primária dos repositórios]

Algumas linguagens, como JavaScript, Python e Java, destacam-se por concentrar um grande número de repositórios populares, evidenciando sua ampla aceitação e uso na comunidade de desenvolvimento. No entanto, além dessas linguagens populares, também encontramos uma variedade de outras linguagens presentes em sistemas populares, como C++, PHP, Go, C# e Ruby, demonstrando a diversidade de escolhas utilizadas na construção desses projetos.

Embora exista uma correlação entre a popularidade de uma linguagem e sua probabilidade de ser utilizada em sistemas populares, também encontramos exceções notáveis. É possível notar também que alguns casos, linguagens menos populares estão presentes em sistemas considerados populares. Isso sugere que a escolha da linguagem vai além da sua popularidade e está sujeita a uma série de fatores adicionais.

Além da popularidade, a escolha da linguagem de programação depende de diversos fatores, como a natureza específica do projeto, a familiaridade da equipe de desenvolvimento com a linguagem e a disponibilidade de ferramentas e bibliotecas adequadas. Esses elementos influenciam diretamente a seleção da linguagem mais adequada para cada contexto de desenvolvimento.

#### **RQ 06 - Sistemas populares possuem um alto percentual de issues fechadas?**

[Gráfico de Boxplot de issues fechadas]

[Gráfico de Dispersão de issues fechadas]

A análise do gráfico de dispersão revela uma correlação positiva entre a popularidade dos sistemas open-source, medida pelo número de estrelas, e a taxa de issues fechadas. Sistemas mais populares tendem a apresentar uma taxa de issues fechadas mais alta, indicando uma eficácia superior na resolução de problemas. No entanto, também observamos exceções a essa tendência, em que sistemas menos populares exibem uma alta taxa de issues fechadas e vice-versa.

Isso indica que sistemas open-source populares geralmente são mais eficientes na resolução de issues. Essa eficiência pode ser atribuída a diversos fatores, como a presença de uma comunidade de colaboradores mais ampla, um maior nível de atenção e engajamento dedicado às questões levantadas e uma disponibilidade de recursos mais robusta para abordar os problemas identificados.

A elevada taxa de fechamento de issues em projetos populares pode estar diretamente associada ao grande volume de `pull requests` aceitas e à frequência considerável de atualizações realizadas.

## Discussão da Hipóteses

Nesta seção, serão analisadas as hipóteses informais relacionadas às perguntas investigativas em consonância com os resultados obtidos neste estudo:

-   **HI 01 - Sistemas populares provavelmente serão mais antigos, indicando maturidade e estabilidade.**

Os resultados da pesquisa indicam que a idade dos repositórios varia consideravelmente, com uma mediana em torno de 8 anos. Isso sugere que enquanto alguns sistemas populares são de fato mais antigos, uma parte significativa deles também é relativamente recente. A relação entre idade e popularidade não é determinista, uma vez que a novidade e a utilidade também desempenham papéis importantes na popularidade de um sistema open-source.

-   **HI 02 - Sistemas populares são mais propensos a receber uma quantidade significativa de `pull requests`, dado seu alcance e comunidade ativa.**

Os resultados confirmam essa hipótese, mostrando uma correlação positiva entre popularidade e quantidade de `pull requests` aceitas. Os sistemas mais populares tendem a receber mais contribuições externas, refletindo uma comunidade ativa e engajada de desenvolvedores.

-   **HI 03 - Sistemas populares podem lançar releases mais frequentes devido à necessidade de atualizações regulares para atender às expectativas da comunidade.**

Embora alguns sistemas populares tenham lançado um volume considerável de releases, a maioria possui um número relativamente baixo. Isso sugere que, embora a necessidade de atualizações regulares seja reconhecida, a frequência de lançamentos varia amplamente entre os projetos.

-   **HI 04 - Sistemas populares provavelmente são atualizados com mais frequência para manter sua relevância e correções de segurança.**

Os resultados indicam uma variedade de tempos de atualização, sem uma relação direta entre a popularidade e a frequência de atualizações. Diversos fatores podem influenciar essa frequência, não sendo possível afirmar que sistemas populares são atualizados com mais frequência de forma geral.

-   **HI 05 - Projetos populares podem ser mais diversificados em termos de linguagens de programação, refletindo a variedade de interesses da comunidade.**

Os dados confirmam essa hipótese, mostrando que além das linguagens mais populares, uma variedade de outras linguagens está presente em sistemas populares. Isso sugere que a escolha da linguagem vai além da popularidade e está sujeita a uma série de fatores adicionais.

-   **HI 06 - Sistemas populares podem ter uma taxa de fechamento de issues mais alta devido a uma comunidade ativa.**

Os resultados mostram uma correlação positiva entre popularidade e taxa de issues fechadas, indicando que sistemas populares são mais eficientes na resolução de problemas. Isso pode ser atribuído a uma comunidade de colaboradores mais ampla e recursos mais robustos para abordar os problemas identificados.

## Conclusão

A análise abrangente das principais características de sistemas open-source populares, utilizando dados de 1000 repositórios hospedados no GitHub, proporcionou algumas percepções sobre a dinâmica e complexidade desses projetos. Esta pesquisa visa compreender o desenvolvimento, a participação da comunidade, os padrões de lançamento, as linguagens de programação e a eficiência na resolução de problemas nesses sistemas.

Os resultados obtidos revelam uma variedade de padrões e tendências que desafiam algumas das suposições iniciais. Em relação à idade dos repositórios, enquanto alguns sistemas populares são mais antigos, uma parte significativa é relativamente recente, sugerindo que a novidade e a utilidade também são importantes para a popularidade. A correlação entre popularidade e quantidade de `pull requests` aceitas confirma a hipótese de que sistemas populares recebem uma quantidade significativa de contribuições externas, refletindo uma comunidade ativa e engajada de desenvolvedores.

No entanto, em relação aos lançamentos de releases e atualizações, não foi identificada uma tendência clara. A frequência de lançamentos varia amplamente entre os projetos, e não há uma relação direta entre popularidade e frequência de atualizações. Da mesma forma, a escolha da linguagem de programação não se limita às mais populares, refletindo a diversidade de escolhas da comunidade de desenvolvimento.

A eficiência na resolução de problemas, medida pela taxa de issues fechadas, tende a ser maior em sistemas populares, sugerindo uma comunidade de colaboradores mais ampla e recursos mais robustos para abordar problemas identificados.

Essas descobertas destacam a complexidade e a variedade do ecossistema de software open-source. A contribuição para esses projetos vai além da idade e popularidade, envolvendo fatores como novidade, utilidade, diversidade de linguagens e engajamento da comunidade. Compreender esses aspectos é essencial para direcionar o desenvolvimento e a colaboração na comunidade open-source, impulsionando a inovação e a excelência nos projetos.
