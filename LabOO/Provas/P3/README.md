# Segunda Avaliação - MAC0321


## Identificação


Nome: Gabriel Agra de Castro Motta


NUSP: 15452743


Email USP: gabrielagra@usp.br


Endereço do repositório no Github: https://github.com/gabrielGAGRA/LabOO_Prova


## OBS
Me inspirei fortemente na solucao do simulado de gerenciador de caronas que estava disponivel no Moodle. 
Isso eh, utilizei principalmente de sua estrutura de implementacao de estados em caronas para criar os estados de veiculos.
Fica aqui como referencia de uso: https://github.com/gabrielGAGRA/LabOO/tree/main/Provas/Simulado_P3/src

## Instruções iniciais


Preencha o cabeçalho acima com seu nome completo, número e email USP.

Crie um repositório privado no Github e adicione @denismaua, @ArthurPilone e @DaphLie com permissão para visualizar. Copie este arquivo como parte de seu arquivo README.md, adicionando o endereço do repositório na seção acima.


Se seu repositório tiver visibilidade pública, será considerado plágio e sua nota será zerada. Se você se esquecer de fornecer permissão para o docente e monitores, receberá nota zero também.


Você pode acessar a internet para consultar a documentação de classes e bibliotecas dos Java e fóruns de perguntas e resposta como o StackOverflow. O acesso a sites que contenham soluções prontas ou muito similares a este exercício será considerado plágio. O uso de assistentes de código (Copilot, ChatGPT etc) também será considerado plágio.


Você deve acessar seu repositório e fazer atualizações por meio de commits e pushs do computador; para isso você deverá cadastrar uma chave pública ssh no github (usando o comando `ssh-keygen` e copiando a chave pública no diretório `~/.ssh/`).


Você deve entregar sua solução no e-disciplinas (contendo este arquivo e todo o código fonte e estrutura de pastas necessárias para execução e entendimento do seu projeto) e não deve fazer nenhuma alteração no repositório do Github após a entrega do arquivo. As versões no repositório e no e-disciplina devem ser idênticas, caso contrário sua nota será zerada. 


Você deve usar este arquivo para descrever qualquer decisão de projeto não trivial (ou seja, algo que não seja facilmente entendido a partir da sua base de código e hierarquia de classes). Isso inclui, por exemplo, detalhar qual arquivo deve ser executado (ou em que ordem, se mais de um), configurações e parâmetros necessários, se houverem, entre outras coisas.


## Descrição


Projete e implemente um sistema de software baseado em Orientação a Objetos para aluguel de veículos elétricos de baixa velocidade. O sistema deve possuir duas interfaces de uso: administração e locatário/usuário. 


Não é esperado que você desenvolva um sistema funcional que permita de fato que as duas interfaces estejam ativas simultaneamente, ou seja, você pode fazer um programa que alterna entre cada interface. Soluções que implementem a possibilidade de uso simultâneo das três interfaces terão bônus, no entanto, como soluções que usem interfaces gráficas, arquiteturas cliente-servidor ou arquitetura web.



## Administração


O sistema deve permitir ao administrador cadastrar novos veículos durante a execução e obter relatórios gerenciais sobre o uso dos veículos (ex. tempo médio por viagem, número de viagens, quantidade de veículos disponíveis e indisponíveis etc) e sobre os usuários (ex. quantidade de usuários, média de tempo total por usuário, média de custo etc). O administrador deve também poder alterar a disponibilidade de um determinado veículo (livre, em uso, fora de uso). 


## Veículos


Seu sistema deve permitir ao menos dois tipos de veículos elétricos: bicicletas e patinetes. Porém deve ser possível incluir novos tipos de veículo durante a execução e cadastrar novos veículos de dado tipo, sem precisar reiniciar (e recompilar) o sistema.


Cada veículo possui ao menos uma _localização geográfica_ (ex., GPS), _número de identificação_, _nível de carga de bateria_ e _disponibilidade para locação_. Um veículo deixa de estar disponível se estiver em uso, se seu nível de carga cai abaixo de 15%, se algum usuário relata algum problema.


