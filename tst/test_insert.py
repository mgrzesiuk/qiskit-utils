from math import pi
from unittest import TestCase

from qiskit import QuantumCircuit
from qiskit.circuit import Clbit, Qubit
from qiskit.circuit.exceptions import CircuitError
from qiskit.circuit.library import RGate, Measure, iSwapGate
from pytest import raises

from qiskit_utils import insert_instruction


class TestInsert(TestCase):
    def test_insert_correct_when_one_qubit_instruction(self):
        circuit = self._prepare_circuit()
        instruction = RGate(pi/2, pi/4)
        insert_instruction(circuit, instruction, (0,), (), 4)
        assert instruction in circuit.get_instructions('r')[0]
        assert len(circuit.get_instructions('r')) == 1

    def test_insert_correct_when_one_qubit_one_bit_instruction(self):
        circuit = self._prepare_circuit()
        instruction = Measure()
        insert_instruction(circuit, instruction, (circuit.qubits[0],), (circuit.clbits[1], ), 2)
        assert instruction in circuit.get_instructions('measure')[0]
        assert len(circuit.get_instructions('measure')) == 2

    def test_insert_correct_when_multiple_qubit_instruction(self):
        circuit = self._prepare_circuit()
        instruction = iSwapGate()
        insert_instruction(circuit, instruction, (circuit.qubits[0], circuit.qubits[2]), (), 3)
        assert instruction in circuit.get_instructions('iswap')[0]
        assert len(circuit.get_instructions('iswap')) == 1

    def test_insert_raises_circuit_error_when_mismatch_with_instruction_interface(self):
        with raises(CircuitError) as exc:
            circuit = self._prepare_circuit()
            instruction = iSwapGate()
            insert_instruction(circuit, instruction, (circuit.qubits[1],), (), 3)

    def test_insert_raises_value_error_when_not_instruction_given(self):
        with raises(ValueError) as exc:
            circuit = self._prepare_circuit()
            instruction = QuantumCircuit()
            insert_instruction(circuit, instruction, (circuit.qubits[1],), (), 3)
        assert str(exc.value) == "specified instruction is not of type Instruction"

    def test_insert_raises_value_error_when_none_instruction_given(self):
        with raises(ValueError) as exc:
            circuit = self._prepare_circuit()
            instruction = None
            insert_instruction(circuit, instruction, (circuit.qubits[1],), (), 3)
        assert str(exc.value) == "specified instruction is not of type Instruction"

    def test_insert_raises_value_error_when_incorrect_qubits(self):
        with raises(ValueError) as exc:
            circuit = self._prepare_circuit()
            instruction = RGate(pi / 2, pi / 4)
            insert_instruction(circuit, instruction, (circuit.clbits[0],), (), 3)

    def test_insert_raises_value_error_when_incorrect_clbits(self):
        with raises(ValueError) as exc:
            circuit = self._prepare_circuit()
            instruction = Measure()
            insert_instruction(circuit, instruction, (circuit.qubits[0],), (circuit.qubits[1], ), 3)

    def test_insert_raises_circuit_error_when_missing_qubits(self):
        with raises(CircuitError) as exc:
            circuit = self._prepare_circuit()
            instruction = iSwapGate()
            insert_instruction(circuit, instruction, (circuit.qubits[0], Qubit()), (), 3)

    def test_insert_raises_circuit_error_when_missing_clbits(self):
        with raises(CircuitError) as exc:
            circuit = self._prepare_circuit()
            instruction = Measure()
            insert_instruction(circuit, instruction, (circuit.qubits[0],), (Clbit(), ), 3)

    @staticmethod
    def _prepare_circuit() -> QuantumCircuit:
        circuit = QuantumCircuit(3, 2)
        circuit.h(0)
        circuit.cx(0, 2)
        circuit.ccx(1, 2, 0)
        circuit.measure(1, 0)
        return circuit
