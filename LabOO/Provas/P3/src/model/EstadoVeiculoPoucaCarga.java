package LabOO_Prova.P3.Aluguel.src.model;

//criei esse daqui mais pensando em poder diferenciar se um veiculo esta quebrado (fora de uso) ou se so precisa recarregar, ao inves de jogar os dois pro mesmo estado

public class EstadoVeiculoPoucaCarga extends EstadoVeiculo{

    public EstadoVeiculoPoucaCarga(Veiculo veiculo) {
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
        return true;
    }

    @Override
    public String getNome() {
        return "Pouca carga";
    }
}
