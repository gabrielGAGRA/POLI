package LabOO_Prova.P3.Aluguel.src.model;
import java.util.Random;

public class Distancia {
    private double localizacao;

    // coloquei um .random porque no readme fica confuso como seria. nesse caso entao ele gera uma aleatoria para manter o sistema funcional enquanto nao eh implementada
    private static final Random random = new Random();
    
    public Distancia(double localizacao) {
        this.localizacao = localizacao;
    }
    
    public double calcularDistancia(Distancia localizacao) {
        return random.nextDouble();
    }
}
