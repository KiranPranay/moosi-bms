# Research notes — Review-1

Checked on 29 September 2026. Every citation below was confirmed against
Crossref (`api.crossref.org/works/<DOI>`), and the summaries in the literature
survey come from the paper abstracts as published in OpenAlex. None of the ten
is retracted.

The engineering values used in the deck (thresholds, pin map, parts) come from
[`../../current-architecture.md`](../../current-architecture.md), revision 2.1,
not from these papers.

---

## References used in the deck

Seven of the ten are IEEE publications.

| # | Citation | DOI | IEEE | Abstract checked |
| --- | --- | --- | --- | --- |
| 1 | X. Feng, M. Ouyang, X. Liu, L. Lu, Y. Xia, and X. He, "Thermal runaway mechanism of lithium ion battery for electric vehicles: A review," *Energy Storage Mater.*, vol. 10, pp. 246–267, Jan. 2018. | 10.1016/j.ensm.2017.05.013 | — | No (see note) |
| 2 | H. Rahimi-Eichi, U. Ojha, F. Baronti, and M.-Y. Chow, "Battery management system: An overview of its application in the smart grid and electric vehicles," *IEEE Ind. Electron. Mag.*, vol. 7, no. 2, pp. 4–16, Jun. 2013. | 10.1109/MIE.2013.2250351 | Yes | Yes |
| 3 | B. Xu, L. Kong, G. Wen, and M. G. Pecht, "Protection devices in commercial 18650 lithium-ion batteries," *IEEE Access*, vol. 9, pp. 66687–66695, 2021. | 10.1109/ACCESS.2021.3075972 | Yes | Yes |
| 4 | X. Hu, K. Zhang, K. Liu, X. Lin, S. Dey, and S. Onori, "Advanced fault diagnosis for lithium-ion battery systems: A review of fault mechanisms, fault features, and diagnosis procedures," *IEEE Ind. Electron. Mag.*, vol. 14, no. 3, pp. 65–91, Sep. 2020. | 10.1109/MIE.2020.2964814 | Yes | Yes |
| 5 | X. Zhang, S. Chen, J. Zhu, and Y. Gao, "A critical review of thermal runaway prediction and early-warning methods for lithium-ion batteries," *Energy Mater. Adv.*, vol. 4, Art. no. 0008, 2023. | 10.34133/energymatadv.0008 | — | Yes |
| 6 | Z. Sun *et al.*, "An online data-driven fault diagnosis and thermal runaway early warning for electric vehicle batteries," *IEEE Trans. Power Electron.*, vol. 37, no. 10, pp. 12636–12646, Oct. 2022. | 10.1109/TPEL.2022.3173038 | Yes | Yes |
| 7 | O. Ojo, H. Lang, Y. Kim, X. Hu, B. Mu, and X. Lin, "A neural network based method for thermal fault detection in lithium-ion batteries," *IEEE Trans. Ind. Electron.*, vol. 68, no. 5, pp. 4068–4078, May 2021. | 10.1109/TIE.2020.2984980 | Yes | Yes |
| 8 | Q. Chen, Y. He, N. Fang, and G. Yu, "A combined data-driven and model-based algorithm for accurate battery thermal runaway warning," *Sensors*, vol. 24, no. 15, Art. no. 4964, Jul. 2024. | 10.3390/s24154964 | — | Yes, and full text |
| 9 | X. Lin *et al.*, "Online parameterization of lumped thermal dynamics in cylindrical lithium ion batteries for core temperature estimation and health monitoring," *IEEE Trans. Control Syst. Technol.*, vol. 21, no. 5, pp. 1745–1755, Sep. 2013. | 10.1109/TCST.2012.2217143 | Yes | Yes |
| 10 | A. Adhikaree, T. Kim, J. Vagdoda, A. Ochoa, P. J. Hernandez, and Y. Lee, "Cloud-based battery condition monitoring platform for large-scale lithium-ion battery energy storage systems using internet-of-things (IoT)," in *Proc. IEEE ECCE*, 2017, pp. 1004–1009. | 10.1109/ECCE.2017.8095896 | Yes | Yes |

