from typing import Dict, Union, List

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, Aer, transpile
from qiskit.circuit import Qubit, Clbit
from qiskit.result import Result


def parse_result(
        qiskit_result: Result, circuit: QuantumCircuit,
        indexed_results: bool = True) -> Dict[Union[Qubit, int], Dict[str, int]]:

    qubit_clbit_mapping = _get_qubit_mapping(circuit)
    parsed_results = {}
    for state, count in qiskit_result.get_counts().items():
        parsed_state = _parse_state(state)
        for qubit_index in range(len(circuit.qubits)):
            key = qubit_index if indexed_results else circuit.qubits[qubit_index]
            measurement_index = qubit_clbit_mapping[qubit_index]

            if measurement_index is None:
                continue

            qubit_state = parsed_state[measurement_index]

            if key not in parsed_results:
                parsed_results[key] = {'0': 0, '1': 0}
            parsed_results[key][qubit_state] += count

    return parsed_results


def _get_qubit_mapping(circuit: QuantumCircuit) -> List[Union[None, int]]:
    qubit_mapping = [None] * circuit.num_qubits
    for instruction, qubits, bits in circuit.get_instructions('measure'):
        qubit_index = circuit.qubits.index(qubits[0])
        qubit_mapping[qubit_index] = _get_real_clbit_index(circuit, bits[0])
    return qubit_mapping


def _get_real_clbit_index(circuit: QuantumCircuit, clbit: Clbit) -> int:
    creg_index = 0
    for creg in reversed(circuit.cregs):
        if clbit in creg:
            clbit_index = creg.index(clbit)
            return creg_index + (len(creg) - clbit_index - 1)
        else:
            creg_index += len(creg)


def _parse_state(state: str) -> str:
    return state.replace(" ", "")
