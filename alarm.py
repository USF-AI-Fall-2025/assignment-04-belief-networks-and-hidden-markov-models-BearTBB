from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.inference import VariableElimination

alarm_model = DiscreteBayesianNetwork(
    [
        ("Burglary", "Alarm"),
        ("Earthquake", "Alarm"),
        ("Alarm", "JohnCalls"),
        ("Alarm", "MaryCalls"),
    ]
)

# Defining the parameters using CPT
from pgmpy.factors.discrete import TabularCPD

cpd_burglary = TabularCPD(
    variable="Burglary", variable_card=2, values=[[0.001], [0.999]],
    state_names={"Burglary":['yes', 'no']},
)
cpd_earthquake = TabularCPD(
    variable="Earthquake", variable_card=2, values=[[0.002], [0.998]],
    state_names={"Earthquake":["yes", "no"]},
)
cpd_alarm = TabularCPD(
    variable="Alarm",
    variable_card=2,
    values=[[0.95, 0.94, 0.29, 0.001], [0.05, 0.06, 0.71, 0.999]],
    evidence=["Burglary", "Earthquake"],
    evidence_card=[2, 2],
    state_names={"Burglary":['yes', 'no'], "Earthquake":['yes', 'no'], 'Alarm':['yes', 'no']},
)
cpd_johncalls = TabularCPD(
    variable="JohnCalls",
    variable_card=2,
    values=[[0.9, 0.05], [0.1, 0.95]],
    evidence=["Alarm"],
    evidence_card=[2],
    state_names={"Alarm":['yes', 'no'], "JohnCalls":['yes', 'no']},
)
cpd_marycalls = TabularCPD(
    variable="MaryCalls",
    variable_card=2,
    values=[[0.7, 0.01], [0.3, 0.99]],
    evidence=["Alarm"],
    evidence_card=[2],
state_names={"Alarm":['yes', 'no'], "MaryCalls":['yes', 'no']},
)

# Associating the parameters with the model structure
alarm_model.add_cpds(
    cpd_burglary, cpd_earthquake, cpd_alarm, cpd_johncalls, cpd_marycalls)

alarm_infer = VariableElimination(alarm_model)

# print(alarm_infer.query(variables=["JohnCalls"],evidence={"Earthquake":"yes"}))

# the probability of Mary Calling given that John called

# q = alarm_infer.query(variables=["Alarm", "Burglary"],evidence={"MaryCalls":"yes"})
# print(q)

print("P(M|J)")
q = alarm_infer.query(variables=["MaryCalls"],evidence={"JohnCalls":"yes"})
print(q, "\n")

print("P(J^M|A)")
q = alarm_infer.query(variables=["JohnCalls", "MaryCalls"],evidence={"Alarm":"yes"})
print(q, "\n")

print("P(A|M)")
q = alarm_infer.query(variables=["Alarm"],evidence={"MaryCalls":"yes"})
print(q, "\n")