package LabOO_Prova.P3.Aluguel.src.model;

import java.util.List;

/*
 * Usuários mensalistas devem poder cancelar suas assinaturas e efetuar o pagamento da mensalidade.
 */
/*
 * Usuários mensalistas não pagam a taxa fixa de uso, são cobrados R$0,10/minuto apenas após 30 minutos de uso e podem permanecer por um período máximo de 120 minutos, após o qual é aplicada multa de R$5,00 por minuto. 
 */

public class UsuarioMensalista extends Usuario {

    public UsuarioMensalista(int id, String nome, String localizacaoGeograficaAtual, String metodoPagamento, List<String> historicoViagens) {
        super(id, nome, localizacaoGeograficaAtual, metodoPagamento, historicoViagens);
        //TODO Auto-generated constructor stub
    }

    @Override
    public double calcularPrecoAluguel(int minutos) {
        double valorMinuto = 0.10;
        
        if (minutos <= 30) {
            return 0;
        } else {
            int minutosExtras = minutos - 120;
            return (minutos - 30) * valorMinuto + (minutosExtras * 5.0);
        }
    }
    
    @Override
    public int getTempoMaximo() {
        return 120;
    }
    
}
