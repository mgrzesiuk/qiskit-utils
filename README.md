# qiskit-utils
qiskit-utils is a library containing utility, quality of life methods for qiskit.

## current methods
  - parsing results
  - inserting instructions and gates into circuit (in any location not just append the gate to the circuit)

## Inserting instructions
```python
from qiskit_utils import insert_instruction

instruction = Measure()
insert_instruction(circuit, instruction, (circuit.qubits[0],), (circuit.clbits[1], ), index)
```

## QuantumCircuitEnhanced
```python
from qiskit.circuit.library import iSwapGate
from qiskit_utils import QuantumCircuitEnhanced

qc = QuantumCircuitEnhanced(2)
qc.insert(iSwapGate(), (0, 1), (,), index)
```
