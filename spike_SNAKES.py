# spike_SNAKES.py
# Directions:
# pip install SNAKES

from snakes.nets import PetriNet, Place, Transition, Value, Substitution

net = PetriNet("kuripot")

net.add_place(Place("state_archive", [Value("state_0")]))
net.add_place(Place("updated_state_archive", []))

net.add_transition(Transition("operator_generator"))

net.add_input("state_archive", "operator_generator", Value("state_0"))
net.add_output("updated_state_archive", "operator_generator", Value("state_1"))

transition = net.transition("operator_generator")

binding = Substitution()

if transition.enabled(binding):
    transition.fire(binding)

print(net.place("state_archive").tokens)
print(net.place("updated_state_archive").tokens)