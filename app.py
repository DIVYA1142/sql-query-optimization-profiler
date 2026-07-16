import sqlite3
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns

# Set clean styling configurations for our charts
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 11, 'figure.titlesize': 14})

# ========================================================
# STEP 1: DATABASE SETUP (HIGH-VOLUME TRANSACTION LEDGER)
# ========================================================
print("Initializing performance database testing environment...")
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create table tracking 50,000 retail banking transaction rows
cursor.execute("""
CREATE TABLE SYSTEM_AUDIT_LOG (
    LOG_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ACCOUNT_NUMBER TEXT,
    TRANSACTION_TYPE TEXT,
    TRANSACTION_VALUE REAL,
    PROCESSING_ZONE TEXT
);
""")

print("Generating 50,000 randomized records to simulate production scale...")
np.random.seed(42)
records_count = 50000
mock_bulk_data = [
    (
        f"ACC-{np.random.randint(1000, 2000)}",
        np.random.choice(['DEBIT', 'CREDIT', 'FX_TRANSFER', 'ACH']),
        float(np.random.uniform(10.0, 50000.0)),
        np.random.choice(['ZONE_EAST', 'ZONE_WEST', 'ZONE_NORTH', 'ZONE_SOUTH'])
    )
    for _ in range(records_count)
]

cursor.executemany("INSERT INTO SYSTEM_AUDIT_LOG (ACCOUNT_NUMBER, TRANSACTION_TYPE, TRANSACTION_VALUE, PROCESSING_ZONE) VALUES (?, ?, ?, ?);", mock_bulk_data)
conn.commit()
print(f"Successfully generated and loaded {records_count} rows.")

# ========================================================
# STEP 2: TEST UNOPTIMIZED QUERY PERFORMANCE (NO INDEX)
# ========================================================
print("\nTesting Query Phase 1: Running UNOPTIMIZED scan query...")
target_zone = 'ZONE_SOUTH'
target_type = 'FX_TRANSFER'

# Run the query multiple times to get an accurate average execution speed
unindexed_times = []
for _ in range(100):
    start_time = time.perf_counter()
    cursor.execute(f"SELECT * FROM SYSTEM_AUDIT_LOG WHERE PROCESSING_ZONE='{target_zone}' AND TRANSACTION_TYPE='{target_type}';").fetchall()
    unindexed_times.append((time.perf_counter() - start_time) * 1000) # Convert to Milliseconds

# ========================================================
# STEP 3: DATABASE TUNING & INDEX ADDITION
# ========================================================
print("\nTuning Database Environment: Creating Composite Database Index...")
cursor.execute("CREATE INDEX IDX_LOG_ZONE_TYPE ON SYSTEM_AUDIT_LOG (PROCESSING_ZONE, TRANSACTION_TYPE);")
conn.commit()

# ========================================================
# STEP 4: TEST OPTIMIZED QUERY PERFORMANCE (INDEXED)
# ========================================================
print("Testing Query Phase 2: Running OPTIMIZED search query...")
indexed_times = []
for _ in range(100):
    start_time = time.perf_counter()
    cursor.execute(f"SELECT * FROM SYSTEM_AUDIT_LOG WHERE PROCESSING_ZONE='{target_zone}' AND TRANSACTION_TYPE='{target_type}';").fetchall()
    indexed_times.append((time.perf_counter() - start_time) * 1000)

conn.close()

# Assemble the timing metrics into a clean reporting data table
df_perf = pd.DataFrame({
    'Execution Time (ms)': unindexed_times + indexed_times,
    'Database Optimization Status': ['Unoptimized (Full Table Scan)'] * 100 + ['Optimized (Composite Index)'] * 100
})

# ========================================================
# STEP 5: PERFORMANCE AUDIT VISUALIZATION LAYER
# ========================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Database Query Optimization Audit & Latency Profiling', weight='bold')

# Chart 1: Average Speed Comparison Metrics
sns.barplot(
    x="Database Optimization Status", 
    y="Execution Time (ms)", 
    data=df_perf, 
    errorbar=None, 
    palette="Set1", 
    ax=axes[0]
)
axes[0].set_title("Average Query Execution Time (Lower is Better)", weight='semibold')
axes[0].set_ylabel("Latency Window (Milliseconds)")

# Chart 2: Latency Distribution Ranges (Showing Stability)
sns.boxplot(
    x="Database Optimization Status", 
    y="Execution Time (ms)", 
    data=df_perf, 
    palette="Set1", 
    ax=axes[1]
)
axes[1].set_title("Latency Distribution & System Stability Outliers", weight='semibold')
axes[1].set_ylabel("Latency Window (Milliseconds)")

plt.tight_layout()
plt.savefig('query_optimization_benchmark.png', dpi=300)
plt.show()

# Calculate and display the final efficiency percentage score
print(f"\nOptimization Result: Index tracking reduced average latency from {np.mean(unindexed_times):.4f}ms to {np.mean(indexed_times):.4f}ms.")
print(f"System performance improved by {((np.mean(unindexed_times) - np.mean(indexed_times)) / np.mean(unindexed_times) * 100):.2f}%!")
