from investiq.bootstrap.live import bootstrap_live_runtime
from investiq.bootstrap.synthetic import bootstrap_synthetical_runtime

if __name__ == "__main__":

    synthetical_runtime = bootstrap_synthetical_runtime("TEST_RUN")
    live_runtime = bootstrap_live_runtime("TEST_RUN")

    #synthetical_runtime.run()
    live_runtime.run()