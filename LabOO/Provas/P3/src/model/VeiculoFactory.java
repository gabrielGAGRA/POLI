package LabOO_Prova.P3.Aluguel.src.model;

//pra gerenciar as bicicletas e parinetes sem precisar se importar com suas diferencas

public class VeiculoFactory {
    public Bicicleta criarBicicleta(String localizacao, int id, int carga, int quantidadeMarchas, boolean possuiFarol) {
        return new Bicicleta(localizacao, id, carga, quantidadeMarchas, possuiFarol);
    }
    
    public Patinete criarPatinete(String localizacao, int id, int carga) {
        return new Patinete(localizacao, id, carga);
    }
    
    public Veiculo criarVeiculo(String tipo, String localizacao, int id, int carga, Object... params) {
        if (tipo == "bicicleta") {
            int marchas = (int)params[0];
            boolean farol = (boolean)params[1];
            return criarBicicleta(localizacao, id, carga, marchas, farol);
        } else if (tipo == "patinete") {
            return criarPatinete(localizacao, id, carga);
        }
        return null;
    }
}