IEEE style lists every author up to six and uses *et al.* beyond that. Papers 6
and 9 have eight authors each.

---

## Corrections made to the earlier references

These were in the zeroth-review deck and the first version of the first-review
deck. Both decks are now corrected.

- **Zhang et al. (ref. 5)** has exactly four authors. It was cited as
  "X. Zhang, S. Chen, J. Zhu *et al.*"; the fourth author, Y. Gao, is now listed.
- **Chen et al. (ref. 8) and the 1 °C/s figure.** This figure was previously
  described as the paper's warning threshold and as the basis of this project's
  trip limit. Both were wrong. The full text (Section 4.1, *Data Source*) says:

  > The criteria for determining thermal runaway is as follows: (A) The test
  > object experiences a voltage drop. (B) The temperature at the monitoring
  > point reaches the battery's protection operating temperature, which is
  > 60 °C. (C) The temperature rising rate at the monitoring point, dT/dt, is
  > greater than or equal to 1 °C/s. When both (A) and (C) or (B) and (C) occur,
  > it is considered that a thermal runaway has occurred.

  So 1 °C/s is the rule the authors used to decide that runaway **had already
  happened** in their abuse tests. It is not an early-warning limit. The
  project's own limits are far lower, and are set in `current-architecture.md`
  (warning at 0.5 °C/min held for 30 s, trip at 1.0 °C/min held for 10 s).
- **Habib et al.** has a serial comma in its title: "Constraints, Challenges,
  and Recommendations".
- **Habib et al. (zeroth review only)** is not carried into Review-1. Its place
  as the general BMS review is taken by the IEEE overview in ref. 2.

---

## What each paper supports in the deck

| Ref | Used for |
| --- | --- |
| 1 | Thermal runaway is a chain of heat-producing reactions |
| 2 | A BMS must estimate state *and* protect against hazardous conditions |
| 3 | The CID and top vent are the only protection fitted in every 18650; the rest is optional |
| 4 | Sensor and actuator faults are real fault classes — hence plausibility checks and fail-open relays |
| 5 | Early-warning methods fall into electrochemical, big-data and AI groups |
| 6–8 | Existing warning methods work, but need many cells, trained models or fitted parameters |
| 9 | Only the surface temperature can be measured; the core can be hotter |
| 10 | Cloud monitoring depends on the network, so protection must stay local |

---

## Notes and limits of this check

- **Feng et al. (ref. 1)** — the abstract is not in any open API (the publisher
  withholds it), so its survey row is limited to what the title and the paper's
  widely known subject support: the mechanism of thermal runaway. The citation
  itself is confirmed.
- **Search scope.** Within this search, no well-cited IEEE paper was found that
  uses a plain regression-based dT/dt limit on surface temperature as an early
  warning on a low-cost controller. That is the gap the deck states, and it is
  stated as a gap in the papers reviewed, not a claim that no such work exists
  anywhere.
- **Candidates considered but not used:** Hannan *et al.*, IEEE Access 2018
  (10.1109/ACCESS.2018.2817655); Omariba *et al.*, IEEE Access 2019
  (10.1109/ACCESS.2019.2940090, cell balancing); Lyu *et al.*, IEEE TIE 2022
  (10.1109/TIE.2021.3062267, impedance-based warning). An ESP32 conference paper
  was also found but not used, because its abstract reads as machine-paraphrased.
- Citation counts change over time and differ between databases, so they are
  not quoted in the deck.

---

## Component facts carried over from the earlier notes

- **ESP32 ADC** (Espressif ESP-IDF guide): 12-bit SAR ADC; ADC1 is GPIO32–39;
  ADC2 is shared with the Wi-Fi radio, so every analogue input stays on ADC1.
  <https://docs.espressif.com/projects/esp-idf/en/v4.4/esp32/api-reference/peripherals/adc.html>
- **IS 16046 (Part 2):2018**, identical to IEC 62133-2:2017, is the Indian
  safety standard for sealed portable lithium cells. It was cited in the zeroth
  review; no compliance or certification is claimed.
