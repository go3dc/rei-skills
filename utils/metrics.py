import logging
def log_run_stats(count, errors):
    with open('logs/metrics.log', 'a') as f:
        f.write(f"Listings: {count}, Errors: {errors}\n")