As bicicletas devem também possuir informações sobre _quantidade de marchas_ e _presença de faróis_.


De forma a simplificar o funcionamento podemos assumir que a bateria de de bicicletas diminuem 10% a cada minuto usado e que a bateria de patinetes diminuem 20% a cada minuto usado. 

Um veículo pode ser carregado (é informado a quantidade de carga realizada pelo administrador).



## Usuários


Seu sistema deve permitir o cadastro de novos usuários. Cada usuário deve possuir um _número de identificação_, _nome_, _localização geográfica atual_ e _método de pagamento_ (ex. cartão de crédito, débito em conta etc). Os usuários se dividem em usuários avulsos e usuários mensalistas; um usuário avulso pode se tornar mensalista ao assinar o plano pago assim como um usuário mensalista pode se tornar avulso ao cancelar sua assinatura. 


A interface de usuário deve permitir listar todos os veículos próximos disponíveis à localização atual do usuário a partir de um dado parâmetro configurável (como raio de distância, por exemplo). 

O usuário deve poder realizar o aluguel de um veículo informando seu número de identificação, para liberar o veículo e iniciar a viagem. Uma vez iniciada a viagem o veículo deixa de estar disponível para locação.

O usuário deve também poder concluir a viagem, disponibilizando o veículo e concluindo o aluguel.

Por fim, o usuário deve poder relatar um problema com um veículo, tornando-o indisponível.


Usuários mensalistas devem poder cancelar suas assinaturas e efetuar o pagamento da mensalidade.

Usuários avulsos devem poder assinar o plano pago.

Todos os usuários devem poder gerar um relatório detalhando as viagens realizadas (com duração e custo) em dado período (por exemplo, segregado por meses) e o total de tempo e custo, além de outras informações relevantes (exemplo, o valor da mensalidade, se for mensalista, multas etc).


## Aluguel 


O aluguel é cobrado por minutos. Usuários avulsos pagam R$0,10/minuto de uso, mais uma taxa fixa de R$3,50 por uso, por um período máximo de 60 minutos. Após tal período é cobrado uma multa de R$5,00 por minuto ultrapassado. Usuários mensalistas não pagam a taxa fixa de uso, são cobrados R$0,10/minuto apenas após 30 minutos de uso e podem permanecer por um período máximo de 120 minutos, após o qual é aplicada multa de R$5,00 por minuto. 


Ao final do aluguel o sistema deve calcular e informar o valor devido e executar o pagamento. 


## Recomendações gerais


Você deve escrever um código bem organizado, documentado, modular, flexível e evitar a repetição de dados e redundância de código. Deve ser possível adicionar e remover funcionalidades de seu sistema afetando apenas as partes relevantes do seu código, o que implica não ter regras complexas com seleções condicionais que leve ao casamento de tipos de dados distintos. Lembre-se de aplicar as boas práticas de POO quanto à divisão de responsabilidades de classes e métodos, usar nomes claros para classes, atributos e métodos e manter a implementação de seus métodos curta (em geral, < 15 linhas), além de outras recomendações típicas.

Uma boa organização de seu código em classes e hierarquias é fundamental. **Lembre-se de programar para interfaces**.


Todas as classes e métodos criados devem ser usados ao menos uma vez no seu código. É recomendável que cada classe tenha sempre um método `main` demonstrando como usar a classe e os métodos principais. Não é necessário realizar casos de teste (embora seja considerado desejável).


Planeje antes de escrever seu código. Pense nas classes, atributos e métodos e nas relações entre objetos (comoposição, associação, especialização, interfaces etc).

Diagramas de classes são úteis para organizar seu planejamento. Pense também em casos de uso para as funcionalidades. Uma opção é escrever tais casos antes mesmo de implementar os métodos que o realizem.


## Entrega


Além de submeter seu código em seu repositório pessoal privado (commit e push), você deve submeter sua solução no edisciplinas na forma de um arquivo comprimido (.zip) contendo todo os arquivos necessários para a execução, incluindo a estrutura de pastas necessária. Plágios de qualquer tipo levarão a anulação do seu exame e consequente nota zero.