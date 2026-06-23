from investiq.bootstrap.live import bootstrap_live_runtime

if __name__ == "__main__":
    live_runtime = bootstrap_live_runtime()
    live_runtime.run_ibkr_thread()
    live_runtime.run_process_thread()