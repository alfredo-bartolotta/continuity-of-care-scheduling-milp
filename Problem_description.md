**Problem Description**



**Context**

Outpatient physiotherapy services must balance operational efficiency with patient-centred care. Scheduling decisions do not only affect resource utilization, but can also influence the perceived quality of the service. A key element in this context is continuity of care, which refers to the consistent assignment of a patient to the same healthcare provider across the treatment pathway. In physiotherapy, continuity of care may support a stronger therapeutic relationship, better patient experience and improved perceived service quality.



**Research Gap**

Many healthcare scheduling models focus on throughput, waiting time reduction, resource utilization, workload balancing or no-show management. However, continuity of care is often treated as a secondary preference or is not explicitly modelled as a structural scheduling requirement. This project addresses this gap by embedding continuity of care directly into a mathematical scheduling model for outpatient physiotherapy.



**Scheduling Setting**

The model considers a hypothetical outpatient physiotherapy centre.

The centre provides two types of therapy:

* hand-based therapy;
* machine-based therapy.



Hand-based therapy requires the active involvement of a physiotherapist throughout the session. Machine-based therapy requires equipment and therapist supervision.

The planning horizon is weekly and is discretized into:

* 5 days;
* 12 one-hour time slots per day.



The scheduling problem assigns:

* patients;
* physiotherapists;
* therapy types;
* days;
* time slots.



The schedule must respect clinical requirements, patient availability, physiotherapist availability and capacity constraints.



**Input Data**

The model uses synthetic data generated through Python.

The main input elements are:

* number of patients;
* number of physiotherapists;
* number of rooms;
* number of machines;
* number of days;
* number of time slots;
* patient urgency level;
* patient waiting time;
* number of required sessions by therapy type;
* patient availability;
* physiotherapist availability.



The patient priority index is based on urgency and waiting time.



**Decision Variables**

The model includes binary decision variables representing:

* whether a patient is assigned to a physiotherapist for a given therapy type, day and time slot;
* whether a patient is assigned to a physiotherapist for continuity-of-care purposes;
* whether a patient is scheduled.



The main scheduling variable simultaneously captures patient, physiotherapist, therapy type, day and time slot.



**Objective Function**

The objective function maximizes total system benefit. Each scheduled session contributes to the objective value according to the priority of the patient. This means that the model does not simply maximize the number of scheduled sessions, but gives more weight to patients with higher clinical urgency and longer waiting time.



**Main Constraints**

The model includes constraints related to:

* physiotherapist availability;
* patient availability;
* no overlapping sessions for the same patient;
* maximum number of sessions per therapy type per day;
* room capacity;
* machine capacity;
* exact fulfilment of prescribed treatment plans for scheduled patients;
* continuity of care;
* consistency between patient selection and physiotherapist assignment.



**Continuity-of-Care Scenarios**

The project compares three scenarios.



**Scenario A: CoC for Manual Sessions**

Continuity of care is required only for hand-based therapy sessions. If a patient requires multiple hand-based sessions, all those sessions must be assigned to the same physiotherapist. Machine-based sessions remain flexible.



**Scenario B: No CoC**

Continuity-of-care constraints are deactivated. Any session can be assigned to any available physiotherapist, subject to the operational constraints of the model. This scenario represents a more flexible classical scheduling configuration.



**Scenario C: CoC for All Session Types**

Continuity of care is required for both hand-based and machine-based sessions. This is the most restrictive scenario because the same physiotherapist must follow the patient across all session types.



**Experimental Design**

The model is tested on synthetic instances.

The main setting includes:

* 100 patients;
* 10 physiotherapists;
* 4 rooms;
* 4 machines;
* 5 days;
* 12 time slots per day.

Ten instances are generated and solved for each of the three continuity-of-care scenarios.



**Evaluation Framework**

The scenarios are evaluated through the following KPIs:

* total system benefit;
* percentage of patients scheduled;
* percentage of sessions scheduled;
* global physiotherapist utilization;
* fairness gap of physiotherapist utilization;
* coefficient of variation of physiotherapist utilization;
* resolution time.



These KPIs are grouped into four dimensions:

* operational efficiency;
* service effectiveness;
* workload distribution;
* computational sustainability.



**Implementation Note**

The MILP model is implemented in FICO Xpress. Python is used for synthetic instance generation, KPI processing and visualization. The Python support scripts were developed and adapted with support during the thesis work. They are included in this repository to document the computational workflow and reproduce the main analysis outputs.



**Limitations**

The model is deterministic. Demand, availability, session duration and attendance are assumed to be known.

The data are synthetic and generated for experimental purposes.

Future developments could include stochastic demand, no-shows, cancellations, variable service times, emergency insertions and larger-scale instances.



