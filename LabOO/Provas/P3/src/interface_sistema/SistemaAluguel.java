package LabOO_Prova.P3.Aluguel.src.interface_sistema;

import LabOO_Prova.P3.Aluguel.src.model.Usuario;
import LabOO_Prova.P3.Aluguel.src.model.Veiculo;

public class SistemaAluguel {
    private int idAluguel;
    private Usuario usuario;
    private Veiculo veiculo;
    private double valorAluguel;
    private boolean finalizado;
    private long start;
    private long finish;
        

    public SistemaAluguel(int idAluguel, Usuario usuario, Veiculo veiculo, double valorAluguel, boolean finalizado) {
        this.idAluguel = idAluguel;
        this.usuario = usuario;
        this.veiculo = veiculo;
        this.valorAluguel = valorAluguel;
        this.finalizado = finalizado;
        this.valorAluguel = valorAluguel;
        this.finalizado = finalizado;

        this.start = System.currentTimeMillis();
        veiculo.alugar();
    }
    
    public void finalizarAluguel() {
        //como implementar um sistema que conta quanto tempo passou: https://www.baeldung.com/java-measure-elapsed-time
        this.finish = System.currentTimeMillis();
        long duracaoMinutos = (finish - start) / 60000;
            
        veiculo.descarregarBateria((int)duracaoMinutos);
        this.valorAluguel = usuario.calcularPrecoAluguel((int)duracaoMinutos);
        veiculo.finalizarAluguel();
            
        this.finalizado = true;
    }
    public void reportarProblema() {
        veiculo.reportarProblema();
        this.finalizado = true;
    }


    //getters e setters
    public int getIdAluguel() {
        return idAluguel;
    }

    public void setIdAluguel(int idAluguel) {
        this.idAluguel = idAluguel;
    }

    public Usuario getUsuario() {
        return usuario;
    }

    public void setUsuario(Usuario usuario) {
        this.usuario = usuario;
    }

    public Veiculo getVeiculo() {
        return veiculo;
    }

    public void setVeiculo(Veiculo veiculo) {
        this.veiculo = veiculo;
    }

    public double getValorAluguel() {
        return valorAluguel;
    }

    public void setValorAluguel(double valorAluguel) {
        this.valorAluguel = valorAluguel;
    }

    public boolean isFinalizado() {
        return finalizado;
    }

    public void setFinalizado(boolean finalizado) {
        this.finalizado = finalizado;
    }
}