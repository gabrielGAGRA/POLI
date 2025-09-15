package LabOO_Prova.P3.Aluguel.src.model;

import java.util.List;

/*
 * Usuários avulsos devem poder assinar o plano pago.
 */

public class UsuarioAvulso extends Usuario {
    
    public UsuarioAvulso(int id, String nome, String localizacaoGeograficaAtual, String metodoPagamento, List<String> historicoViagens) {
        super(id, nome, localizacaoGeograficaAtual, metodoPagamento, historicoViagens);
        //TODO Auto-generated constructor stub
    }

    @Override
    public double calcularPrecoAluguel(int minutos) {
        double valorBase = 3.50; 
        double valorMinuto = 0.10;
        
        if (minutos <= 60) {
            return valorBase + (minutos * valorMinuto);
        } else {
            int minutosExtras = minutos - 60;
            return valorBase + (60 * valorMinuto) + (minutosExtras * 5.0);
        }
    }
    
    @Override
    public int getTempoMaximo() {
        return 60;
    }
  
}
