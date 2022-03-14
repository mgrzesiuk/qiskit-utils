from typing import Sequence, Union, Type

from qiskit import QuantumCircuit
from qiskit.circuit import Instruction, Qubit, Clbit
from qiskit.circuit.bit import Bit
from qiskit.circuit.exceptions import CircuitError


def insert_instruction(
        circuit: QuantumCircuit, instruction: Instruction, qubits: Sequence[Union[Qubit, int]],
        clbits: Sequence[Union[Clbit, int]], index: int, in_place: bool = True) -> QuantumCircuit:
    """

    :param circuit:
    :param instruction:
    :param qubits:
    :param clbits:
    :param index:
    :param in_place:
    :return:
    """

    new_circuit = circuit if in_place else circuit.copy()

    if not isinstance(instruction, Instruction):
        raise ValueError("specified instruction is not of type Instruction")

    if index > len(new_circuit.data):
        raise IndexError("index provided is larger than current number of instructions")

    if len(qubits) != instruction.num_qubits or len(clbits) != instruction.num_clbits:
        raise CircuitError(
            "number of qubits or clbits provided doesn't match instruction's qubits and clbits requirements")

    parsed_qubits = _parse_bit(qubits, Qubit, new_circuit)
    parsed_clbits = _parse_bit(clbits, Clbit, new_circuit)
    instruction_tuple = (instruction, parsed_qubits, parsed_clbits)

    new_circuit.data.insert(index, instruction_tuple)
    return new_circuit


def _parse_bit(bits: Sequence[Union[Bit, int]], bit_type: Type[Bit], circuit: QuantumCircuit):
    """

    :param bits:
    :param bit_type:
    :param circuit:
    :return:
    """
    parsed_bits = []
    type_name = {bit_type.__name__}

    for bit in bits:
        if isinstance(bit, bit_type):
            if bit_type == Qubit:
                if bit in circuit.qubits:
                    parsed_bits.append(bit)
                else:
                    raise CircuitError(f"One of the specified {type_name}s is not a part of a circuit, try adding it first")
            elif bit_type == Clbit:
                if bit in circuit.clbits:
                    parsed_bits.append(bit)
                else:
                    raise CircuitError(f"One of the specified {type_name}s is not a part of a circuit, try adding it first")
            else:
                raise ValueError("bit type must be either qiskit.circuit.Clbit or qiskit.circuit.Qubit")
        elif isinstance(bit, int):
            parsed_bits.append(circuit.qubits[bit])
        else:
            raise ValueError(f"Sequence of {type_name}s contains elements that are neither a {type_name} or a int")
    return parsed_bits
