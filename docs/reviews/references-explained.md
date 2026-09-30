# References Used in My Review Presentations

**Muskan Sulathana** · Roll No. 23WH1A0208 · Guide: Dr. M. Rupesh, Associate Professor, EEE Department
Predictive Thermal Battery Management System for Li-ion Battery Packs · 30 September 2026

My first review presentation cites ten sources, and my zeroth review cites two more. This document goes through each one and says what I took from it and where it appears in my slides.

The numbers [1] to [10] match the References slides of the first review. Seven of the ten are IEEE publications. I checked every paper against its publisher record on Crossref, and wherever the abstract is openly available, I read it before writing the paper's row in the Literature Survey. Every paper below has a DOI link, so the original can be opened directly.

## At a glance

| Ref | Paper | What I took from it | Where it appears |
| --- | --- | --- | --- |
| [1] | Feng et al., 2018 | Thermal runaway is a chain of heat-producing reactions | Literature Survey, Problem Analysis |
| [2] | Rahimi-Eichi et al., 2013 (IEEE) | A BMS must both estimate the battery's state and protect it | Literature Survey |
| [3] | Xu et al., 2021 (IEEE) | An 18650 cell's own protection is a last resort, not monitoring | Literature Survey |
| [4] | Hu et al., 2020 (IEEE) | Sensors and switches can fail, not only cells | Literature Survey, Research Gap |
| [5] | Zhang et al., 2023 | Early-warning methods need models, big data or AI | Literature Survey, Problem Analysis |
| [6] | Sun et al., 2022 (IEEE) | Early warning by comparing many cells | Literature Survey, Problem Analysis |
| [7] | Ojo et al., 2021 (IEEE) | Thermal faults found with a trained neural network | Literature Survey, Problem Analysis |
| [8] | Chen et al., 2024 | Warned 25 minutes early, but needs training and fitting | Literature Survey, Problem Analysis |
| [9] | Lin et al., 2013 (IEEE) | Only the surface temperature can be measured; the core is hotter | Literature Survey, Problem Analysis |
| [10] | Adhikaree et al., 2017 (IEEE) | Cloud monitoring depends on the network | Literature Survey, Problem Analysis |
| Z4 | Habib et al., 2023 | What a BMS does and its open problems | Zeroth review only |
| Z5 | IS 16046 (Part 2) : 2018 | The Indian safety standard for lithium cells | Zeroth review only |

## [1] Feng et al., 2018

