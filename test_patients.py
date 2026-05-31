
import json
import requests

BASE_URL = "http://localhost:8000"

def test_flow():
    # Sample patient data
    patient1 = {
        "id": "P001",
        "Name": "John Doe",
        "City": "New York",
        "Age": 30,
        "Gender": "male",
        "Height": 180,
        "Weight": 75,
        "Blood_Pressure": "120/80",
        "Heart_Rate": 72,
        "Medical_History": ["hypertension", "diabetes"],
        "Verdict": "Improving"
    }

    patient2 = {
        "id": "P002",
        "Name": "Jane Smith",
        "City": "Los Angeles",
        "Age": 45,
        "Gender": "female",
        "Height": 165,
        "Weight": 60,
        "Blood_Pressure": "118/76",
        "Heart_Rate": 68,
        "Medical_History": ["asthma"],
        "Verdict": "Stable"
    }

    # 1. Create two patients
    print("Creating patient P001...")
    resp = requests.post(f"{BASE_URL}/patients", json=patient1)
    assert resp.status_code == 201, f"Failed: {resp.text}"
    print(" OK")

    print("Creating patient P002...")
    resp = requests.post(f"{BASE_URL}/patients", json=patient2)
    assert resp.status_code == 201, f"Failed: {resp.text}"
    print(" OK")

    # 2. Try duplicate creation (should fail)
    print("Attempting duplicate patient P001...")
    resp = requests.post(f"{BASE_URL}/patients", json=patient1)
    assert resp.status_code == 409
    print(" OK (correctly rejected)")

    # 3. Get all patients
    print("Fetching all patients...")
    resp = requests.get(f"{BASE_URL}/patients")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    print(f" OK, got {len(data)} patients")

    # 4. Get single patient by ID
    print("Fetching patient P001...")
    resp = requests.get(f"{BASE_URL}/patients/P001")
    assert resp.status_code == 200
    assert resp.json()["Name"] == "John Doe"
    print(" OK")

    # 5. Filter by city
    print("Filtering by city=New York...")
    resp = requests.get(f"{BASE_URL}/patients?city=New York")
    assert len(resp.json()) == 1
    print(" OK")

    # 6. Filter by age range
    print("Filtering by age>=40...")
    resp = requests.get(f"{BASE_URL}/patients?min_age=40")
    assert len(resp.json()) == 1  # Only Jane
    print(" OK")

    # 7. Filter by medical history
    print("Filtering by medical_history=diabetes...")
    resp = requests.get(f"{BASE_URL}/patients?medical_history=diabetes")
    assert len(resp.json()) == 1
    print(" OK")

    # 8. Update patient (PUT)
    print("Updating P001's City and Verdict...")
    update_payload = {"City": "Brooklyn", "Verdict": "Excellent"}
    resp = requests.put(f"{BASE_URL}/patients/P001", json=update_payload)
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["City"] == "Brooklyn"
    assert updated["Verdict"] == "Excellent"
    print(" OK")

    # 9. Delete a patient
    print("Deleting patient P002...")
    resp = requests.delete(f"{BASE_URL}/patients/P002")
    assert resp.status_code == 204
    # Verify deletion
    resp = requests.get(f"{BASE_URL}/patients/P002")
    assert resp.status_code == 404
    print(" OK")

    # 10. Verify final state
    resp = requests.get(f"{BASE_URL}/patients")
    assert len(resp.json()) == 1  # only P001 remains
    print("\nAll tests passed successfully!")

if __name__ == "__main__":
    test_flow()