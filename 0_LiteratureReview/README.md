# Literature Review

Approaches or solutions that have been tried before on similar projects.

**Summary of Each Work**:

- **Source 1**: [New Kinematic Model of the Early Opening of the
Equatorial Atlantic Realm (Lesourd-Laux et al., 2025)]

  - **[Link](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024TC008713?af=R)**  
  
  - **Objective**:  
This study aims to develop a new kinematic model for the early opening of the Equatorial Atlantic Ocean, addressing challenges posed by limited magnetic data and complex fracture zones. Its goal is to re-evaluate tectonic settings, including continental margins and the Cretaceous Jurassic Line (CJL). The research also intends to improve understanding of the triple junction's evolution between the Equatorial Atlantic, Central Atlantic, and proto-Caribbean oceans, and its implications for Lesser Antilles Arc subduction hazards.

  - **Methods**:  
The researchers used GPlates and PyGPlates software to create their kinematic reconstruction. They built upon the Moulin et al. (2010) South Atlantic model, updating timing of rotations based and adjusting continental block boundaries in northern South America. The methods used were as follows:  
  
    a) Gravity and bathymetry data to identify major tectonic features like fracture zones (FZs) and continental margins  

    b) Multi-Channel Seismic (MCS) and structural data to define continental margin types and their boundaries (COBs)  

    c) Gravity-derived Moho depth and global sedimentary thickness maps for inland plate boundaries  
  
    The study used identified FZs, especially the Cretaceous Jurassic Line (CJL), to reconstruct the ocean's opening direction and initial continental fits. Seismic         data helped interpret the CJL's structure and sedimentary infill. The model proposes a two-phase rifting process, with distinct plate movements in each phase,           constrained by known timings and South Atlantic rotations.

  - **Outcomes**:   
The study presents a new kinematic model for the Equatorial Atlantic, identifying two regions divided by the St Paul Fracture Zone. It outlines a two-phase rifting history: the first phase involved strike-slip movement between West Africa and the Guyana block during the Early Cretaceous, while the second phase saw northward movements leading to oblique rifting. The Cretaceous Jurassic Line (CJL) is identified as an Early Cretaceous transform fault that later became a rift zone, with chaotic sediments from this rifting. Additionally, the Amazon basins acted as a boundary for early plate movements. The model suggests significant implications for the Lesser Antilles Arc subduction zone, including revised oceanic boundaries and the subduction of Equatorial Atlantic crust around 3 million years ago, linked to intermediate earthquakes due to dehydration in the lithosphere.  
  
  - **Relation to the Project**:  
This reference is a key part of my internship, as it helps define a new understanding of the North American-South American (NA-SA) plate boundary. The CJL offers a fresh look at how the North American, South American, and African plates separated. My goal during this internship is to support and prove this idea.
  
- **Source 2**: [Residual Bouguer satellite gravity anomalies reveal basement grain and structural elements of the Vøring Margin, off Norway (Christian Berndt, 2002)]

  - **[Link](https://oceanrep.geomar.de/id/eprint/19128/)**

  - **Objective**:  
The objective of this study was to map and interpret deep crustal and basement structures of the Vøring Margin, offshore Norway, by generating a high-resolution residual Bouguer gravity anomaly map from satellite gravity and bathymetric data. The aim is to improve understanding of regional geological features such as basins, highs, and faults, and to support seismic interpretation in a key hydrocarbon exploration area.

  - **Methods**:  
     a) Acquired satellite-derived free-air gravity data and combined it with ship-based bathymetric measurements.  

     b) Applied a 3D Bouguer correction to account for the gravitational effect of water, using a sediment–water density contrast of 1400 kg/m³, deemed appropriate for Vøring Basin conditions.  

     c) Filtered the gravity data to isolate wavelength bands between 10 and 190 km, which enhance signals from intermediate to deep crustal structures.

     d) Interpreted the residual gravity anomalies in relation to known geological features and potential new structural elements.
    
  - **Outcomes**:  
