# -------------------------------------------------------------
# Hospital Patient Management System
# Author: Kunal Lohia
# Course: Problem Solving with Python (Unit-3)
# -------------------------------------------------------------

import json
from pathlib import Path
import logging

logging.basicConfig(filename="system.log", level=logging.INFO,
                    format="%(asctime)s:%(levelname)s:%(message)s")


# ------------------ Patient Class ------------------

class Patient:
    def __init__(self, name, age, patient_id, disease, status="Admitted"):
        self.name = name
        self.age = age
        self.patient_id = patient_id
        self.disease = disease
        self.status = status

    def __str__(self):
        return f"{self.patient_id} - {self.name} ({self.status})"

    def __repr__(self):
        return self.__str__()

    def admit(self):
        self.status = "Admitted"

    def discharge(self):
        self.status = "Discharged"

    def is_admitted(self):
        return self.status.lower() == "admitted"

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "patient_id": self.patient_id,
            "disease": self.disease,
            "status": self.status
        }


# ------------------ Doctor Class ------------------

class Doctor:
    def __init__(self, name, specialization, doctor_id):
        self.name = name
        self.specialization = specialization
        self.doctor_id = doctor_id

    def __str__(self):
        return f"{self.doctor_id} - Dr. {self.name} ({self.specialization})"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "name": self.name,
            "specialization": self.specialization,
            "doctor_id": self.doctor_id
        }


# ------------------ Hospital Management ------------------

class HospitalManagement:
    def __init__(self):
        self.patients = {}
        self.doctors = {}
        self.data_file = Path("records.json")
        self.load_records()

    # Save to JSON
    def save_records(self):
        try:
            data = {
                "patients": {pid: p.to_dict() for pid, p in self.patients.items()},
                "doctors": {did: d.to_dict() for did, d in self.doctors.items()}
            }
            with open(self.data_file, "w") as f:
                json.dump(data, f, indent=4)
            logging.info("Records saved successfully")
        except Exception as e:
            logging.error(f"Error saving records: {e}")

    # Load JSON
    def load_records(self):
        if self.data_file.exists():
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)

                for p in data.get("patients", {}).values():
                    self.patients[p["patient_id"]] = Patient(
                        p["name"], p["age"], p["patient_id"], p["disease"], p["status"])

                for d in data.get("doctors", {}).values():
                    self.doctors[d["doctor_id"]] = Doctor(
                        d["name"], d["specialization"], d["doctor_id"])

                logging.info("Records loaded successfully")
            except Exception as e:
                logging.error(f"Error loading records: {e}")

    # Add Patient
    def add_patient(self, name, age, patient_id, disease):
        if patient_id in self.patients:
            print("Patient ID already exists.")
            return
        self.patients[patient_id] = Patient(name, age, patient_id, disease)
        self.save_records()
        print("Patient Added Successfully")

    # Add Doctor
    def add_doctor(self, name, specialization, doctor_id):
        if doctor_id in self.doctors:
            print("Doctor ID already exists.")
            return
        self.doctors[doctor_id] = Doctor(name, specialization, doctor_id)
        self.save_records()
        print("Doctor Added Successfully")

    # Assign Doctor
    def assign_doctor(self, patient_id, doctor_id):
        if patient_id not in self.patients:
            print("Patient not found")
            return
        if doctor_id not in self.doctors:
            print("Doctor not found")
            return
        print(f"Doctor {self.doctors[doctor_id].name} assigned to patient {self.patients[patient_id].name}")

    # Search Patient
    def search_patient(self, pid):
        print(self.patients.get(pid, "Patient Not Found"))

    # Search Doctor
    def search_doctor(self, did):
        print(self.doctors.get(did, "Doctor Not Found"))

    # Display Patients
    def display_patients(self):
        for i in self.patients.values():
            print(i)

    # Display Doctors
    def display_doctors(self):
        for i in self.doctors.values():
            print(i)

    # Discharge Patient
    def discharge(self, pid):
        if pid in self.patients:
            self.patients[pid].discharge()
            self.save_records()
            print("Patient Discharged Successfully")
        else:
            print("Patient Not Found")


# ------------------ MENU SYSTEM ------------------

system = HospitalManagement()

while True:
    print("\n========= HOSPITAL MANAGEMENT SYSTEM =========")
    print("1. Add Patient")
    print("2. Add Doctor")
    print("3. Assign Doctor to Patient")
    print("4. Search Patient")
    print("5. Search Doctor")
    print("6. View All Patients")
    print("7. View All Doctors")
    print("8. Discharge Patient")
    print("9. Exit")

    choice = input("Enter your choice: ")

    try:
        if choice == "1":
            system.add_patient(input("Name: "), int(input("Age: ")), input("Patient ID: "), input("Disease: "))

        elif choice == "2":
            system.add_doctor(input("Name: "), input("Specialization: "), input("Doctor ID: "))

        elif choice == "3":
            system.assign_doctor(input("Patient ID: "), input("Doctor ID: "))

        elif choice == "4":
            system.search_patient(input("Enter Patient ID: "))

        elif choice == "5":
            system.search_doctor(input("Enter Doctor ID: "))

        elif choice == "6":
            system.display_patients()

        elif choice == "7":
            system.display_doctors()

        elif choice == "8":
            system.discharge(input("Enter Patient ID: "))

        elif choice == "9":
            print("Exiting System... Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

    except Exception as e:
        print("Error:", e)
        logging.error(f"Runtime Error: {e}")
