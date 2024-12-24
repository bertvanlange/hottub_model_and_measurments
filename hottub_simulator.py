import scipy
import scipy.conftest
import scipy.constants

# print(scipy.constants.Stefan_Boltzmann)

#This program will simulate the warming of the hottub with the oudside tempeture a
#it will take into acount the outside tempeture, and the losses of the tubb and the power of the stoves

opp_zijkand = 2.4*1*4
A_bovenkand = 2.4*2.4

opp_zijkand_stro = opp_zijkand*.5
opp_zijkand_houd = opp_zijkand*.5


opp_onderkand_stro_los = 
opp_onderkand_sto_baal = 

def convectie_warmte_opp(A_oppervlakte,T_water,T_lucht,h_convectie = 3):
    # convectie constande van water met een zijl er over heen zou tussen 2 en 4 zijn
    return h_convectie*A_oppervlakte*(T_water-T_lucht)

def starling_verlies(A_oppervlakte,T_water,T_lucht,ε_ = .5):
    # strealings verlies ->  Qstraling=ε⋅σ⋅Aoppervlak⋅(Twater4−Tlucht4)
    # ε: Emissiviteit van water (≈ 0,95) -> met zeil .5
    # σ: Stefan-Boltzmann-constante (5,67 × 10⁻⁸ W/m²·K⁴).
    SB_constante = scipy.constants.Stefan_Boltzmann
    temp_index = (T_water+273)^4 - (T_lucht+273)^4
    return SB_constante*ε_*A_oppervlakte*temp_index

def warmte_verlies_wand_bodem(A_oppervlakte,T_water,T_lucht,d,k):
    # Q = k*A(dT)/d
    # K = warmtegeleidingscoeficient = .15 w/(m*k) hout
    # 0,056 tro
    return k*A_oppervlakte*(T_water-T_lucht)/d


def totaal_verlies(t_buiten, t_water):
    W_convectie = convectie_warmte_opp(A_bovenkand,t_water,t_buiten)

    W_straling = starling_verlies(A_bovenkand,t_water,t_buiten)

    k_houd = .15
    W_houd = warmte_verlies_wand_bodem(opp_zijkand*.5,t_water,t_buiten,.02,k_houd)

    k_stro = .056
    W_stro_zijkand = warmte_verlies_wand_bodem(opp_zijkand*.5,t_water,t_buiten,.6,k_stro)

    W_stro_balen_onderkand = W_stro_zijkand

    opp_onderkand = (2.4-2*.5)*(2.4-2*.5)
    stro_dikte = .2
    W_stro_onderkand =  warmte_verlies_wand_bodem(opp_onderkand,t_water,t_buiten,stro_dikte,k_stro)

    totaal_verlies = W_convectie+W_straling+W_houd+W_stro_zijkand+W_stro_balen_onderkand+W_stro_onderkand

    return totaal_verlies

print(totaal_verlies(0,38))