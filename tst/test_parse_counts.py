from unittest import TestCase

from qiskit import QuantumCircuit, Aer, transpile, QuantumRegister, ClassicalRegister
from qiskit.result import Result

from qiskit_utils.parse_counts import parse_counts


class TestParseCounts(TestCase):
    def test_parse_one_register(self):
        qc = QuantumCircuit(3, 2)
        qc.x(0)
        qc.measure(0, 0)
        qc.measure(1, 1)
        result = self._get_counts(qc)
        parsed_counts = parse_counts(result, qc)
        assert parsed_counts == {"10-": 1024}

    def test_parse_one_register_accumulates_states(self):
        qc = QuantumCircuit(2, 1)
        qc.h(1)
        qc.measure(0, 0)
        result = self._get_counts(qc)
        parsed_counts = parse_counts(result, qc)
        assert parsed_counts == {"0-": 1024}

    def test_parse_measure_all(self):
        qc = QuantumCircuit(3, 2)
        qc.x(1)
        qc.measure_all()
        result = self._get_counts(qc)
        parsed_counts = parse_counts(result, qc)
        assert parsed_counts == {"010": 1024}

    def test_parse_multiple_registers(self):
        qr1, qr2 = QuantumRegister(2), QuantumRegister(2)
        cr1, cr2 = ClassicalRegister(2), ClassicalRegister(2)

        qc = QuantumCircuit(qr1, cr1, qr2, cr2)

        qc.x(qr1[0])
        qc.x(qr2[0])

        qc.measure(qr1[0], cr1[0])
        qc.measure(qr1[1], cr1[1])
        qc.measure(qr2[0], cr2[0])
        qc.measure(qr2[1], cr2[1])

        result = self._get_counts(qc)
        parsed_counts = parse_counts(result, qc)
        assert parsed_counts == {"1010": 1024}

    def test_parse_one_bit(self):
        qc = QuantumCircuit(1, 1)
        qc.x(0)
        qc.measure(0, 0)
        result = self._get_counts(qc)
        parsed_counts = parse_counts(result, qc)
        assert parsed_counts == {"1": 1024}

    def test_parse_multiple_registers_with_one_bit(self):
        qr1, qr2 = QuantumRegister(1), QuantumRegister(1)
        cr1, cr2 = ClassicalRegister(1), ClassicalRegister(1)

        qc = QuantumCircuit(qr1, cr1, qr2, cr2)

        qc.x(qr1[0])

        qc.measure(qr1[0], cr1[0])
        qc.measure(qr2[0], cr2[0])

        result = self._get_counts(qc)
        parsed_counts = parse_counts(result, qc)
        assert parsed_counts == {"10": 1024}

    def test_parse_3_registers(self):
        qr1, qr2, qr3 = QuantumRegister(1), QuantumRegister(2), QuantumRegister(3)
        cr1, cr2, cr3 = ClassicalRegister(1), ClassicalRegister(2), ClassicalRegister(3)
        qc = QuantumCircuit(qr1, cr1, qr2, cr2, qr3, cr3)

        qc.x(qr2[1])
        qc.x(qr3[0])
        qc.x(qr3[2])

        qc.measure(qr2[0], cr2[0])
        qc.measure(qr2[1], cr2[1])

        qc.measure(qr3[0], cr3[0])
        qc.measure(qr3[1], cr3[1])
        qc.measure(qr3[2], cr3[2])

        result = self._get_counts(qc)
        parsed_counts = parse_counts(result, qc)
        assert parsed_counts == {"-01101": 1024}

    def test_parse_3_registers_and_measure_all(self):
        qr1, qr2, qr3 = QuantumRegister(1), QuantumRegister(2), QuantumRegister(3)
        cr1, cr2, cr3 = ClassicalRegister(1), ClassicalRegister(2), ClassicalRegister(3)
        qc = QuantumCircuit(qr1, cr1, qr2, cr2, qr3, cr3)

        qc.x(qr2[0])
        qc.x(qr3[0])
        qc.x(qr3[2])

        qc.measure(qr2[0], cr2[0])
        qc.measure(qr2[1], cr2[1])

        qc.measure(qr3[0], cr3[0])
        qc.measure(qr3[1], cr3[1])
        qc.measure(qr3[2], cr3[2])

        qc.measure_all()
        result = self._get_counts(qc)
        parsed_counts = parse_counts(result, qc)
        assert parsed_counts == {"010101": 1024}


    @staticmethod
    def _get_counts(circuit: QuantumCircuit) -> Result:
        backend = Aer.get_backend("aer_simulator")
        transpiled_circuit = transpile(circuit, backend)
        return backend.run(transpiled_circuit).result()

