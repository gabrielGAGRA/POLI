package LabOO_Prova.P3.Aluguel.src.model;

// pra quando estiver com report de problema

public class EstadoVeiculoForaDeUso extends EstadoVeiculo{

    public EstadoVeiculoForaDeUso(Veiculo veiculo) {
        super(veiculo);
        //TODO Auto-generated constructor stub
    }
    
    @Override
    public boolean disponibilidade() {
        return false;
    }

    @Override
    public boolean alugar() {
        return false;
    }

    @Override
    public boolean finalizarAluguel() {
        return false;
    }

    @Override
    public boolean reportarProblema() {
        return false;
    }

    @Override
    public String getNome() {
        return "Fora de uso";
    }
}
