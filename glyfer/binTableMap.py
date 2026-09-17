import numpy as np

class FontTableBinaryMapper:
    """
    Models the internal structure of OpenType tables and their performance limits.
    """
    def __init__(self):
        # Raw structure table sizes (in bytes) for Adam's custom Latin display font
        self.raw_tables = {
            "glyf": 45000,   # Vector line geometries (quadratic arcs)
            "gpos": 18000,   # Glyph positioning (Kerning pair coordinates)
            "gsub": 12000,   # Glyph substitution arrays (Ligatures, alternates)
            "cmap": 4500,    # Unicode index mapping lookups
            "head_hhea": 500 # Header metrics and horizontal bounding values
        }
        
        # Exact efficiency multiplier factors when run through WOFF2 Brotli transforms
        # Delat-encoded coordinates (glyf) compress better than binary pointer blocks (gpos)
        self.brotli_factors = {
            "glyf": 0.42,      # 58% data reduction
            "gpos": 0.65,      # 35% data reduction
            "gsub": 0.55,      # 45% data reduction
            "cmap": 0.35,      # 65% data reduction
            "head_hhea": 0.90   # 10% data reduction
        }

    def process_compression(self):
        compressed_tables = {k: v * self.brotli_factors[k] for k, v in self.raw_tables.items()}
        
        total_raw_kb = sum(self.raw_tables.values()) / 1024.0
        total_woff2_kb = sum(compressed_tables.values()) / 1024.0
        
        return total_raw_kb, total_woff2_kb, compressed_tables

class TrafficExpenseSimulator:
    """
    Simulates monthly egress costs over rising traffic tiers.
    """
    def __init__(self, raw_kb: float, woff2_kb: float, cost_per_gb: float = 0.08):
        self.raw_kb = raw_kb
        self.woff2_kb = woff2_kb
        self.cost_per_gb = cost_per_gb
        # Traffic ranges: from basic portfolio layouts up to viral high usage tiers
        self.traffic_tiers = np.array([5000, 25000, 100000, 500000, 1000000])

    def run_simulation(self):
        results = []
        for views in self.traffic_tiers:
            # Convert asset downloads directly to Gigabytes (GB)
            raw_gb = (views * (self.raw_kb * 1024)) / (1024 ** 3)
            woff2_gb = (views * (self.woff2_kb * 1024)) / (1024 ** 3)
            
            # Compute final walking costs based on cloud provider egress baselines
            cost_raw = raw_gb * self.cost_per_gb
            cost_woff2 = woff2_gb * self.cost_per_gb
            
            results.append({
                "views": views,
                "raw_gb": raw_gb,
                "woff2_gb": woff2_gb,
                "cost_raw": cost_raw,
                "cost_woff2": cost_woff2,
                "net_saved": cost_raw - cost_woff2
            })
        return results

# ==========================================
# EXECUTE ARCHITECTURAL GRAPH PARSES
# ==========================================
mapper = FontTableBinaryMapper()
raw_kb, woff2_kb, compressed_breakdown = mapper.process_compression()

simulator = TrafficExpenseSimulator(raw_kb, woff2_kb)
simulation_data = simulator.run_simulation()

print("==================================================================")
print("📊 INTERNAL FILE MATRIX METRICS (ADAM'S LATIN DISPLAY TYPEFACE)")
print("==================================================================")
print(f"   ├── Total Uncompressed Byte Space : {raw_kb:.2f} KB")
print(f"   ├── Total Optimised WOFF2 Space   : {woff2_kb:.2f} KB")
print(f"   └── Global Data Footprint Drop    : {((raw_kb - woff2_kb)/raw_kb)*100:.1f}% lower")
print("\n🔏 BINARY SUB-TABLE COMPRESSION CONTRIBS:")
for table, bytes_size in mapper.raw_tables.items():
    saved = bytes_size - compressed_breakdown[table]
    print(f"   ├── [{table.upper()}] Raw: {bytes_size}B ➡️ WOFF2: {compressed_breakdown[table]:.0f}B (Deflated {saved/bytes_size*100:.0f}%)")
print("==================================================================")