The residual gravity anomaly map revealed strong negative anomalies over deep sedimentary basins (e.g., Hel Graben, Rås Basin) and strong positive anomalies over basement highs and metamorphic complexes (e.g., Sandflesa High, Utgard High, Gjallar Ridge). It highlighted two dominant structural trends—SW–NE and N–S—and confirmed known elements while uncovering new complexities, such as internal variations within the Gjallar Ridge. Tertiary domes were associated with negative anomalies, and the study confirmed that satellite-derived gravity maps are effective tools for regional structural interpretation.

  - **Relation to the Project**:  
The article describes a very similar processing methodology to the one used during this project, giving a valuable reference and help in deeper understanding of the whole process.

- **Source 3**: [Tools for Edge Detection of Gravity Data: Comparison and Application to Tectonic Boundary Mapping in the Molucca Sea (Liu et al., 2022)]

  - **[Link](https://link.springer.com/article/10.1007/s10712-023-09784-x)**
  
  - **Objective**:  
The objective of this article is to systematically evaluate and compare the performance of 28 edge detection techniques used to interpret gravity data for identifying geological boundaries. The goal was to determine which methods are most effective for resolving complex subsurface structures, particularly in noisy data environments, and to apply these insights to real-world tectonic analysis in the Molucca Sea.

  - **Methods**:  
The study reviewed existing edge detection techniques and tested them on synthetic 2.5D and 3D gravity models with known boundaries, both with and without added noise. Detectors were grouped into three categories: sequential combination methods, ratio-based methods, and mixed-class methods. Their performance was assessed in terms of boundary resolution, noise resistance, and reliability. The most effective techniques were then applied to actual gravity data from the Molucca Sea, integrated with seismic information (earthquake locations and focal mechanisms) to interpret regional tectonics.

  - **Outcomes**:  
The study found that edge detectors vary widely in performance; traditional methods like THDR and ASA showed poor resolution, while first-derivative-based filters like VDR and TA often introduced false boundaries in complex zones. Mixed-class detectors such as LTHG, EHGA, and SF consistently outperformed others, offering sharper boundary definition, better amplitude balancing between shallow and deep sources, and greater resistance to noise. However, even these methods were sensitive to data noise, highlighting the trade-off between noise reduction (e.g., via upward continuation) and resolution. Application to the Molucca Sea revealed four deep tectonic boundaries and five earthquake depth zones, suggesting tectonic control from both multi-plate subduction and the PKMSSF fault system.  
                                       
  - **Relation to the Project**:  
This study is a good reference for a comparative approach of different edge detection methods, identifying the possible limitations, and deepening the understanding of edge detection in general.

    <img src="liu_et_al_2022.png" alt="Gravity Anomaly Map" width="450"/>
    
- **Source 4**: [AnomalyLLM: Few-Shot Anomaly Edge Detection in Dynamic Graphs with Large Language Models (Liu et al. (2024)]

  - **[Link](https://www.computer.org/csdl/proceedings-article/icdm/2024/066800a785/24w4taFG1UI)**
  - **Objective**:  
The objective of this study is to develop a novel few-shot anomaly detection method — AnomalyLLM — that can identify evolving and rare anomalous edges in dynamic graphs with minimal labeled data, overcoming the limitations of existing approaches which typically require abundant labels or only handle simple anomalies.

  - **Methods**:  
  AnomalyLLM integrates Large Language Models (LLMs) with graph-based learning through three main components:  

    1) Dynamic-aware Contrastive Pretraining: Constructs temporal and structural subgraphs around each edge and uses a contrastive learning objective to distinguish            normal vs. anomalous patterns.  

    2) Reprogramming-based Modality Alignment: Bridges the gap between graph embeddings and LLMs (which work with text) by reprogramming edge features into a format            interpretable by LLMs, using text-based prototypes and pseudo-labeling techniques.  

    3) In-Context Learning (ICL) for Few-Shot Detection: Constructs prompt templates for the LLM using a few labeled examples of a specific anomaly type, allowing the          model to classify new edges as anomalies using just those examples without fine-tuning.

  - **Outcomes**:  
AnomalyLLM significantly outperformed traditional methods in few-shot settings across four datasets, achieving AUC scores over 80% even with only 1–5 labeled samples per anomaly type. The model is anomaly type-agnostic, does not require fine-tuning of the LLM itself, and is computationally efficient at inference. Ablation studies validated the contribution of each proposed module to its overall performance.

  - **Relation to the Project**:  
