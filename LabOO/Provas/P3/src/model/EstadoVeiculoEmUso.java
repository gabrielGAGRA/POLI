package LabOO_Prova.P3.Aluguel.src.model;

public class EstadoVeiculoEmUso extends EstadoVeiculo{

    public EstadoVeiculoEmUso(Veiculo veiculo) {
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
        if (getVeiculo().getCarga() < 15) {
            getVeiculo().setEstado(new EstadoVeiculoPoucaCarga(getVeiculo()));
        } else {
            getVeiculo().setEstado(new EstadoVeiculoLivre(getVeiculo()));
        }
        return true;
    }

    @Override
    public boolean reportarProblema() {
        getVeiculo().setEstado(new EstadoVeiculoForaDeUso(getVeiculo()));
        return true;
    }

    @Override
    public String getNome() {
        return "Em uso";
    }
}
