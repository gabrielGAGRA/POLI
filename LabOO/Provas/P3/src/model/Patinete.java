package LabOO_Prova.P3.Aluguel.src.model;

/*
 * De forma a simplificar o funcionamento podemos assumir que a bateria de de bicicletas diminuem 10% a cada minuto usado e que a bateria de patinetes diminuem 20% a cada minuto usado. 
 */

public class Patinete extends Veiculo{    
    public Patinete(String localizacao, int id, int carga) {
        super(localizacao, id, carga);
        //TODO Auto-generated constructor stub
        this.taxaBateria = 20;
    }

    @Override
    public String toString() {
        return "Patinete []";
    }
}

