#!/usr/bin/env python3
"""
Investigar a diferença de R$ 500,00 no total de compra
"""

def investigar_diferenca_500():
    """Investigar de onde vem a diferença de R$ 500,00"""
    
    print("=== INVESTIGAÇÃO DA DIFERENÇA DE R$ 500,00 ===")
    
    # Valores conhecidos
    total_compra_sistema = 3140.31
    total_compra_usuario = 3640.314
    diferenca = total_compra_usuario - total_compra_sistema
    
    print(f"Total compra sistema: R$ {total_compra_sistema:.2f}")
    print(f"Total compra usuário: R$ {total_compra_usuario:.2f}")
    print(f"Diferença: R$ {diferenca:.2f}")
    
    # Dados do payload original
    freight_value_total = 500  # Valor do frete informado no payload
    
    print(f"\n=== ANÁLISE DO FRETE ===")
    print(f"Frete informado no payload: R$ {freight_value_total:.2f}")
    print(f"Diferença encontrada: R$ {diferenca:.2f}")
    
    if abs(diferenca - freight_value_total) < 1.0:
        print("✅ EUREKA! A diferença é exatamente o valor do frete!")
        print("O usuário está incluindo o frete no total de compra!")
        
        # Recalcular rentabilidade com frete
        total_compra_com_frete = total_compra_sistema + freight_value_total
        total_venda = 6493.75056
        
        rentabilidade_com_frete = (total_venda - total_compra_com_frete) / total_compra_com_frete
        
        print(f"\nRentabilidade com frete incluído:")
        print(f"({total_venda:.2f} - {total_compra_com_frete:.2f}) / {total_compra_com_frete:.2f} = {rentabilidade_com_frete:.6f}")
        print(f"Rentabilidade: {rentabilidade_com_frete*100:.2f}%")
        
        # Comparar com a rentabilidade esperada pelo usuário
        rentabilidade_esperada = 0.7838435255859797
        diferenca_rentabilidade = abs(rentabilidade_com_frete - rentabilidade_esperada)
        
        print(f"\nComparação:")
        print(f"Rentabilidade calculada com frete: {rentabilidade_com_frete:.6f} = {rentabilidade_com_frete*100:.2f}%")
        print(f"Rentabilidade esperada usuário: {rentabilidade_esperada:.6f} = {rentabilidade_esperada*100:.2f}%")
        print(f"Diferença: {diferenca_rentabilidade:.6f}")
        
        if diferenca_rentabilidade < 0.000001:
            print("🎯 PROBLEMA RESOLVIDO! O frete deve ser incluído no cálculo de rentabilidade!")
        else:
            print("❌ Ainda há uma pequena diferença")
    else:
        print("❌ A diferença não corresponde ao frete")
        
        # Outras hipóteses
        print(f"\n=== OUTRAS HIPÓTESES ===")
        
        # Hipótese: Diferença por kg
        peso_total = 2020  # 2 itens × 1010kg cada
        diferenca_por_kg = diferenca / peso_total
        print(f"Diferença por kg: R$ {diferenca_por_kg:.6f}")
        
        # Hipótese: Percentual sobre o total
        percentual_diferenca = (diferenca / total_compra_sistema) * 100
        print(f"Diferença como percentual: {percentual_diferenca:.2f}%")
        
        # Hipóteses comuns
        if abs(percentual_diferenca - 15.92) < 0.1:
            print("Possível: Diferença relacionada a impostos ou taxas")
        elif abs(diferenca_por_kg - 0.25) < 0.01:
            print("Possível: Taxa fixa por kg")

if __name__ == "__main__":
    investigar_diferenca_500()