X. Feng, M. Ouyang, X. Liu, L. Lu, Y. Xia, and X. He, “Thermal runaway mechanism of lithium ion battery for electric vehicles: A review,” *Energy Storage Materials*, vol. 10, pp. 246–267, 2018. [doi:10.1016/j.ensm.2017.05.013](https://doi.org/10.1016/j.ensm.2017.05.013)

**What the paper is about.** It is a review of how thermal runaway happens inside a lithium-ion cell. It is one of the most cited papers on the subject, with more than 4,000 citations.

**What I took from it.** Thermal runaway is not one event. It is a chain of heat-producing reactions inside the cell, where each reaction heats the cell and starts the next one. That is why a cell can get worse on its own once it starts heating.

**Where it appears.** First review: Literature Survey row [1], and the first point of Problem Analysis. Zeroth review: Literature Survey row [1].

The publisher does not make this paper's abstract openly available, so I have used only the main idea above and nothing more detailed.

## [2] Rahimi-Eichi et al., 2013 (IEEE)

H. Rahimi-Eichi, U. Ojha, F. Baronti, and M.-Y. Chow, “Battery management system: An overview of its application in the smart grid and electric vehicles,” *IEEE Industrial Electronics Magazine*, vol. 7, no. 2, pp. 4–16, Jun. 2013. [doi:10.1109/MIE.2013.2250351](https://doi.org/10.1109/MIE.2013.2250351)

**What the paper is about.** It is an overview of what a battery management system has to do in electric vehicles and the smart grid. It points to the Boeing 787 battery incidents as a reason why better battery management matters.

**What I took from it.** A BMS has two jobs. It must measure and estimate the state of the battery, such as its state of charge and state of health. It must also protect the battery from hazardous operating conditions. The paper focuses mostly on the first job, and says little about warning early from temperature.

**Where it appears.** First review: Literature Survey row [2].

## [3] Xu et al., 2021 (IEEE)

B. Xu, L. Kong, G. Wen, and M. G. Pecht, “Protection devices in commercial 18650 lithium-ion batteries,” *IEEE Access*, vol. 9, pp. 66687–66695, 2021. [doi:10.1109/ACCESS.2021.3075972](https://doi.org/10.1109/ACCESS.2021.3075972)

**What the paper is about.** The authors took apart four commercial 18650 cells and compared the protection devices inside them.

**What I took from it.** Only two protection devices are fitted in every 18650 cell: the current interrupt device and the top vent. The others, such as the positive temperature coefficient (PTC) element, the bottom vent and a protection circuit, are optional. These devices are the cell's last resort. They do not monitor the pack or give any early warning, so a pack still needs its own protection outside the cells.

**Where it appears.** First review: Literature Survey row [3].

## [4] Hu et al., 2020 (IEEE)

X. Hu, K. Zhang, K. Liu, X. Lin, S. Dey, and S. Onori, “Advanced fault diagnosis for lithium-ion battery systems: A review of fault mechanisms, fault features, and diagnosis procedures,” *IEEE Industrial Electronics Magazine*, vol. 14, no. 3, pp. 65–91, Sep. 2020. [doi:10.1109/MIE.2020.2964814](https://doi.org/10.1109/MIE.2020.2964814)

**What the paper is about.** It reviews the faults that can happen in a lithium-ion battery system, how each one shows up, and how it can be diagnosed.

**What I took from it.** Faults come in three kinds: faults inside the battery, sensor faults and actuator faults. A sensor or a switch can fail, not only a cell. This is why my design checks that every sensor reading is believable, and why both relays open if the controller or a sensor fails. The paper is a review only, and does not build or test a low-cost system.

**Where it appears.** First review: Literature Survey row [4], and the second point of Research Gap.

## [5] Zhang et al., 2023

X. Zhang, S. Chen, J. Zhu, and Y. Gao, “A critical review of thermal runaway prediction and early-warning methods for lithium-ion batteries,” *Energy Material Advances*, vol. 4, Art. no. 0008, 2023. [doi:10.34133/energymatadv.0008](https://doi.org/10.34133/energymatadv.0008)

**What the paper is about.** It reviews the methods people have proposed to predict thermal runaway and warn about it early, with the strengths and weaknesses of each.

**What I took from it.** Early-warning methods fall into three groups: methods based on battery electrochemistry, methods based on big-data analysis, and artificial-intelligence methods. All three depend on detailed models, large amounts of data or trained networks. None of them is a simple check that a low-cost controller on the pack can run by itself.

**Where it appears.** First review: Literature Survey row [5], and the second point of Problem Analysis. Zeroth review: Literature Survey row [2].

## [6] Sun et al., 2022 (IEEE)

Z. Sun, Z. Wang, P. Liu, Z. Qin, Y. Chen, Y. Han, P. Wang, and P. Bauer, “An online data-driven fault diagnosis and thermal runaway early warning for electric vehicle batteries,” *IEEE Transactions on Power Electronics*, vol. 37, no. 10, pp. 12636–12646, Oct. 2022. [doi:10.1109/TPEL.2022.3173038](https://doi.org/10.1109/TPEL.2022.3173038)

**What the paper is about.** It finds the cell that is heading for thermal runaway before it happens, using the voltage and temperature data a vehicle already records.

**What I took from it.** The method compares cells with each other, using the discrete Fréchet distance and the local outlier factor. It was tested on real data from electric vehicles with and without thermal runaway, and it gave fewer false diagnoses than methods that watch only one quantity. Because it looks for the one cell that behaves differently from the rest, it suits large packs with many cells, not a four-cell pack like mine.

**Where it appears.** First review: Literature Survey row [6], and the second point of Problem Analysis.

On my slide this appears as “Sun et al.” because the paper has eight authors, and IEEE style shortens lists of more than six.

## [7] Ojo et al., 2021 (IEEE)

O. Ojo, H. Lang, Y. Kim, X. Hu, B. Mu, and X. Lin, “A neural network based method for thermal fault detection in lithium-ion batteries,” *IEEE Transactions on Industrial Electronics*, vol. 68, no. 5, pp. 4068–4078, May 2021. [doi:10.1109/TIE.2020.2984980](https://doi.org/10.1109/TIE.2020.2984980)

**What the paper is about.** It detects thermal faults in a cell using a neural network.

**What I took from it.** A long short-term memory (LSTM) network predicts what the cell's surface temperature should be. When the real reading moves too far from the prediction, the gap is flagged as a fault. The method adapts to different cell types and can retrain itself while running. But it needs the network to be trained and retrained, which is heavy work for a low-cost microcontroller.

**Where it appears.** First review: Literature Survey row [7], and the second point of Problem Analysis.

## [8] Chen et al., 2024

Q. Chen, Y. He, N. Fang, and G. Yu, “A combined data-driven and model-based algorithm for accurate battery thermal runaway warning,” *Sensors*, vol. 24, no. 15, Art. no. 4964, Jul. 2024. [doi:10.3390/s24154964](https://doi.org/10.3390/s24154964)

**What the paper is about.** It warns about thermal runaway by combining a data-driven part with a model-based part.

**What I took from it.** K-Means clustering picks out unusual points in the battery data, and the Bernardi heat equation estimates how the battery temperature should behave. The two results are weighted and combined. The method warned 25 minutes before thermal runaway, with fewer false alarms. But it needs training data and fitted parameters before it can be used.

**About the 1 °C per second figure.** This paper is often quoted for a limit of 1 °C per second. In the paper, that figure is part of the rule the authors used in their tests to decide that thermal runaway *had already happened*: the temperature rising at 1 °C per second or faster, together with a voltage drop or the cell reaching 60 °C. It is not an early-warning limit. An early warning has to act well before this point, and that is what my slide says.

**Where it appears.** First review: Literature Survey row [8], and the second point of Problem Analysis. Zeroth review: Literature Survey row [3].

## [9] Lin et al., 2013 (IEEE)

X. Lin, H. E. Perez, J. B. Siegel, A. G. Stefanopoulou, Y. Li, R. D. Anderson, Y. Ding, and M. P. Castanier, “Online parameterization of lumped thermal dynamics in cylindrical lithium ion batteries for core temperature estimation and health monitoring,” *IEEE Transactions on Control Systems Technology*, vol. 21, no. 5, pp. 1745–1755, Sep. 2013. [doi:10.1109/TCST.2012.2217143](https://doi.org/10.1109/TCST.2012.2217143)

**What the paper is about.** It estimates the temperature at the core of a cylindrical cell from the temperature measured on its surface.

**What I took from it.** Only the surface temperature of a battery can be measured, while the core can be hotter and is more critical. The authors estimate the core temperature with an adaptive observer that learns the cell's thermal parameters while it runs. They tested it on a 2.3 Ah 26650 lithium iron phosphate cell, not an 18650 pack. For my project this means the thermistors on the cell surfaces always read cooler than the inside of the cells.

**Where it appears.** First review: Literature Survey row [9], and the first point of Problem Analysis.

On my slide this appears as “Lin et al.” because the paper has eight authors.

## [10] Adhikaree et al., 2017 (IEEE)

A. Adhikaree, T. Kim, J. Vagdoda, A. Ochoa, P. J. Hernandez, and Y. Lee, “Cloud-based battery condition monitoring platform for large-scale lithium-ion battery energy storage systems using internet-of-things (IoT),” in *Proc. IEEE Energy Conversion Congress and Exposition (ECCE)*, 2017, pp. 1004–1009. [doi:10.1109/ECCE.2017.8095896](https://doi.org/10.1109/ECCE.2017.8095896)

**What the paper is about.** It is a platform that monitors large battery storage systems through the cloud.

**What I took from it.** IoT parts in each battery module collect data and send it over a wireless link to the cloud, where it is stored, analysed and shown. The authors tested the idea with Raspberry Pi boards and Google Cloud, where the cell states were worked out. The analysis depends on the cloud and the network. In my design the Wi-Fi dashboard is for monitoring only, and all of the protection runs on the board, so it keeps working when Wi-Fi is lost.

**Where it appears.** First review: Literature Survey row [10], and the second point of Problem Analysis.

## Two more sources used only in the zeroth review

### Habib et al., 2023 (zeroth review [4])

A. K. M. A. Habib, M. K. Hasan, G. F. Issa, D. Singh, S. Islam, and T. M. Ghazal, “Lithium-ion battery management system for electric vehicles: Constraints, challenges, and recommendations,” *Batteries*, vol. 9, no. 3, Art. no. 152, 2023. [doi:10.3390/batteries9030152](https://doi.org/10.3390/batteries9030152)

**What I took from it.** A battery management system covers voltage and current monitoring, charge estimation, protection, balancing, thermal management and data storage. The paper also compares cell-balancing circuits and lists the problems that still need work. It is a review, and does not build anything.

**Where it appears.** Zeroth review: Literature Survey row [4]. In the first review I used the IEEE overview [2] for this general background instead.

### IS 16046 (Part 2) : 2018 (zeroth review [5])

IS 16046 (Part 2) : 2018 / IEC 62133-2 : 2017, *Secondary cells and batteries containing alkaline or other non-acid electrolytes — Safety requirements for portable sealed secondary cells, and for batteries made from them, for use in portable applications — Part 2: Lithium systems.*

**What I took from it.** This is the Indian safety standard for sealed portable lithium cells, and it is the same as the international standard IEC 62133-2. It sets out abuse tests such as external short circuit, overcharging, crushing, dropping and heating. I used it to show which abuse conditions my design is aimed at. I do not claim that my pack is certified to it.

**Where it appears.** Zeroth review: Literature Survey row [5].
