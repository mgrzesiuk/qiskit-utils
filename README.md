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

## Result parsing
parse_result method allows to find the counts for each specific qubit individually
(and allows for easy access to check counts for that one specific qubit, independent of the other qubit states)
```python
qc = QuantumCircuit(1, 1)
qc.x(0)
qc.measure(0, 0)
backend = Aer.get_backend("aer_simulator")
transpiled_circuit = transpile(circuit, backend)
result = backend.run(transpiled_circuit).result()

parsed_counts = parse_result(result, qc)
# parsed_counts = {0: {'0': 0, '1': 1024}} 
```
2 return types are possible, with using the flag indexed_results=True resulting directory keys (the most upper level)
will be indexes of qubits (indexes will be same as in qc.qubits), with the flag set to false qubits will be returned
indexed by the qubit object itself (can be received either from qc.qubits[i] or QuantumRegister()[i])