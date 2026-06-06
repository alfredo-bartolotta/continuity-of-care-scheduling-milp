**Key Findings**



**Overview**

This project evaluates the operational impact of continuity of care in outpatient physiotherapy scheduling.

The analysis compares three scenarios:

* Scenario A: continuity of care applied only to hand-based sessions;
* Scenario B: no continuity of care;
* Scenario C: continuity of care applied to all session types.



The results are based on synthetic instances and should be interpreted within the limits of the experimental setting.



**Operational Efficiency**

Operational efficiency is measured through global physiotherapist utilization. The results show that global utilization remains substantially unchanged across the three scenarios. This suggests that, under the tested conditions, introducing continuity-of-care constraints does not reduce the ability of the system to use available physiotherapist capacity.

This is an important result because continuity of care is often perceived as a possible source of rigidity. In this experimental setting, that rigidity does not translate into capacity waste.



**Service Effectiveness**

Service effectiveness is evaluated through:

* objective function value;
* percentage of patients scheduled;
* percentage of sessions scheduled.



Across the three scenarios, these indicators remain substantially stable. The objective function value does not decrease when continuity-of-care constraints are introduced, and the percentage of scheduled patients and sessions shows negligible variation. This suggests that continuity of care does not compromise the ability of the system to satisfy demand in the tested setting. The result is particularly relevant because the objective function prioritizes patients according to urgency and waiting time. Therefore, the model preserves both service coverage and priority-based allocation.



**Workload Distribution**

Workload distribution is evaluated through two complementary indicators:

* fairness gap;
* coefficient of variation of physiotherapist utilization.



The fairness gap captures the difference between the most utilized and the least utilized physiotherapist. The coefficient of variation provides a broader measure of dispersion across all physiotherapists. The results show slight variations in workload distribution under continuity-of-care scenarios. Stronger continuity requirements may create localized workload concentration, because assigning the same patient to the same physiotherapist reduces allocation flexibility. However, these variations do not indicate a systematic workload imbalance. The effect appears limited and manageable in the tested environment.



**Computational Sustainability**

Resolution time is the KPI where the impact of continuity of care is most visible. The total continuity scenario tends to require more computational effort, which is consistent with the additional assignment restrictions introduced by stronger continuity constraints. However, the increase in resolution time remains within an acceptable range. This suggests that the model remains computationally sustainable for the analysed instance size.



**Representative Instance Interpretation**

A representative run shows that some unused capacity may remain even when rooms or therapists are not fully saturated. This is not necessarily caused by a lack of available resources. It may be structurally induced by the interaction between patient availability, therapist availability, required sessions and continuity constraints. For example, a patient may not be scheduled if all required sessions cannot be inserted consistently within the planning horizon. Similarly, a patient requiring manual sessions may be difficult to schedule if no physiotherapist can provide all required sessions while preserving continuity of care.



**Main Managerial Insight**

The main finding is that continuity of care can be operationally sustainable. In the tested setting, continuity constraints do not reduce global utilization, do not reduce total system benefit and do not compromise service effectiveness. They may introduce some additional coordination complexity, especially in terms of workload distribution and computational effort, but this effect remains limited. From a managerial perspective, this suggests that patient-centred scheduling and operational efficiency can coexist under suitable structural conditions.



**Limitations**

The model is deterministic and relies on synthetic data.

The results should not be interpreted as universal conclusions for all outpatient physiotherapy centres. Different demand levels, tighter capacity, more irregular availability or real-world uncertainty may lead to stronger trade-offs.

The analysis does not directly measure economic outcomes. The cost of continuity of care is interpreted as an operational opportunity cost, not as a monetary cost.



**Future Developments**

Possible future extensions include:

* no-show modelling;
* appointment cancellations;
* stochastic session durations;
* emergency patient insertions;
* larger and more saturated instances;
* stochastic programming formulations;
* Markov decision processes;
* additional clinical sequencing constraints;
* economic evaluation of continuity-of-care policies.



