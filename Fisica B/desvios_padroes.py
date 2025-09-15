import numpy as np
import pandas as pd


d_medidas = np.array([1.996, 1.995, 1.998, 1.996])
n = len(d_medidas)


sigma_inst_d = 0.005


d_media = np.mean(d_medidas)
sigma_d = np.std(d_medidas, ddof=1)
sigma_d_media = sigma_d / np.sqrt(n)
sigma_d_combinada = np.sqrt(sigma_d_media**2 + sigma_inst_d**2)

print(n)
print(f"--- Diâmetros (mm) ---")
print(f"Média (d): {d_media:.5f}")
print(f"Desvio Padrão (sigma_d): {sigma_d:.5f}")
print(f"Desvio Padrão da Média (sigma_d_media): {sigma_d_media:.5f}")
print(f"Incerteza Combinada (sigma_dc): {sigma_d_combinada:.5f}")


r_media = d_media / 2
sigma_r_combinada = sigma_d_combinada / 2


r2_media = r_media**2
sigma_r2_combinada = 2 * r_media * sigma_r_combinada

print(f"\n--- Raio e Raio^2 (mm e mm^2) ---")
print(f"Raio (r): {r_media:.5f} ± {sigma_r_combinada:.5f} mm")
print(f"Raio ao Quadrado (r^2): {r2_media:.5f} ± {sigma_r2_combinada:.5f} mm^2")


t_medidas = np.array([10.63, 10.35, 10.44, 10.35])
n_t = len(t_medidas)

sigma_inst_t = 0.01


t_media = np.mean(t_medidas)
sigma_t = np.std(t_medidas, ddof=1)
sigma_t_media = sigma_t / np.sqrt(n_t)
sigma_t_combinada = np.sqrt(sigma_t_media**2 + sigma_inst_t**2)

print(f"\n--- Tempos de Queda (s) ---")
print(f"Média (Δt): {t_media:.2f} ± {sigma_t_combinada:.2f} s")


delta_h_cm = 30.0
sigma_delta_h_cm = 0.05


r_media_cm = r_media / 10
sigma_r_combinada_cm = sigma_r_combinada / 10
t_media_s = t_media
sigma_t_combinada_s = sigma_t_combinada


D_medidas_cm = np.array([6.05, 6.06, 6.04])
D_media_cm = np.mean(D_medidas_cm)


v_lim_D = delta_h_cm / t_media_s
sigma_v_lim_D = abs(v_lim_D) * np.sqrt(
    (sigma_delta_h_cm / delta_h_cm) ** 2 + (sigma_t_combinada_s / t_media_s) ** 2
)


x = (9 * r_media_cm) / (2 * D_media_cm)
f = 1 + x + x**2


v_lim_inf = v_lim_D * f
sigma_v_lim_inf = sigma_v_lim_D * f

print(f"\n--- Velocidades e Correções (CGS) ---")
print(f"v_lim_D: {v_lim_D:.4f} ± {sigma_v_lim_D:.4f} cm/s")
print(x)
print(f"Fator de correção (f): {f:.4f} (adimensional)")
print(f"v_lim_inf: {v_lim_inf:.4f} ± {sigma_v_lim_inf:.4f} cm/s")


dados_finais = pd.DataFrame(
    {
        "r2_cm2": np.array([0.996, 2.519, 5.68]),
        "sigma_r2_cm2": np.array([0.005, 0.009, 0.021]),
        "v_inf_cms": np.array([2.8729, 7.71, 17.11]),
        "sigma_v_inf_cms": np.array([0.021, 0.11, 0.1]),
    }
)


pontos_para_ajuste = dados_finais.iloc[:5]


k = 299.312
sigma_k = 0.974

print("\n\n\n\n")


g_cgs = 978.64
rho_esf_cgs = 7.85
rho_flu_cgs = 0.886
sigma_rho_flu_cgs = 0.0005


eta = (2 * g_cgs) / (9 * k) * (rho_esf_cgs - rho_flu_cgs)
sigma_eta = (eta / k) * sigma_k

print(f"\n--- Resultados Finais ---")
print(f"Viscosidade Absoluta (η): {eta:.4f} ± {sigma_eta:.4f} P (g/cm·s)")


nu = eta / rho_flu_cgs

sigma_nu = nu * np.sqrt((sigma_eta / eta) ** 2 + (sigma_rho_flu_cgs / rho_flu_cgs) ** 2)
print(f"Viscosidade Cinemática (ν): {nu:.4f} ± {sigma_nu:.4f} St (cm²/s)")


dados_finais["f"] = (
    1
    + (9 * np.sqrt(dados_finais["r2_cm2"])) / (2 * D_media_cm)
    + ((9 * np.sqrt(dados_finais["r2_cm2"])) / (2 * D_media_cm)) ** 2
)
dados_finais["v_lim_D_cms"] = dados_finais["v_inf_cms"] / dados_finais["f"]
dados_finais["r_cm"] = np.sqrt(dados_finais["r2_cm2"])

dados_finais["Reynolds"] = (2 * dados_finais["v_lim_D_cms"] * dados_finais["r_cm"]) / nu
print("\n--- Número de Reynolds (adimensional) ---")
print(dados_finais[["r_cm", "v_lim_D_cms", "Reynolds"]].round(3))
