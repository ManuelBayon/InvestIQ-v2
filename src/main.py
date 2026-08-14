from investiq.bootstrap.synthetic import bootstrap_synthetical_runtime

if __name__ == "__main__":
    synthetic_runtime = bootstrap_synthetical_runtime("TEST_RUN", 1)
    synthetic_runtime.run()

    #live_runtime = bootstrap_live_runtime("TEST_LIVE_RUN")
    #live_runtime.run()