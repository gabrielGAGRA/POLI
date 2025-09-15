package LabOO_Prova.P3.Aluguel.src.model;

/*
 * As bicicletas devem também possuir informações sobre _quantidade de marchas_ e _presença de faróis_.
 */

 /*
  * De forma a simplificar o funcionamento podemos assumir que a bateria de de bicicletas diminuem 10% a cada minuto usado e que a bateria de patinetes diminuem 20% a cada minuto usado. 
  */

public class Bicicleta extends Veiculo{
    private int quantidadeMarchas;
    private boolean possuiFarol;
    
    public Bicicleta(String localizacao, int id, int carga, int quantidadeMarchas, boolean possuiFarol) {
        super(localizacao, id, carga);
        //TODO Auto-generated constructor stub
        this.quantidadeMarchas = quantidadeMarchas;
        this.possuiFarol = possuiFarol;
        this.taxaBateria = 10;
    }

    public int getQuantidadeMarchas() {
      return quantidadeMarchas;
    }

    public boolean isPossuiFarol() {
      return possuiFarol;
    }

    @Override
    public String toString() {
        return "Bicicleta [quantidadeMarchas=" + quantidadeMarchas + ", possuiFarol=" + possuiFarol + "]";
    }
}
