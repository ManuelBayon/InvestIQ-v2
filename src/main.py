from investiq.bootstrap.synthetic import bootstrap_synthetical_runtime

if __name__ == "__main__":
    synthetic_runtime = bootstrap_synthetical_runtime()
    synthetic_runtime.run_slow(n=5, delay_seconds=2)