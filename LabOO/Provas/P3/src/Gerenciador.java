package LabOO_Prova.P3.Aluguel.src;

import java.util.Scanner;

import LabOO_Prova.P3.Aluguel.src.model.Veiculo;
import LabOO_Prova.P3.Aluguel.src.interface_sistema.SistemaAluguel;
import LabOO_Prova.P3.Aluguel.src.interface_sistema.SistemaAluguelFacade;




public class Gerenciador {
    /*
     * O sistema deve permitir ao administrador cadastrar novos veículos durante a execução e obter relatórios gerenciais sobre o uso dos veículos (ex. tempo médio por viagem, número de viagens, quantidade de veículos disponíveis e indisponíveis etc) e sobre os usuários (ex. quantidade de usuários, média de tempo total por usuário, média de custo etc). 
     * O administrador deve também poder alterar a disponibilidade de um determinado veículo (livre, em uso, fora de uso). 
     */
    
     /*
      * Um veículo pode ser carregado (é informado a quantidade de carga realizada pelo administrador).
      */

    private static Gerenciador instancia;

    //singleton
    public static Gerenciador getInstancia() {
        if (instancia == null) {
            instancia = new Gerenciador();
        }
        return instancia;
    }

    private static Scanner scanner = new Scanner(System.in);
    private static Gerenciador gerenciador = Gerenciador.getInstancia();

    public static void main(String[] args) {
        int opcao = -1;
                
        while (opcao != 0) {
            exibirMenu();
            opcao = scanner.nextInt();
            scanner.nextLine();
            
            switch (opcao) {
                case 1:
                    menuAdministrador();
                    break;
                case 2:
                    menuUsuario();
                    break;
                case 0:
                    System.out.println("Saindo");
                    break;
            }
        }
        scanner.close();
    }
    
    private static void exibirMenu() {
        System.out.println("1 Admnistrador");
        System.out.println("2 Usuáiro");
        System.out.println("0 Sairr");
    }
    
    private static void menuAdministrador() {
        int opcao = -1;
        
        while (opcao != 0) {
            System.out.println("1 Cadastra bicicleta");
            System.out.println("2. Cadastra patinette");
            System.out.println("3. Carrega bateria de veiculo");
            System.out.println("4. Relatorio");
            System.out.println("5. Relatorio de usúarios");
            
            opcao = scanner.nextInt();
            scanner.nextLine(); 
            
            switch (opcao) {
                case 1:
                    cadastrarBicicleta();
                    break;
                case 2:
                    cadastrarPatinete();
                    break;
                case 3:
                    carregarBateria();
                    break;
                case 4:
                    gerenciador.gerarRelatorioAdministrativo();
                    break;
                case 5:
                    gerenciador.gerarRelatorioUsuario();
                    break;
                case 0:
                    break;
            }
        }
    }
    
    private static void menuUsuario() {
        int opcao = -1;
        
        while (opcao != 0) {
            System.out.println("1. Cadastra novo avulço");
            System.out.println("2. Cadastra novo mensalistta");
            System.out.println("3. Busca veiculos disponiveis");
            System.out.println("4. Aluga veiculo");
            System.out.println("5. Finaliza aluguel");
            System.out.println("6. Reporta problema");
            
            opcao = scanner.nextInt();
            scanner.nextLine();
            
            switch (opcao) {
                case 1:
                    cadastrarUsuarioAvulso();
                    break;
                case 2:
                    cadastrarUsuarioMensalista();
                    break;
                case 3:
                    buscarVeiculosDisponiveis();
                    break;
                case 4:
                    alugarVeiculo();
                    break;
                case 5:
                    finalizarSistemaAluguel();
                    break;
                case 6:
                    reportarProblema();
                    break;
                case 0:
                    break;
            }
        }
    }
    
    private static void cadastrarBicicleta() {
        System.out.print("Localizacão: ");
        String localizacao = scanner.nextLine();
        
        System.out.print("Carga da bateria: ");
        int carga = scanner.nextInt();
        
        System.out.print("Quantidde de marchas: ");
        int marchas = scanner.nextInt();
        
        System.out.print("FArol: ");
        int temFarol = scanner.nextInt();
        
        Veiculo bicicleta = gerenciador.cadastrarBicicleta(localizacao, carga, marchas, temFarol == 1);
    }
    
    
    private static void buscarVeiculosDisponiveis() {
        System.out.print("Localização: ");
        String localizacao = scanner.nextLine();
        
        System.out.print("Raio de busca: ");
        double raio = scanner.nextDouble();
        
        List<Veiculo> veiculosDisponiveis = gerenciador.buscarVeiculosProximos(localizacao, raio);
        
        if (veiculosDisponiveis.isEmpty()) {
            System.out.println("Nenhum veículo disponíve");
        } else {
            for (Veiculo veiculo : veiculosDisponiveis) {
                System.out.println(veiculo);
            }
        }
    }
    
    private static void alugarVeiculo() {
        System.out.print("ID do usuário: ");
        int idUsuario = scanner.nextInt();
        
        System.out.print("ID do veículo: ");
        int idVeiculo = scanner.nextInt();
        
        SistemaAluguel aluguel = gerenciador.criarSistemaAluguel(idUsuario, idVeiculo);
    }
    
    private static void finalizarSistemaAluguel() {
        System.out.print("ID do aluguel: ");
        int idSistemaAluguel = scanner.nextInt();
    }
    
    private static void reportarProblema() {
        System.out.print("ID do veículo: ");
        int idVeiculo = scanner.nextInt();
    }
}