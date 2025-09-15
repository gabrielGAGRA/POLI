package LabOO_Prova.P3.Aluguel.src.model;

public class EstadoVeiculoLivre extends EstadoVeiculo{

    public EstadoVeiculoLivre(Veiculo veiculo) {
        super(veiculo);
        //TODO Auto-generated constructor stub
    }

    @Override
    public boolean disponibilidade() {
        return true;
    }

    @Override
    public boolean alugar() {
        getVeiculo().setEstado(new EstadoVeiculoEmUso(getVeiculo()));
        return true;
    }

    @Override
    public boolean finalizarAluguel() {
        return false;
    }

    @Override
    public boolean reportarProblema() {
        getVeiculo().setEstado(new EstadoVeiculoForaDeUso(getVeiculo()));
        return true;
    }

    @Override
    public String getNome() {
        return "Livre";
    }
}

