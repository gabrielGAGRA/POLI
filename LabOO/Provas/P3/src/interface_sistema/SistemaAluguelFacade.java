package LabOO_Prova.P3.Aluguel.src.interface_sistema;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import java.util.Random;

import LabOO_Prova.P3.Aluguel.src.model.Bicicleta;
import LabOO_Prova.P3.Aluguel.src.model.Distancia;
import LabOO_Prova.P3.Aluguel.src.model.Patinete;
import LabOO_Prova.P3.Aluguel.src.model.Usuario;
import LabOO_Prova.P3.Aluguel.src.model.UsuarioAvulso;
import LabOO_Prova.P3.Aluguel.src.model.UsuarioMensalista;
import LabOO_Prova.P3.Aluguel.src.model.Veiculo;
import LabOO_Prova.P3.Aluguel.src.model.VeiculoFactory;

public class SistemaAluguelFacade {
    private List<Veiculo> veiculos;
    private List<Usuario> usuarios;
    private List<SistemaAluguel> alugueis;
    private VeiculoFactory veiculo;
    
    private static SistemaAluguelFacade instancia;

    private static final Random random = new Random();

    private SistemaAluguelFacade() {
        this.veiculos = new ArrayList<>();
        this.usuarios = new ArrayList<>();
        this.alugueis = new ArrayList<>();
        this.veiculo = new VeiculoFactory();
    }
    
    public static SistemaAluguelFacade getInstancia() {
        if (instancia == null) {
            instancia = new SistemaAluguelFacade();
        }
        return instancia;
    }


    
    public Bicicleta cadastrarBicicleta(String localizacao, int carga, int marchas, boolean temFarol) {
        int id = random.nextInt();
        Bicicleta bicicleta = veiculo.criarBicicleta(localizacao, id, carga, marchas, temFarol);
        veiculos.add(bicicleta);
        return bicicleta;
    }
    public Patinete cadastrarPatinete(String localizacao, int carga) {
        int id = random.nextInt();
        Patinete patinete = veiculo.criarPatinete(localizacao, id, carga);
        veiculos.add(patinete);
        return patinete;
    }
    public void carregarBateria(int idVeiculo, int quantidade) {
        Veiculo veiculo = buscarVeiculoPorId(idVeiculo);
        veiculo.carregarBateria(quantidade);
    }




    public Usuario cadastrarUsuarioAvulso(String nome, String localizacao, String metodoPagamento, List<String> historicoViagens) {
        int id = random.nextInt();
        Usuario usuario = new UsuarioAvulso(id, nome, localizacao, metodoPagamento, historicoViagens);
        usuarios.add(usuario);
        return usuario;
    }
    public Usuario cadastrarUsuarioMensalista(String nome, String localizacao, String metodoPagamento, List<String> historicoViagens) {
        int id = random.nextInt();
        Usuario usuario = new UsuarioMensalista(id, nome, localizacao, metodoPagamento, historicoViagens);
        usuarios.add(usuario);
        return usuario;
    }
    public void converterParaMensalista(int idUsuario) {
        Usuario usuario = buscarUsuarioPorId(idUsuario);
            UsuarioMensalista novoUsuario = new UsuarioMensalista(
                usuario.getId(), 
                usuario.getNome(), 
                usuario.getLocalizacaoGeograficaAtual(), 
                usuario.getMetodoPagamento(),
                usuario.getHistoricoViagens()
            )
            
            int index = usuarios.indexOf(usuario);
            usuarios.set(index, novoUsuario);
        }
    public void converterParaAvulso(int idUsuario) {
        Usuario usuario = buscarUsuarioPorId(idUsuario);
        UsuarioAvulso novoUsuario = new UsuarioAvulso(
                usuario.getId(), 
                usuario.getNome(), 
                usuario.getLocalizacaoGeograficaAtual(), 
                usuario.getMetodoPagamento(),
                usuario.getHistoricoViagens()
        );
            
            int index = usuarios.indexOf(usuario);
            usuarios.set(index, novoUsuario);
        }

    

    //se tiver ocupado, nao alugamos
    public SistemaAluguel iniciarAluguel(int idUsuario, int idVeiculo) {
        Usuario usuario = buscarUsuarioPorId(idUsuario);
        Veiculo veiculo = buscarVeiculoPorId(idVeiculo);

        if (veiculo.disponibilidade()) {
            int idAluguel = random.nextInt();
            double valorAluguel = 0.0;
            boolean finalizado = false;
            SistemaAluguel aluguel = new SistemaAluguel(idAluguel, usuario, veiculo, valorAluguel, finalizado);
            alugueis.add(aluguel);
            return aluguel;
        }
        return null;
    }

    public double finalizarAluguel(int idAluguel) {
        SistemaAluguel aluguel = buscarAluguelPorId(idAluguel);
        return aluguel.getValorAluguel();
    }
    public boolean reportarProblema(int idAluguel) {
        SistemaAluguel aluguel = buscarAluguelPorId(idAluguel);
        aluguel.reportarProblema();
        return true;
    }
    


    
    public String gerarRelatorio() {
        StringBuilder relatorio = new StringBuilder();
        relatorio.append("Ttoal de veiculos: ").append(veiculos.size()).append("\n");
        
        long veiculosDisponiveis = veiculos.stream().filter(Veiculo::disponibilidade).count();
        relatorio.append("Veiculos disponiveis: ").append(veiculosDisponiveis).append("\n");
        relatorio.append("Veiculos indisponiveis: ").append(veiculos.size() - veiculosDisponiveis).append("\n");
        
        relatorio.append("Ttoal de usuarios: ").append(usuarios.size()).append("\n");
        relatorio.append("Ttoal de alugueis: ").append(alugueis.size()).append("\n");
        
        return relatorio.toString();
    }
    
    public String gerarRelatorioUsuario(int idUsuario) {
        Usuario usuario = buscarUsuarioPorId(idUsuario);
        if (usuario == null) return "Usuario nao encotrnado";
        
        StringBuilder relatorio = new StringBuilder();
        relatorio.append("Usuario: ").append(usuario.getNome()).append("\n");
        relatorio.append("Tipo: ").append(usuario instanceof UsuarioAvulso ? "Avulso" : "Mensalista").append("\n");
        
        return relatorio.toString();
    }
    
    public List<Veiculo> buscarVeiculosProximos(String localizacaoUsuario, double raioKm) {
        return veiculos.stream()
            .filter(Veiculo::disponibilidade)
            .filter(v -> Distancia.calcularDistancia(
                localizacaoUsuario))
            .collect(Collectors.toList());
    }
    
    private Veiculo buscarVeiculoPorId(int id) {
        return veiculos.stream()
            .filter(v -> v.getId() == id)
            .findFirst()
            .orElse(null);
    }
    
    private Usuario buscarUsuarioPorId(int id) {
        return usuarios.stream()
            .filter(u -> u.getId() == id)
            .findFirst()
            .orElse(null);
    }
    
    private SistemaAluguel buscarAluguelPorId(int id) {
        return alugueis.stream()
            .filter(a -> a.getIdAluguel() == id)
            .findFirst()
            .orElse(null);
    }
    
    public List<Veiculo> getVeiculos() {
        return new ArrayList<>(veiculos);
    }
    
    public List<Usuario> getUsuarios() {
        return new ArrayList<>(usuarios);
    }
}