from collections.abc import Sequence
from typing import Union

from qiskit import QuantumCircuit
from qiskit.circuit import Instruction, Qubit, Clbit

from qiskit_utils.insert import insert_instruction


class QuantumCircuitEnhanced(QuantumCircuit):
    def insert(
            self, instruction: Instruction, qubits: Union[Sequence[Qubit, int]],
            clbits: Union[Sequence[Clbit, int]], index: int, in_place: bool = True) -> QuantumCircuit:
        """

        :param instruction:
        :param qubits:
        :param clbits:
        :param index:
        :param in_place:
        :return:
        """
        return insert_instruction(self, instruction, qubits, clbits, index, in_place=in_place)
