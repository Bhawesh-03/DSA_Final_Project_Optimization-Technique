# benchmark_no_plot.py
import argparse, random, time, statistics, tracemalloc, csv, os
from freq_count import freq_count_naive, freq_count_counter

def benchmark(func, data, trials=3):
    times = []
    peaks = []
    for _ in range(trials):
        tracemalloc.start()
        t0 = time.perf_counter()
        _ = func(data)
        t1 = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        times.append(t1 - t0)
        peaks.append(peak)
    return {
        "mean_time_s": statistics.mean(times),
        "stdev_time_s": statistics.pstdev(times),
        "mean_peak_bytes": statistics.mean(peaks),
        "stdev_peak_bytes": statistics.pstdev(peaks),
        "times": times,
        "peaks": peaks,
    }

def save_csv(results, outdir):
    path = os.path.join(outdir, "benchmark_results.csv")
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["method","mean_time_s","stdev_time_s","mean_peak_bytes","stdev_peak_bytes","times","peaks"])
        for name, r in results.items():
            writer.writerow([
                name,
                f"{r['mean_time_s']:.6f}",
                f"{r['stdev_time_s']:.6f}",
                int(r['mean_peak_bytes']),
                int(r['stdev_peak_bytes']),
                ";".join(f"{t:.6f}" for t in r['times']),
                ";".join(str(p) for p in r['peaks'])
            ])
    return path

def main():
    parser = argparse.ArgumentParser(description="Benchmark data-structure choices for frequency counting (no plotting).")
    parser.add_argument("--n", type=int, default=100_000, help="Number of items to generate")
    parser.add_argument("--k", type=int, default=1000, help="Number of distinct values")
    parser.add_argument("--trials", type=int, default=3, help="Number of benchmark trials")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--outdir", type=str, default="results", help="Output directory for results")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    # Data generation
    rng = random.Random(args.seed)
    data = [rng.randint(1, args.k) for _ in range(args.n)]

    # Run benchmarks
    results = {}
    results["Naive (list.count in loop)"] = benchmark(freq_count_naive, data, trials=args.trials)
    results["Optimized (collections.Counter)"] = benchmark(freq_count_counter, data, trials=args.trials)

    # Save CSV
    csv_path = save_csv(results, args.outdir)
    print(f"Saved results CSV: {csv_path}")

    # Print summary to console
    for name, r in results.items():
        print(f"\n{name}")
        print(f"  mean_time_s: {r['mean_time_s']:.6f} (stdev {r['stdev_time_s']:.6f})")
        print(f"  mean_peak_mb: {r['mean_peak_bytes']/(1024*1024):.2f} (stdev {r['stdev_peak_bytes']/(1024*1024):.2f})")
        print(f"  times: {', '.join(f'{t:.6f}' for t in r['times'])}")
        print(f"  peaks: {', '.join(str(p) for p in r['peaks'])}")

if __name__ == "__main__":
    main()
