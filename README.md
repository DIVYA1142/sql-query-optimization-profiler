# Database Performance Tuning & Query Optimization Audit
## Profiling Database Speeds and Eliminating Full Table Scan Bottlenecks

### 💼 Why I Built This
In large-scale corporate banking networks, poorly structured database configurations lead to massive query delays and server spikes. With 7+ years of database engineering experience, I built this system to show how index structures dramatically optimize performance. 

This project builds a data warehouse of 50,000 transaction rows, monitors query latency under an unoptimized condition, adds a tailored Composite Index, and tracks the speed improvements using Python benchmarking tools.

### 🧠 The Engineering Logic Used
When a database handles thousands of production rows, how queries are indexed changes everything:

1. **Unoptimized State (Full Table Scan):** Without an index, the database engine has to check every single row one-by-one to find data. This wastes processing time.
2. **Composite Index Structure:** We engineer a multi-column database pointer index (`PROCESSING_ZONE`, `TRANSACTION_TYPE`) that maps directly to our filtering conditions. 
3. **Optimized State (Index Search):** The database engine reads our map pointers and jumps directly to the matching rows instantly, skipping the rest of the table.

### 🛠️ The Tools Used
* **Database Engine:** SQL (`sqlite3`) to build a 50,000-row warehouse table and run index modifications.
* **Performance Profiler:** Python (`time.perf_counter`) to record precise query clocks down to the millisecond across 200 testing loops.
* **Analytical Framework:** Python (`Pandas` and `NumPy`) to aggregate performance data.
* **Diagnostics Dashboard:** Python (`Seaborn` and `Matplotlib`) to generate latency distributions.

### 📊 How the Data Flows
1. **The Core Feed:** The system populates a mock ledger `SYSTEM_AUDIT_LOG` with 50,000 high-volume transaction lines.
2. **The Benchmark Phase 1:** Python runs a filtered query 100 times against the unindexed table and logs the clock speeds.
3. **The Tuning Phase:** The script injects a composite structural database index (`IDX_LOG_ZONE_TYPE`).
4. **The Benchmark Phase 2:** Python runs the exact same query 100 more times against the optimized index layout.
5. **The Reporting Phase:** The script calculates the exact efficiency gains and outputs side-by-side performance graphs.

### 📈 Reading the Performance Charts
* **Left Chart (Average Execution Time):** Visually compares the drop in query speed. It showcases a stark, dramatic decline in processing time required after the index layer is applied.
* **Right Chart (Latency Distribution):** Uses boxplots to prove that the index not only speeds up the system but also stabilizes execution ranges, removing unstable variance spikes.

<img width="4800" height="1800" alt="query_optimization_benchmark" src="https://github.com/user-attachments/assets/81556ef0-5953-4a77-8a2e-327c14ab7497" />
