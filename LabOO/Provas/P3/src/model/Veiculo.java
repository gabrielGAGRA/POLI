package LabOO_Prova.P3.Aluguel.src.model;

/*
 * Seu sistema deve permitir ao menos dois tipos de veículos elétricos: bicicletas e patinetes.
 */

/*
 * Cada veículo possui ao menos uma _localização geográfica_ (ex., GPS), _número de identificação_, _nível de carga de bateria_ e _disponibilidade para locação_. 
 * Um veículo deixa de estar disponível se estiver em uso, se seu nível de carga cai abaixo de 15%, se algum usuário relata algum problema.
 */

 /*
  * Um veículo pode ser carregado (é informado a quantidade de carga realizada pelo administrador).
  */

public class Veiculo {
    private String localizacao;
    private int id;
    private int carga;

    protected int taxaBateria;

    // padrao estado
    private EstadoVeiculo estado;

    public Veiculo(String localizacao, int id, int carga) {
        this.localizacao = localizacao;
        this.id = id;
        this.carga = carga;
        this.estado = new EstadoVeiculoLivre(this);
    }

    public void descarregarBateria(int minutos) {
        this.carga -= minutos * taxaBateria;
        if (this.carga < 0) this.carga = 0;
        
        if (this.carga < 15) {
            this.estado = new EstadoVeiculoForaDeUso(this);
        }
    }
    
    public void carregarBateria(int quantidade) {
        this.carga += quantidade;
        
        if (this.carga >= 15 && !this.estado.disponibilidade() && 
            this.estado.getNome() == ("Pouca baterria")) {
            this.estado = new EstadoVeiculoLivre(this);
        }
    }
    
    public boolean alugar() {
        return estado.alugar();
    }
    
    public boolean finalizarAluguel() {
        return estado.finalizarAluguel();
    }
    
    public boolean reportarProblema() {
        return estado.reportarProblema();
    }
    
    public boolean disponibilidade() {
        return estado.disponibilidade();
    }


    //getters e setters gerados
    public String getLocalizacao() {
        return localizacao;
    }

    public void setLocalizacao(String localizacao) {
        this.localizacao = localizacao;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getCarga() {
        return carga;
    }

    public void setCarga(int carga) {
        this.carga = carga;
    }

    public int getTaxaBateria() {
        return taxaBateria;
    }

    public void setTaxaBateria(int taxaBateria) {
        this.taxaBateria = taxaBateria;
    }

    public EstadoVeiculo getEstado() {
        return estado;
    }

    public void setEstado(EstadoVeiculo estado) {
        this.estado = estado;
    }

    @Override
    public String toString() {
        return "Veiculo [localizacao=" + localizacao + ", id=" + id + ", carga=" + carga + ", taxaBateria="
                + taxaBateria + ", estado=" + estado + "]";
    }

}