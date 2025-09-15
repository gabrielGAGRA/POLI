package LabOO_Prova.P3.Aluguel.src.model;

/*
 * estado do veiculo abstrata
 */

public abstract class EstadoVeiculo {
    private Veiculo veiculo;
    
    public EstadoVeiculo(Veiculo veiculo) {
        this.veiculo = veiculo;
    }
    
    protected Veiculo getVeiculo() {
        return veiculo;
    }
    
    public abstract boolean disponibilidade();
    public abstract boolean alugar();
    public abstract boolean finalizarAluguel();
    public abstract boolean reportarProblema();
    public abstract String getNome();
}