import os
from senhas import FilaSenhas
from banco import salvar_dados, carregar_dados

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print("=" * 50)
    print("   🏥 SISTEMA DE SENHAS - FARMÁCIA BASE REGIONAL")
    print("=" * 50)
    print("1. 📌 Gerar nova senha (Normal)")
    print("2. ⭐ Gerar nova senha (Prioritário)")
    print("3. 📋 Ver fila de espera")
    print("4. 📢 Chamar próximo paciente")
    print("5. 📊 Estatísticas")
    print("6. 💾 Salvar e Sair")
    print("=" * 50)

def main():
    fila, atendidas, contador = carregar_dados()
    
    sistema = FilaSenhas()
    sistema.fila = fila
    sistema.atendidas = atendidas
    sistema.contador = contador
    
    while True:
        limpar_tela()
        mostrar_menu()
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            senha = sistema.gerar_senha("Normal")
            print(f"\n✅ Senha gerada: **{senha}** (Normal)")
            input("\nPressione Enter para continuar...")
        
        elif opcao == "2":
            senha = sistema.gerar_senha("Prioritário")
            print(f"\n✅ Senha gerada: **{senha}** (Prioritário ⭐)")
            input("\nPressione Enter para continuar...")
        
        elif opcao == "3":
            fila_atual = sistema.listar_fila()
            if not fila_atual:
                print("\n📭 Nenhum paciente aguardando.")
            else:
                print("\n📋 FILA DE ESPERA:")
                print("-" * 30)
                for i, s in enumerate(fila_atual, 1):
                    tipo_icone = "⭐" if s["tipo"] == "Prioritário" else "📌"
                    print(f"{i}. {s['senha']} - {s['tipo']} {tipo_icone} - {s['horario']}")
            input("\nPressione Enter para continuar...")
        
        elif opcao == "4":
            proximo = sistema.chamar_proximo()
            if proximo:
                print(f"\n📢 CHAMANDO: **{proximo['senha']}** - {proximo['tipo']}")
                print(f"   ⏰ Gerado às {proximo['horario']}")
            else:
                print("\n📭 Nenhum paciente na fila para chamar.")
            input("\nPressione Enter para continuar...")
        
        elif opcao == "5":
            print("\n📊 ESTATÍSTICAS:")
            print("-" * 30)
            print(f"👥 Aguardando: {sistema.total_aguardando()}")
            print(f"✅ Atendidos hoje: {sistema.total_atendidos()}")
            if sistema.atendidas:
                ultimo = sistema.atendidas[-1]
                print(f"🕐 Último atendido: {ultimo['senha']} às {ultimo['horario_atendimento']}")
            input("\nPressione Enter para continuar...")
        
        elif opcao == "6":
            salvar_dados(sistema.fila, sistema.atendidas, sistema.contador)
            print("\n💾 Dados salvos com sucesso!")
            print("👋 Até logo!")
            break
        
        else:
            print("\n❌ Opção inválida. Tente novamente.")
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()