??

- **Source 5**: [Tectonic reevaluation of West Cameroon domain: Insights from high-resolution gravity models and advanced edge detection methods (Yasmine et al., 2024)]

  - **[Link](https://www.sciencedirect.com/science/article/pii/S0264370724000449)**

  - **Objective**:  
The objective of this study was to reassess the geological and tectonic structure of the West Cameroon region—particularly the Cameroon Volcanic Line (CVL)—using high-resolution satellite gravity data, in order to provide clearer, more accurate mapping of subsurface features and reduce uncertainties from earlier studies.

   - **Methods**:  
The study utilized the SGG-UGM-2 gravity model, a highly detailed satellite gravity dataset. Researchers applied several advanced edge detection techniques to this data to identify and delineate underground structures: 

      a) **Balanced Horizontal Gradient (BHG)**: Used to highlight subsurface boundaries with high accuracy and low false detection.

      b) **Tilt Angle of Horizontal Gradient (TAHG)** and **Improved TAHG (ImpTAHG)**: Provided enhanced boundary resolution.

      c) **Tilt Depth**: Estimated the depth of geological sources.
    The gravity data were decomposed into regional (deep) and residual (shallow) components to isolate structures at different depths.

  - **Outcomes**:  
The study mapped 333 lineaments, including newly identified NNW–SSE structures, and refined the understanding of five dominant structural directions. Key features such as Lakes Nyos and Monoun were confirmed to sit on major fractures. It also accurately mapped strike-slip faults (Bao, Bomana, Tiko, Ekona) and the boundaries of Mount Cameroon. The findings demonstrate overcompensated topography and active tectonic processes in the region. The BHG filter proved particularly reliable for deep structural interpretation.

  - **Relation to the Project**:

- **Source 6**: [Volcanic influence during the formation of a transform marginal plateau: Insights from wide-angle seismic data along the northwestern Demerara Plateau (Padron et al., 2022)]

  - **[Link](https://www.sciencedirect.com/science/article/pii/S0040195122003869)**

  - **Objective**:  
This study looks at how the Demerara Plateau, located offshore Suriname and French Guiana, was formed. It focuses on how volcanism and transform movement helped shape this type of feature, known as a Transform Marginal Plateau (TMP). The goal is to better understand how these plateaus form, especially where two ocean basins of different ages meet, like the Central and Equatorial Atlantic.

   - **Methods**:  
Researchers used wide-angle seismic (WAS) data and gravity data to study the deep structure of the crust. The data comes from a 2016 survey with two main profiles (MAR03 and MAR04). They used:  

     a) Wide-angle seismic data from ocean-bottom seismometers (OBS)  
     b) Seismic reflection data to map sediment layers  
     c) A modeling program called Rayinvr  
     d) Gravity data to help estimate rock densities  
     e) A method that builds the model layer by layer, using both velocity and reflection changes  
The crust was divided into seven domains (A–G), each with different thickness, rock types, and tectonic history.    

  - **Outcomes**:  
The Demerara Plateau has a thick crust (up to 30 km) with high seismic velocities (>7 km/s), suggesting a mix of volcanic flows and continental material. The structure includes seaward-dipping reflectors (SDRs) and shows strong magmatic influence, possibly from a hotspot. The Moho reaches 37 km depth near the continent and thins sharply toward the ocean, with some areas showing very thin crust (2–3 km) or exposed serpentinized mantle. Crustal domains vary across the plateau, reflecting different formation phases linked to Jurassic rifting and Cretaceous transform faulting. The study supports the idea that TMPs form where rifting slows or stops at transform margins, causing heat buildup and volcanic activity.  

  - **Relation to the Project**:  
This paper is an important reference for gravity and seismic data. It provides useful data on crustal thickness and structure, which can be compared with other parts of the Equatorial Atlantic. The detailed seismic and gravity models help confirm that TMPs like the Demerara Plateau are key features when studying how continents break apart and how ocean basins open. It’s a helpful reference for understanding the deeper structure of the North American–South American plate boundary, as well as support the hypotheses we're trying to explore in this project.

