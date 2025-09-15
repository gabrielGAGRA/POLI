package LabOO_Prova.P3.Aluguel.src.model;

import java.util.ArrayList;
import java.util.List;

/*
 * Seu sistema deve permitir o cadastro de novos usuários. 
 * Cada usuário deve possuir um _número de identificação_, _nome_, _localização geográfica atual_ e _método de pagamento_ (ex. cartão de crédito, débito em conta etc). 
 * Os usuários se dividem em usuários avulsos e usuários mensalistas; um usuário avulso pode se tornar mensalista ao assinar o plano pago assim como um usuário mensalista pode se tornar avulso ao cancelar sua assinatura. 
 */

  /*
   * O usuário deve poder realizar o aluguel de um veículo informando seu número de identificação, para liberar o veículo e iniciar a viagem. Uma vez iniciada a viagem o veículo deixa de estar disponível para locação.
   * O usuário deve também poder concluir a viagem, disponibilizando o veículo e concluindo o aluguel.
   * Por fim, o usuário deve poder relatar um problema com um veículo, tornando-o indisponível.
   * Todos os usuários devem poder gerar um relatório detalhando as viagens realizadas (com duração e custo) em dado período (por exemplo, segregado por meses) e o total de tempo e custo, além de outras informações relevantes (exemplo, o valor da mensalidade, se for mensalista, multas etc).
   */
  
public abstract class Usuario {
   private int id;
   private String nome;
   private String localizacaoGeograficaAtual;
   private String metodoPagamento;
   private List<String> historicoViagens;
    

   public Usuario(int id, String nome, String localizacaoGeograficaAtual, String metodoPagamento,
         List<String> historicoViagens) {
      this.id = id;
      this.nome = nome;
      this.localizacaoGeograficaAtual = localizacaoGeograficaAtual;
      this.metodoPagamento = metodoPagamento;
      this.historicoViagens = historicoViagens;
   }
   //ambas vao depender do tipo de usuario, das subclasses avulso e mensalista
   public abstract double calcularPrecoAluguel(int minutos);
   public abstract int getTempoMaximo();

   public void adicionarViagem(String detalhesViagem) {
       historicoViagens.add(detalhesViagem);
   }
   
   public List<String> getHistoricoViagens() {
       return new ArrayList<>(historicoViagens);
   }

   //getters e setters
   //removi set ID porque deve ser criado e nunca modificado
    public int getId() {
       return id;
    }

    public String getNome() {
       return nome;
    }

    public void setNome(String nome) {
       this.nome = nome;
    }

    public String getLocalizacaoGeograficaAtual() {
       return localizacaoGeograficaAtual;
    }

    public void setLocalizacaoGeograficaAtual(String localizacaoGeograficaAtual) {
       this.localizacaoGeograficaAtual = localizacaoGeograficaAtual;
    }

    public String getMetodoPagamento() {
       return metodoPagamento;
    }

    public void setMetodoPagamento(String metodoPagamento) {
       this.metodoPagamento = metodoPagamento;
    }
}
