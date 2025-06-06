# 🧠 Optimization Project with Gurobi & Streamlit

This project provides interactive solutions to two classic operations research problems using **Gurobi Optimizer** and a **Streamlit** interface:

- 🗺️ Facility Location Problem (FLP)
- 🏭 Factory Planning Problem (FPP)

Both models are fully parameterized and user-friendly, allowing you to input data and instantly get optimized results with visual feedback.

---

## 🚀 Features

### 🗺️ Facility Location Problem
- Determine optimal locations for facilities to minimize total costs.
- Customize:
  - Number and location of facilities/customers.
  - Setup costs and per-mile transport costs.
- Solve and visualize:
  - Which facilities to build.
  - Shipment plan from facilities to customers.
  - Graphical plot of customer-facility relationships.

### 🏭 Factory Planning Problem
- Maximize total profit over several months by planning:
  - Production
  - Storage
  - Sales
- Configure:
  - Profits, storage cost, demand, and labor availability.
  - Raw material limits and usage.
  - Labor downtime periods.
- Output:
  - Optimal production and inventory plan.
  - Resource and raw material usage breakdown.

---

## 📦 Tech Stack

- **[Gurobi Optimizer](https://www.gurobi.com/)** – High-performance solver for LP/MIP models.
- **[Streamlit](https://streamlit.io/)** – Intuitive and fast UI for model interaction.
- **Matplotlib** – Visualizing results for FLP.
- **Pandas** – Tabular data display and processing.

---

## 📂 Project Structure

```bash
📁 optimization-project/
├── facility_location.py       # FLP model and visualization
├── factory_planning.py        # FPP model with Gurobi
├── Home.py                     # Streamlit interface
├── data/                      # (Optional) Data samples or templates
├── requirements.txt           # Dependencies
└── README.md                  # This file
 
```


## 🚀 How to Run

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Create and activate a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app:**

   ```bash
   streamlit run Home.py
   ```

    