- **Source 7**: [Along-Arc Heterogeneity in Local Seismicity across the Lesser Antilles Subduction Zone from a Dense Ocean-Bottom Seismometer Network (Bie et al., 2019)]

  - **[Link](https://pubs.geoscienceworld.org/ssa/srl/article-abstract/91/1/237/575207/Along-Arc-Heterogeneity-in-Local-Seismicity-across?redirectedFrom=fulltext)**

  - **Objective**:  
This study aimed to map seismic activity across the entire Lesser Antilles subduction zone with greater detail than ever before. The goals were to understand how fluids influence earthquake patterns, improve seismic hazard assessments, and produce the first unified 1D velocity model for accurate earthquake locations. The research also explored the structure of the arc, mantle wedge, and subducting slab.

   - **Methods**:  
A temporary network of 34 ocean-bottom seismometers (OBSs) operated from March 2016 to May 2017, alongside permanent and temporary land stations. Researchers:

      a) Compiled a regional earthquake catalog from multiple sources
      b) Manually picked P- and S-wave arrivals for 502 events
      c) Selected 265 high-quality earthquakes for joint inversion of earthquake locations, velocity structure, and station corrections using VELEST
      d) Included 63 active-source shots to improve shallow velocity constraints
      e) Used the final 1D model to re-locate all manually picked events

  - **Outcomes**:  
The inversion resulted in an average crustal thickness of 27 km across the arc and back-arc. Deep intraslab earthquakes beneath Martinique and Dominica were linked to the subduction of fracture zones carrying water, supporting dehydration embrittlement as a key process. Unusual seismicity in the cold mantle wedge above ~65 km depth suggests active fluid pathways or rock hydration. A Mw 5.8 earthquake in 2017 occurred on a deep section of the plate interface, indicating a wider and deeper seismogenic zone than typically seen, with implications for larger possible earthquakes. The slab was found to dip more steeply than shown in global models. No large-scale slab tear was detected at 15° N; instead, a thickening of the Wadati–Benioff zone may mark the edge of a subducted fracture zone. Shallow seismicity and earthquake swarms suggest localized fluid activity. Seismicity was more intense in the northern part of the subduction zone.  

  - **Relation to the Project**:  
The paper delivers essential insights into regional seismicity and crustal structure, which are key to understanding earthquake generation and distribution in the Lesser Antilles subduction system, which can later be used as a reference in the report's discussion section.  

- **Source 8**: [Deep structure of the central Lesser Antilles Island Arc: Relevance for the formation of continental crust (Kopp et al., 2011)]

  - **[Link](https://www.sciencedirect.com/science/article/pii/S0012821X11000483)**

  - **Objective**:  
This study aimed to image the deep crustal and upper mantle structure of the central Lesser Antilles island arc, a region with limited existing seismic profiles. Goals included constraining the composition and thickness of the arc crust, understanding crust formation processes, and mapping the geometry of the forearc backstop and décollement zone.

   - **Methods**:  
A 280 km-long wide-angle seismic profile south of Guadeloupe was acquired using 44 ocean-bottom seismometers and a 5-element seismic source array. Coincident multichannel seismic (MCS) data covered the northeastern section. Researchers:  

      a) Used first-arrival travel time tomography (Korenaga et al., 2000) to build an initial velocity model from over 22,500 picks.  
      b) Applied pre-stack depth migration to MCS data using the tomography model to resolve upper crustal structure.  
      c) Conducted forward modeling with the Zelt & Smith (1992) method using 3,611 secondary arrivals (reflections from Moho, backstop, etc.) to refine the final structural       model.  

  - **Outcomes**:  
The seismic data reveal that the island arc crust beneath the central Lesser Antilles is composed of three distinct layers: a ~3 km thick volcanogenic upper crust with velocities below 3.0 km/s, a 10 km thick intermediate-to-felsic middle crust (5.5–6.8 km/s), and a 12 km thick plutonic lower crust with velocities up to 7.3 km/s. The Moho is located at an average depth of 28 km, and upper mantle velocities (~8.0 km/s) show no evidence of serpentinization.

  - **Relation to the Project**:  
This paper is a good reference for Moho depth in the Lesser Antilles zone, which will be useful to choose the right filter for gravity data.
